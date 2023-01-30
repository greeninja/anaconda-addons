BASEDIR := /usr/share/anaconda/
ADDONDIR := $(BASEDIR)/addons/
SERVICESDIR := $(BASEDIR)/dbus/services/
CONFDIR := $(BASEDIR)/dbus/confs/

_default: install

.PHONY: install
install:
	@echo "*** ERROR ***"
	@echo "*** Choose which addon to install ***"
	@echo "make user / make network"

.PHONY: user
user:
	@echo "*** Building Anaconda Addon"
	@mkdir -p $(ADDONDIR)
	@cp -par org_rh_consulting_user $(ADDONDIR)
	@mkdir -p $(SERVICESDIR)
	@cp -pa data/org_rh_consulting_user/*.service $(SERVICESDIR)
	@mkdir -p $(CONFDIR)
	@cp -pa data/org_rh_consulting_user/*.conf $(CONFDIR)
	@echo "done."
	@echo "In theory - you can now run:"
	@echo "/usr/libexec/anaconda/start-module org_rh_consulting_user.service"