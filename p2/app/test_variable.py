import os

# we are ovveriding env variable to test api on another postgres instance
os.environ["DATABASE_URL"] =  "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
