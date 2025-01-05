FROM python:3.11-slim

WORKDIR /app/

COPY requirements.txt .

RUN apt-get update && apt install -y libpq-dev iputils-ping 

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["/bin/bash","-c","python manage.py runserver 0.0.0.0:8000 > /dev/stdout"]
