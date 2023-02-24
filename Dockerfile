FROM python:latest
# RUN apk add --update --no-cache postgresql-client

WORKDIR /src/app

COPY requirements.txt requirements.txt
COPY app2.py app2.py
COPY app.py app.py
COPY .streamlit .streamlit
# RUN conda install --file requirements.txt
# RUN pip uninstall streamlit -y
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt
# RUN pip install streamlit -U

EXPOSE 80

ENTRYPOINT [ "streamlit", "run", "app2.py", "--browser.serverAddress", "0.0.0.0"]
# , \
#     "--server.port", "80", \
#     "--server.enableCORS", "true", \
#     "--browser.serverAddress", "0.0.0.0", \
#     "--browser.serverPort", "443"]