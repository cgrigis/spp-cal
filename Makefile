all: calendar

.ONESHELL:

SRC = gen_spp_cal.py serve_calendar.py templates/index.html

PYTEST_OPTIONS := -v
VENV_DIR := venv

$(VENV_DIR):
	python3 -m venv $(VENV_DIR)
$(VENV_DIR)/%: | $(VENV_DIR)
	@: nothing

.PHONY: env
env: requirements.txt $(VENV_DIR)
	. $(VENV_DIR)/bin/activate
	pip3 install -r $<

.PHONY: calendar
calendar: env gen_spp_cal.py
	. $(VENV_DIR)/bin/activate

.PHONY: env-test
env-test: requirements-test.txt $(VENV_DIR)
	. $(VENV_DIR)/bin/activate
	pip3 install -r $<

.PHONY: test
test: env-test
	. $(VENV_DIR)/bin/activate
	python3 -m pytest $(PYTEST_OPTIONS)

.PHONY: clean
clean:
	rm -rf $(VENV_DIR)

.PHONY: docker
docker: $(SRC) Dockerfile docker-compose.yaml
	docker-compose build
