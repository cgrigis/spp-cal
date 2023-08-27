FROM alpine:3.18.3

COPY requirements.txt ./
RUN apk update --no-cache
RUN apk add --no-cache py3-pip rsvg-convert font-dejavu
RUN pip install --no-cache-dir -r requirements.txt

COPY gen_spp_cal.py serve_calendar.py /home/
COPY templates /home/templates/
COPY lib /home/lib/

CMD [ "hypercorn", \
        "--bind", "0.0.0.0:8000", \
        "/home/serve_calendar:app" ]
