FROM debian:stable-slim

COPY requirements.txt ./
RUN apt-get update && apt-get install -y python3-pip librsvg2-bin
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY gen_spp_cal.py serve_calendar.py /home/
COPY templates /home/templates/
COPY lib /home/lib/

CMD [ "hypercorn", \
        "--bind", "0.0.0.0:8000", \
        "/home/serve_calendar:app" ]
