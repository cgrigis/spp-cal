Run on command line:
```
$ make env
$ . ./venv/bin/activate
$ ./gen_spp_cal.py --help
$ ./gen_spp_cal.py --year 2023 --start-shift A --filename my_cal.svg
```

Generate pdf:

```
$ rsvg-convert --format pdf my_cal.svg > my_cal.pdf
```

or:
```
$ convert -page A4+0+0 my_cal.svg my_cal.pdf
```

Run from Docker:
```
$ docker-compose build
$ docker run --publish <local-port>:8000 cgrigis/spp-cal
```

The app is then accessible on `http://localhost:<local-port>/`.
