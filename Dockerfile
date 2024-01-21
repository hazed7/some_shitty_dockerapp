FROM python:3

WORKDIR /usr/src/

COPY app/requirements.txt app/requirements.txt

RUN pip install --no-cache-dir -r app/requirements.txt

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]