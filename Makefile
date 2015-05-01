.PHONY: clean-pyc test serve
FLAGS='--datastore_path=./db --skip_sdk_update_check'
PORT=8080
ADMIN_PORT=8000
HOST='0.0.0.0'

all: clean-pyc test

serve:
	dev_appserver.py  $(FLAGS) --port $(PORT) --host $(HOST) \
		--admin_host $(HOST) --admin_port $(ADMIN_PORT) .

test:
	nosetests --with-gae 

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
