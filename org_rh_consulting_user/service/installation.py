import logging
from os.path import normpath, join as joinpath

from pyanaconda.modules.common.task import Task

from org_rh_consulting_user.constants import CONSULTING_USER_FILE_PATH

log = logging.getLogger(__name__)


class ConsultingUserConfigurationTask(Task):
    @property
    def name(self):
        return "Configure Consulting User"

    def run(self):
        log.info("Running configuration task.")


class ConsultingUserInstallationTask(Task):

    def __init__(self, sysroot, tick, lines):
        super().__init__()
        self._sysroot = sysroot
        self._tick = tick
        self._lines = lines

    @property
    def name(self):
        return "Install Consulting User"

    def run(self):
        log.info("Running installation task.")
        user_file_path = normpath(
            joinpath(self._sysroot, CONSULTING_USER_FILE_PATH))
        log.debug("Writing consulting user file to: %s", user_file_path)

        # Last line could be missing the trailing line ending if it came from GUI.
        # That breaks the reversed output, so make sure it is there.
        if self._lines and not self._lines[-1].endswith("\n"):
            self._lines[-1] += "\n"

        iterator = reversed(self._lines) if self._tick else self._lines
        with open(user_file_path, "w") as user_file:
            for line in iterator:
                user_file.write(line)
