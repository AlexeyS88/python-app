FROM python:3.15-alpine

WORKDIR /src


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tests .
COPY app ./app 

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]