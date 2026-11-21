from agents import Agent, WebSearchTool, trace, Runner, function_tool
import asyncio
from dotenv import load_dotenv
import os
from messenger import push
from tools import push_tool,get_performance_data_tool,median_tool,daily_report_tool
from datetime import datetime 


#from agents.model_settings import ModelSettings
#from pydantic import BaseModel, Field
#from IPython.display import display, Markdown
#import sys

MODEL_NAME = "gpt-5.4-mini"

load_dotenv(override=True)

# Check the key - if you're not using OpenAI, check whichever key you're using! Ollama doesn't need a key.

openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")
   
hours=24
report_date=datetime.now().strftime("%a, %Y-%m-%d %H:%M")

INSTRUCTIONS = f"""
You are a diligent system administrator concern with performance and security
"""
TASK = f"""
your task is to send a daily report about the system's performance and security. 
Include the following report date: {report_date}
Send a message with a report with the median value of the main performance variables of the last {hours} hours.
The report should be structured in a way that is easy to read and understand.

Use your push_tool to send the message. 

Use your get_performance_data_tool to get data about the system. Use localhost as the host. Use the last {hours} hours as the time range.
Check the tool variables description in Args and use only the available variables to call the tool. Use only variables load15, tcp_active and cpu_temp. Use only this variables to call the tool.

Use your median_tool to get the median value of the main performance variables of the last {hours} hours, and the standard deviation. The median tool takes a list of numbers as input and returns a list containing the median value and standard deviation. Show the median value and standard deviation in the report.  Show only 2 decimal places for the standard deviation. If the median tool returns None, show a message indicating that there is no data available for that variable.

Use your daily_report_tool to get and parse JSON data about the system. Use local host as input to this tool. Integrate that information in the report. Write a special warning is disk usage is more than 70%. If this tool returns no text or older than the specified range, say so on the report.  
"""
#print(TASK)

DR_agent = Agent(name="Daily report Agent", instructions=INSTRUCTIONS, tools=[push_tool,get_performance_data_tool,median_tool,daily_report_tool], model=MODEL_NAME)

async def main():       
    #result = await Runner.run(DR_agent, task=TASK)
    #https://platform.openai.com/logs?api=traces
    with trace("Sysadmin daily report"):
        result = await Runner.run(DR_agent,TASK)    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
