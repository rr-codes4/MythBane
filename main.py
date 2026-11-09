import os
from threading import Event, Thread #Shows mssg while ai works in the backgrounds
from datetime import datetime
from pathlib import Path
from ddgs.exceptions import DDGSException
from dotenv import load_dotenv #It Helps me load the env variables
from openai import APIConnectionError
from pydantic import BaseModel,Field #To create a schema and add description
from langchain_openai import ChatOpenAI #To use the OpenAI API
from langchain_core.prompts import ChatPromptTemplate #To create a prompt template for the model
from langchain_core.output_parsers import PydanticOutputParser #To parse the output of the model
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent #To create an agent that can call tools
from resources import search_tool, tool_for_wiki #Importing the search tools from resources.py
from flask import Flask, render_template, request, jsonify # Added for the website

load_dotenv()
model = ChatOpenAI(model="openai/gpt-4o-mini", temperature=0,
                   base_url="https://ai.hackclub.com/proxy/v1",
                   api_key=os.getenv("API_KEY")) #keeping the temperature 0 would make sure the model is deterministic and focused
 #I just want ai to give the most mathematically accurate ans as its gonna debunk myths..rather it would hallucinate
class Report(BaseModel):
    rumor: str = Field(description="The original conspiracy theory or rumor/myth provided")
    verdict: str = Field(description="The final verdict on the rumor/myth, whether it is true or false")
    summary: str=Field(description="A brief summary of the reasoning behind the verdict, including any evidence or sources used to support the conclusion")
    sources: list[str]=Field(description="Any sources or references used to support the verdict, including links to articles, studies, or other relevant information")  
    tool_used: list[str]=Field(description="Any tools or methods used to investigate the rumor/myth, such as fact-checking websites, scientific studies, or expert opinions")
parser = PydanticOutputParser(pydantic_object=Report) #To parse the output of the model into the report schema
def format_report(report: Report, timestamp: str) -> str:
    lines = [
        f"Date/time: {timestamp}",
        f"Rumor: {report.rumor}",
        f"Verdict: {report.verdict}",
        f"Summary: {report.summary}",
    ]
    for label, values in (
        ("Sources", report.sources),
        ("Tools used", report.tool_used),
    ):
        lines.append(f"{label}:")
        lines.extend(f"  - {value}" for value in values)
        if not values:
            lines.append("  -Didn't find any relevant sources or tools used.")
    return "\n".join(lines)
def save_chat_history(query: str, formatted_report: str) -> Path:#To save the chat history to a file
    history_path = Path(__file__).with_name("chat_history.txt")
    with history_path.open("a", encoding="utf-8") as history_file:
        history_file.write(
            f"Question: {query}\n{formatted_report}\n{'-' * 72}\n"
        )
    return history_path
prompts= ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a fact-checking AI that debunks conspiracy theories and rumors. Your task is to provide a verdict on the given rumor or myth, along with a summary of your reasoning and any sources or tools used in your investigation."
            "Sound Diplomatic and Defensive."
            "You have been given the supreme responsibily of destroying stereotypes too and spread love."
            "Be like a detective but avoid being desrespectful to the person who believes in the theory."
            "Use the available search tools to verify claims and cite sources when found. "
            "If web search fails, be transparent that live sources could not be checked and do not invent citations."
            "rumors.\nFollow these formatting guidelines strictly:\n"
            "{format_instructions}"
        ),
    ),
("placeholder","{chat_history}"),
("human","{query}"),
("placeholder","{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions()) #To create a prompt template for the model with the format instructions from the parser
agent = create_tool_calling_agent(
    llm=model,
    prompt=prompts,
    tools=[search_tool, tool_for_wiki],
)
executor= AgentExecutor(
    agent=agent,
    verbose=False,
    tools=[search_tool, tool_for_wiki],
)#I dont want to show the thought process

# --- FLASK WEB APP WIRING ADDED BELOW ---
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/debunk", methods=["POST"])
def debunk():
    data = request.get_json()
    query = data.get("query", "")
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        response = executor.invoke({"query": query}) #Invoking the agent with the user input
    except DDGSException:
        return jsonify({
            "error": "Bruh! Live web search unavailable(DNS, network, rate limit, or no results). Check your connection and try again;the error could be from your side."
        }), 500
    except APIConnectionError:
        return jsonify({
            "error": "AAAh!The AI service timed out(maybe it was used too much).Let it rest human!!."
        }), 500

    try:
        structured = parser.parse(response["output"])
    except Exception as e:
        return jsonify({"error": f"Sorry I am facing error parsing response, try contacting the dev {e}"}), 500
    
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    formatted_report = format_report(structured, timestamp)
    save_chat_history(query, formatted_report)

    # Send structured data back to the website frontend
    return jsonify({
        "rumor": structured.rumor,
        "verdict": structured.verdict,
        "summary": structured.summary,
        "sources": structured.sources,
        "tool_used": structured.tool_used
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

