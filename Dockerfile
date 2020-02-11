FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install streamlit

COPY install_setup.py install_setup.py
COPY settings.ini settings.ini

RUN python install_setup.py
RUN pip install -r req.txt

WORKDIR /app

COPY . /app

RUN pip install -e .

EXPOSE 8501

CMD ["bash", "start_streamlit.sh"]