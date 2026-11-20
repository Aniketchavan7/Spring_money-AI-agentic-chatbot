from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from backend.websocket_manager import WebSocketManager
from backend.utils import write_md_to_pdf, write_md_to_word, write_text_to_md
from backend.config_validator import validate_runtime_environment
import time
import json
import os


class ResearchRequest(BaseModel):
    task: str
    report_type: str
    agent: str


app = FastAPI(title="Spring Money AI Agent Server", version="0.1.0")

if os.path.exists("./frontend"):
    app.mount("/site", StaticFiles(directory="./frontend"), name="site")
if os.path.exists("./frontend/static"):
    app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

templates = Jinja2Templates(directory="./frontend") if os.path.exists("./frontend") else None

manager = WebSocketManager()


# Dynamic directory for outputs once first research is run
@app.on_event("startup")
def startup_event():
    if not os.path.isdir("outputs"):
        os.makedirs("outputs")
    app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


@app.get("/")
async def read_root(request: Request):
    if templates:
        return templates.TemplateResponse('index.html', {"request": request, "report": None})
    return {"status": "ok", "service": "Spring Money AI Agent API"}


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint for container orchestrators and load balancers."""
    env_info = validate_runtime_environment()
    return {
        "status": "healthy" if env_info["valid"] else "degraded",
        "service": "Spring Money AI Agent",
        "timestamp": time.time(),
        "warnings": env_info["warnings"],
    }


@app.get("/api/v1/diagnostics")
async def diagnostics():
    """Detailed runtime configuration and active environment diagnostics."""
    return validate_runtime_environment()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("start"):
                json_data = json.loads(data[6:])
                task = json_data.get("task")
                report_type = json_data.get("report_type")
                filename = f"task_{int(time.time())}_{task}"
                if task and report_type:
                    report = await manager.start_streaming(task, report_type, websocket)
                    # Saving report as pdf
                    pdf_path = await write_md_to_pdf(report, filename)
                    # Saving report as docx
                    docx_path = await write_md_to_word(report, filename)
                    # Returning the path of saved report files
                    md_path = await write_text_to_md(report, filename)
                    await websocket.send_json({"type": "path", "output": {"pdf": pdf_path, "docx": docx_path, "md": md_path}})
                else:
                    print("Error: not enough parameters provided.")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
