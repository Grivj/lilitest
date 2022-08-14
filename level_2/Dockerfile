FROM python:3.10

WORKDIR /api

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /api

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "3000"]
