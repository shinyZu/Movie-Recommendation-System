FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
# ENTRYPOINT [ "pwd" ]
# CMD ["python", "server.py"]
CMD ["flask","--app","server","run","--host=0.0.0.0"]