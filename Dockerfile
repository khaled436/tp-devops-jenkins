FROM python:latest

WORKDIR /app

COPY /sum.py /app/sum.py

CMD ["tail", "-f","/dev/null"]

# CMD [ "python", "sum.py" ]


#ENTRYPOINT ["python","sum.py"]

