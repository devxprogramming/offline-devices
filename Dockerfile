FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \ 
PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt update && apt install -y libssl-dev curl ca-certificates

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# copy and install the requirements file(s) before copying the app
# This is efficient because docker will cache the layer

COPY core/requirements.txt .
COPY core/requirements-dev.txt .
RUN uv pip install -r requirements.txt --system

# Copy the app
COPY core/ .

EXPOSE 8000


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
