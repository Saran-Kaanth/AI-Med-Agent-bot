from datetime import datetime, timedelta

from langchain.tools import tool
from sqlalchemy import text

from db.sql import engine
from schemas.schema import *
from rag.retriever import retriever


@tool(
    args_schema=PatientDataSchema,
    description="Tool to add a patient data to the database.",
)
def add_patient(patient_name: str, patient_email: str, patient_mobile: str) -> str:
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT COUNT(*) FROM patient WHERE email = :email"),
                [{"email": patient_email}],
            ).fetchone()
            if not result[0]:
                conn.execute(
                    text(
                        "INSERT INTO patient (name, email, mobile) VALUES (:name, :email, :mobile)"
                    ),
                    [
                        {
                            "name": patient_name,
                            "email": patient_email,
                            "mobile": patient_mobile,
                        }
                    ],
                )
                conn.commit()
        return f"Patient Name: {patient_name}, Email: {patient_email}, Mobile No.: {patient_mobile} stored sucessfully"
    except Exception as e:
        print("Error in adding patient: ", e)
        raise e


@tool(
    args_schema=SpecializationFilterSchema,
    description="Tool to filter the doctors based on the specialist type.",
)
def filter_doctors(specialization: str) -> str:
    try:
        with engine.connect() as conn:
            result = (
                conn.execute(
                    text(
                        "SELECT name, id, specialization FROM doctor WHERE specialization = :specialization"
                    ),
                    [{"specialization": specialization}],
                )
                .mappings()
                .all()
            )
        if result:
            doctor_details = "\n".join(
                [
                    f"Doctor Name: {row['name']}, Doctor ID: {row['id']} Specialization: {row['specialization']}"
                    for row in result
                ]
            )
            return "Specialized doctors are: " + " \n" + doctor_details
        return "There are no specialized doctors available."
    except Exception as e:
        return str(e)


def convert_time(time_str, format_type="24to12"):
    if format_type == "12to24":
        return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")
    elif format_type == "24to12":
        return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")
    else:
        raise ValueError("Invalid format_type. Use '12to24' or '24to12'.")


@tool(
    args_schema=DoctorAvailabilitySchema,
    description="Tool to check the availability of the doctor on a particular date.",
)
def check_doctor_availability(doctor_id: int, date: str) -> str:
    try:
        print("Doctor availability checking")
        with engine.connect() as conn:
            result = (
                conn.execute(
                    text(
                        "SELECT date, start_time, end_time FROM appointment WHERE doctor_id = :doctor_id AND date = :date"
                    ),
                    [{"doctor_id": doctor_id, "date": date}],
                )
                .mappings()
                .all()
            )
        if result:
            booked_time_slots = "\n".join(
                [
                    f"{convert_time(row['start_time'])}-{convert_time(row['end_time'])}"
                    for row in result
                ]
            )
            return f"Doctor booked slots are: {booked_time_slots}"
        return "Doctor is available for the whole day."
    except Exception as e:
        print("Error in checking doctor availability: ", e)
        return str(e)


@tool(args_schema=AppointmentBookingSchema, description="Tool to book an appointment.")
def book_appointment(
    patient_id: int, doctor_id: int, date: str, start_time: str, end_time: str
) -> str:
    try:
        start_time = convert_time(start_time, "12to24")
        time_obj = datetime.strptime(start_time, "%H:%M")
        end_time = time_obj + timedelta(minutes=30)
        end_time = end_time.strftime("%H:%M")

        with engine.connect() as conn:
            conn.execute(
                text(
                    "INSERT INTO appointment (patient_id, doctor_id, date, start_time, end_time) VALUES (:patient_id, :doctor_id, :date, :start_time, :end_time)"
                ),
                [
                    {
                        "patient_id": patient_id,
                        "doctor_id": doctor_id,
                        "date": date,
                        "start_time": start_time,
                    }
                ],
            )
            conn.commit()
        return f"Appointment booked successfully for the patient with ID: {patient_id} with doctor ID: {doctor_id} on {date} at {start_time} to {end_time}."
    except Exception as e:
        return str(e)


@tool(
    args_schema=ContextRetrievalSchema,
    description="Tool to retrieve the relevant context for the user query",
)
def retrieval_tool(question: str):
    try:
        docs = retriever.similarity_search(question, k=5)
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return "Couldn't able to fetch relevant context, please try again later."
