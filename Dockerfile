FROM python:3.9

WORKDIR /project

COPY ./requirements.txt /project/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

COPY ./data /project/data

COPY ./main.py /project/

CMD ["uvicorn", "main:splatform", "--host", "0.0.0.0", "--port", "80"]