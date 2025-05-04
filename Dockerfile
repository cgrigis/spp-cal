FROM alpine:3.21.3

RUN apk update --no-cache
RUN apk add --no-cache py3-pip rsvg-convert font-dejavu

ENV VIRTUAL_ENV=/home/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY gen_spp_cal.py serve_calendar.py /home/
COPY templates /home/templates/
COPY lib /home/lib/

CMD [ "hypercorn", \
        "--bind", "0.0.0.0:8000", \
        "/home/serve_calendar:app" ]
