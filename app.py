from flask import Flask, render_template, request, jsonify
import asyncio
from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='frontend', template_folder='frontend')

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/research', methods=['POST'])
def research():
	data = request.json
	query = data.get('query')
	report_type = data.get('report_type', ReportType.ResearchReport.value)

	async def run_research():
		researcher = GPTResearcher(query=query, report_type=report_type)
		await researcher.conduct_research()
		report = await researcher.write_report()
		return report

	report = asyncio.run(run_research())
	return jsonify({'report': report})

if __name__ == '__main__':
	app.run(debug=True, port=5000)