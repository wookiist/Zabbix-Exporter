FROM python:2-slim

RUN mkdir -p /app/zabbix_exporter

WORKDIR /app/zabbix_exporter

COPY requirements.txt /app/zabbix_exporter
RUN pip install --no-cache-dir -r requirements.txt

COPY zabbix_exporter.py /app/zabbix_exporter

EXPOSE 9288

ENTRYPOINT ["python", "-u", "./zabbix_exporter.py"]