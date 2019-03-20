FROM prom/prometheus:v2.0.0
ADD prometheus.yml /etc/prometheus/
ADD ./alert.rules /alertmanager/
EXPOSE 9090