FROM python:3.11.2-alpine3.17

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY main.py /app/  

COPY utils /app/utils  

COPY auth /app/auth  

COPY database /app/database  

ENV POSTGRES_USER=${POSTGRES_USER}

ENV POSTGRES_DB=${POSTGRES_DB}

ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

EXPOSE 5000

CMD ["python", "main.py"]