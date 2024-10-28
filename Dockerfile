FROM python:3.10

RUN mkdir /dns_test_task

WORKDIR /dns_test_task

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /dns_test_task/docker/*.sh

CMD ["uvicorn", "app.main:app", "--reload", "--bind=0.0.0.0:5000"]