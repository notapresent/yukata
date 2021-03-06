
APPCFG          = appcfg.py
APP_ID          = (YOUR-APP-ID)
EMAIL           = (YOUR-EMAIL)
SERVE_PORT      = 8080
SERVE_ADDRESS   = 0.0.0.0
DATASTORE_PATH  = ./datastore.sqlite3

help:
	@echo "AppEngine make file. Options are:"
	@echo " test"
	@echo "    Runs the test suite"
	@echo "    (Usage: make test [dir=directory])"
	@echo " coverage"
	@echo "    Runs the test suite and prints a coverage report"
	@echo " update (or deploy)"
	@echo "    Updates (deploys) the current project"
	@echo " rollback"
	@echo "    Rolls back an unclosed update to the application"
	@echo " serve"
	@echo "    Runs the development web server"
	@echo " console"
	@echo "    Opens a development console to your remote application"
	@echo "    (Only works if you've enabled the /_ah/remote_api URL)"
	@echo " project"
	@echo "    Creates a new project template"
	@echo "    (Usage: make project name=yourprojectname)"
	@echo " download-data"
	@echo "    Downloads your data from App Engine"
	@echo "    (Usage: make download-data filename=downloaded-data.out)"
	@echo " update-indexes"
	@echo "    Updates App Engine with any indexes in index.yaml not already pushed"
	@echo " vacuum-indexes"
	@echo "    Deletes any indexes existing on App Engine but not in your index.yaml file"

test:
	@nosetests --with-gae $(dir)

coverage:
	@nosetests --with-gae --with-coverage $(dir)

deploy:
	$(APPCFG) -e $(EMAIL) update .

update:
	$(APPCFG) -e $(EMAIL) update .

rollback:
	$(APPCFG) -e $(EMAIL) rollback .

serve:
	@dev_appserver.py \
	--host $(SERVE_ADDRESS) \
	--admin_host $(SERVE_ADDRESS) \
	--port $(SERVE_PORT) \
	--datastore_path=$(DATASTORE_PATH) \
	.

console:
	@remote_api_shell.py -s $(APP_ID).appspot.com

localconsole:
	@remote_api_shell.py -s localhost:$(SERVE_PORT)

update-indexes:
	$(APPCFG) update_indexes .

vacuum-indexes:
	$(APPCFG) vacuum_indexes .

download-data:
ifndef filename
	@echo "Invalid usage. Try 'make help' for more details."
else
	$(APPCFG) download_data \
	--application=$(APP_ID) \
	--email=$(EMAIL) \
	--url=http://$(APP_ID).appspot.com/_ah/remote_api \
	--filename=$(filename)
endif

project:
ifndef name
	@echo "Invalid usage. Try 'make help' for more details."
else
	@mkdir scripts
	@mkdir $(name)
	@mkdir $(name)/handlers
	@mkdir $(name)/handlers/tests
	@mkdir $(name)/library
	@mkdir $(name)/library/tests
	@mkdir $(name)/models
	@mkdir $(name)/models/tests
	@mkdir $(name)/media
	@mkdir $(name)/templates
	@touch $(name)/__init__.py
	@touch $(name)/handlers/__init__.py
	@touch $(name)/handlers/tests/__init__.py
	@touch $(name)/library/__init__.py
	@touch $(name)/library/tests/__init__.py
	@touch $(name)/models/__init__.py
	@touch $(name)/models/tests/__init__.py
	@curl --silent -L http://appengine.google.com/favicon.ico > $(name)/media/favicon.ico
	@echo "User-agent: *\nDisallow: " > $(name)/robots.txt
	@echo "application: $(name)" >> app.yaml
	@echo "version: 1" >> app.yaml
	@echo "runtime: python" >> app.yaml
	@echo "api_version: 1" >> app.yaml
	@echo "" >> app.yaml
	@echo "builtins:" >> app.yaml
	@echo "- remote_api: on" >> app.yaml
	@echo "- datastore_admin: on" >> app.yaml
	@echo "- appstats: on" >> app.yaml
	@echo "- deferred: on" >> app.yaml
	@echo "" >> app.yaml
	@echo "inbound_services:" >> app.yaml
	@echo "- mail" >> app.yaml
	@echo "- xmpp_message" >> app.yaml
	@echo "" >> app.yaml
	@echo "handlers:" >> app.yaml
	@echo "- url: /favicon.ico" >> app.yaml
	@echo "  static_files: $(name)/media/favicon.ico" >> app.yaml
	@echo "  upload: $(name)/media/favicon.ico" >> app.yaml
	@echo "" >> app.yaml
	@echo "- url: /robots.txt" >> app.yaml
	@echo "  static_files: $(name)/robots.txt" >> app.yaml
	@echo "  upload: $(name)/robots.txt" >> app.yaml
	@echo "queue:" >> queue.yaml
	@echo "- name: default" >> queue.yaml
	@echo "  rate: 5/s" >> queue.yaml
	@echo "  bucket_size: 5" >> queue.yaml
	@echo "cron:" >> cron.yaml
endif
