FROM python:3.11.2

WORKDIR /penzi

COPY requirements.txt . 

RUN pip install -r requirements.txt

RUN pip install mysql-connector-python


COPY . .

EXPOSE 80

CMD [ "uvicorn", "penzi:app", "--host", "0.0.0.0","--port", "80"]