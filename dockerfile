FROM python:3.11.2-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src /src
COPY .env .
CMD ["py","server.py"]
EXPOSE 5000