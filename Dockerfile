FROM postgres:latest

ENV POSTGRES_USER postgres
ENV POSTGRES_DB HFC
ENV POSTGRES_PASSWORD mysecretpassword

COPY Database/db-scripts/* /docker-entrypoint-initdb.d/

EXPOSE 5432