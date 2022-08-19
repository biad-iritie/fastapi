FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirement.txt ./

RUN pip install --no-cache-dir -r requirement.txt

COPY  . .

CMD ["cd", "app", "&","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]