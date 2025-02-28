import os

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from tools.tools import *
from prompts.prompts import *

load_dotenv(override=True)

llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.0)

patient_data_collector_agent = create_react_agent(
    model=llm, tools=[add_patient], prompt=data_collector_prompt
)

specialist_recommender_agent = create_react_agent(
    model=llm, tools=[filter_doctors], prompt=specialist_recommender_prompt
)

doctor_availability_agent = create_react_agent(
    model=llm, tools=[check_doctor_availability], prompt=doctor_availability_prompt
)

confirmation_agent = create_react_agent(
    model=llm, tools=[book_appointment], prompt=confirmation_prompt
)

rag_agent = create_react_agent(model=llm, tools=[retrieval_tool], prompt=rag_prompt)
