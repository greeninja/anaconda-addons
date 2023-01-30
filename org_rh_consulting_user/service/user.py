import logging

from pyanaconda.core.configuration.anaconda import conf
from pyanaconda.core.dbus import DBus
from pyanaconda.core.signal import Signal
from pyanaconda.modules.common.base import KickstartService
from pyanaconda.modules.common.containers import TaskContainer

from org_rh_consulting_user.constants import CONSULTING_USER
from org_rh_consulting_user.service.interface import ConsultingUserInterface
from org_rh_consulting_user.service.installation import ConsultingUserConfigurationTask, \
    ConsultingUserInstallationTask
from org_rh_consulting_user.service.kickstart import ConsultingUserKickstartSpecification

log = logging.getLogger(__name__)


class ConsultingUser(KickstartService):
    def __init__(self):
        super().__init__()
        self._tick = False
        self._lines = []

        self.tick_changed = Signal()
        self.lines_changed = Signal()

    def publish(self):
        TaskContainer.set_namespace(CONSULTING_USER.namespace)
        DBus.publish_object(CONSULTING_USER.object_path,
                            ConsultingUserInterface(self))
        DBus.register_service(CONSULTING_USER.service_name)

    @property
    def kickstart_specification(self):
        return ConsultingUserKickstartSpecification

    def process_kickstart(self, data):
        log.debug("Processing kickstart data...")
        self._tick = data.addons.org_rh_consulting_user.tick
        self._lines = data.addons.org_rh_consulting_user.lines

    def setup_kickstart(self, data):
        log.debug("Generating kickstart data...")
        data.addons.org_rh_consulting_user.tick = self._tick
        data.addons.org_rh_consulting_user.lines = self._lines

    @property
    def tick(self):
        return self._tick

    def set_tick(self, tick):
        self._tick = tick
        self.tick_changed.emit()
        log.debug("Tick is set to %s", tick)

    @property
    def lines(self):
        return self._lines

    def set_lines(self, lines):
        self._lines = lines
        self.lines_changed.emit()
        log.debug("Lines is set to %s.", lines)

    def configure_with_tasks(self):
        task = ConsultingUserConfigurationTask()
        return [task]

    def install_with_tasks(self):
        task = ConsultingUserInstallationTask(
            conf.target.system_root,
            self._tick,
            self._lines
        )
        return [task]
