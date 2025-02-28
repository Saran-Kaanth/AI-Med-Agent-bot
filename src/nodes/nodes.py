from typing import Literal

from langgraph.types import Command
from langgraph.graph import END

from schemas.schema import State, members
from agents.agents import *


def data_collector_node(state: State) -> Command[Literal["orchestrator"]]:
    result = patient_data_collector_agent.invoke(state)

    return Command(
        update={"messages": [result["messages"][-1].content]}, goto="orchestrator"
    )


def specialist_recommender_node(state: State) -> Command[Literal["orchestrator"]]:
    result = specialist_recommender_agent.invoke(state)

    return Command(
        update={"messages": [result["messages"][-1].content]}, goto="orchestrator"
    )


def doctor_availability_node(state: State) -> Command[Literal["orchestrator"]]:
    result = doctor_availability_agent.invoke(state)

    return Command(
        update={"messages": [result["messages"][-1].content]}, goto="orchestrator"
    )


def appointment_confirmation_node(state: State) -> Command[Literal["orchestrator"]]:
    result = confirmation_agent.invoke(state)

    return Command(
        update={"messages": [result["messages"][-1].content]}, goto="orchestrator"
    )


def retrieval_node(state: State) -> Command[Literal["orchestrator"]]:
    result = rag_agent.invoke(state)

    return Command(
        update={"messages": [result["messages"][-1].content]}, goto="orchestrator"
    )


def human_interrupt(state: State) -> Command[Literal["orchestrator"]]:
    """Node to get the input from user or human"""
    user_input = input("user: ")
    return Command(goto="orchestrator", update={"messages": [user_input]})


def orchestrator_node(state: State) -> Command[Literal[*members, "__end__"]]:
    messages = [{"role": "system", "content": orchestrator_prompt}] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]

    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto, "messages": response["messages"]})
