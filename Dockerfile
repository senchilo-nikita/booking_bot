FROM python:3.10

COPY main.py requirements.txt .env ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

CMD ["python","main.py"]