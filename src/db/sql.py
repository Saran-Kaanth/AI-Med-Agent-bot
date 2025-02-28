from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:admin123@localhost/agent-db"

engine = create_engine(DATABASE_URL)
