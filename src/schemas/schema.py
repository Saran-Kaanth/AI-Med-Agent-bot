from typing import Annotated, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel

from langgraph.graph import MessagesState

members = [
    "rag_agent",
    "patient_data_collector_agent",
    "specialist_recommender_agent",
    "doctor_availability_agent",
    "confirmation_agent",
    "human_interrupt_or_input_agent",
]

options = members + ["FINISH"]


class State(MessagesState):
    next: str


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]
    messages: str


class PatientDataSchema(BaseModel):
    patient_name: Annotated[str, "Name of the patient"]
    patient_email: Annotated[str, "Email of the patient"]
    patient_mobile: Annotated[str, "Mobile number of the patient"]


class SpecializationFilterSchema(BaseModel):
    specialization: Annotated[
        Literal["Cardiologist", "Dermatologist", "Oncologist"],
        "Specialization type to filter the doctors (Cardiologist or Dermatologist or Oncologist)",
    ]


class DoctorAvailabilitySchema(BaseModel):
    doctor_id: Annotated[int, "Doctor ID to check the availability"]
    date: Annotated[str, "Date to check the availability"]


class AppointmentBookingSchema(BaseModel):
    patient_id: Annotated[int, "Patient ID to book the appointment"]
    doctor_id: Annotated[int, "Doctor ID to book the appointment"]
    date: Annotated[str, "Date to book the appointment (YYYY-MM-DD)"]
    start_time: Annotated[
        str, "Start time of the appointment (eg. 12:30 PM, 3:00 PM, 9:00 AM)"
    ]


class ContextRetrievalSchema(BaseModel):
    question: Annotated[str, "General hospital related query from the user"]
