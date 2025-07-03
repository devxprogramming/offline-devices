FROM python:latest


ENV PYTHONUNBUFFERED=1 \ 
PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt update && apt install -y libssl-dev curl ca-certificates

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# copy and install the requirements file(s) before copying the app
# This is efficient because docker will cache the layer

COPY core/requirements.txt .
COPY core/requirements-dev.txt .
RUN python -m pip install --upgrade pip
# RUN pip install -r requirements-dev.txt 
RUN  pip install -r requirements.txt

# Copy the app
COPY core/ .

# RUN chmod +x core/manage.py
# RUN python core/manage.py migrate

EXPOSE 8000


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
