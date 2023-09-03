# Generation of "ABCD" calendar

## Run on command line:
```
$ make env
$ . ./venv/bin/activate
$ ./gen_spp_cal.py --help
$ ./gen_spp_cal.py --year 2023 --start-shift A --filename my_cal.svg
```

## Generate pdf:

```
$ rsvg-convert --format pdf my_cal.svg > my_cal.pdf
```

or:
```
$ convert -page A4+0+0 my_cal.svg my_cal.pdf
```

## Run the web app locally:
```
$ make env
$ . ./venv/bin/activate
$ hypercorn --bind 0.0.0.0:<local-port> ./serve_calendar:app
```

The app is then accessible on `http://localhost:<local-port>/`.

## Run the app from Docker:
```
$ docker-compose build
$ docker run --publish <local-port>:8000 cgrigis/spp-cal
```

The app is then accessible on `http://localhost:<local-port>/`.
