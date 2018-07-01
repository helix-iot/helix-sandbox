FROM python:2.7

MAINTAINER Angelo Moura "m4n3dw0lf@gmail.com"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python","run.py"]
