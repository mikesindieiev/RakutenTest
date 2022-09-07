FROM presidentbeef/brakeman:latest
USER root
RUN apk add --update --no-cache git python3
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
ADD /src/* .
RUN pip install -r requirements.txt 
USER app
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:80", "wsgi:app" ]
EXPOSE 80