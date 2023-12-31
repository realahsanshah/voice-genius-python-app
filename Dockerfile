FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev ffmpeg -y

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "8080"]

EXPOSE 8080

