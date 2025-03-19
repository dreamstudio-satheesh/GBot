FROM ankane/pgvector:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=chatbot_user
ENV POSTGRES_PASSWORD=chatbot_pass
ENV POSTGRES_DB=chatbot_db

# Copy the init.sql file into the container
COPY init.sql /docker-entrypoint-initdb.d/init.sql
