FROM tiangolo/uvicorn-gunicorn:python3.7

RUN pip install fastapi
RUN pip install --upgrade pip

WORKDIR /app
COPY install_setup.py install_setup.py
COPY settings.ini settings.ini

RUN python install_setup.py
RUN pip install -r req.txt

COPY .env .env
COPY setup.py setup.py
COPY settings.ini setup.ini
COPY README.md README.md
COPY ./strava_overview strava_overview
RUN pip install -e .

COPY ./backend /app

# streamlit
EXPOSE 8080 
EXPOSE 80
