To generate pdf:

```
$ rsvg-convert --format pdf calendar.svg > calendar.pdf
```

or:
```
$ convert -page A4+0+0 calendar.svg calendar.pdf
```

Docker:
```
$ docker-compose build
$ docker-compose up -d
```

Get the container IP:
```
$ docker network inspect calendar_default | jq '.[0].Containers[].IPv4Address'
```

The app is then accessible as `<IP>:8000/cal?year=<YEAR>&week_id=<WEEK_ID>`.
