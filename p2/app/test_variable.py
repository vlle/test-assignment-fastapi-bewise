import os

# we are ovveriding env variable to test api on another postgres instance
os.environ[
    "DATABASE_URL"
] = "postgresql+psycopg://postgres:postgres@test:5432/postgres"
