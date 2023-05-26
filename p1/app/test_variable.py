import os

# do not touch, this file is needed for test_start.sh
# we are ovveriding env variable to test api on another postgres instance
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:postgres@test:5432/postgres"
