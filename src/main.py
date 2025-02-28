import os

from langgraph.graph import START, StateGraph

from schemas.schema import State
from dotenv import load_dotenv

load_dotenv(override=True)

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
from nodes.nodes import *

if __name__ == "__main__":
    builder = StateGraph(State)
    builder.add_edge(START, "orchestrator")
    builder.add_node("orchestrator", orchestrator_node)
    builder.add_node("rag_agent", retrieval_node)
    builder.add_node("patient_data_collector_agent", data_collector_node)
    builder.add_node("specialist_recommender_agent", specialist_recommender_node)
    builder.add_node("doctor_availability_agent", doctor_availability_node)
    builder.add_node("confirmation_agent", appointment_confirmation_node)
    builder.add_node("human_interrupt_or_input_agent", human_interrupt)

    graph = builder.compile()

    for s in graph.stream(
        {"messages": [("user", "Hi")]}, subgraphs=True, config={"recursion_limit": 30}
    ):
        for key, value in s[1].items():
            if key in members + ["orchestrator"]:
                print(value["messages"])
        print("===" * 30)
