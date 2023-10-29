FROM python:3.10
WORKDIR /code

COPY . /code/certifever-qa

WORKDIR /code/certifever-qa
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:server", "--port", "80"]