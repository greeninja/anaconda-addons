import logging

from dasbus.server.interface import dbus_interface
from dasbus.server.property import emits_properties_changed
from dasbus.typing import *  # pylint: disable=wildcard-import,unused-wildcard-import

from pyanaconda.modules.common.base import KickstartModuleInterface

from org_rh_consulting_user.constants import CONSULTING_USER

log = logging.getLogger(__name__)


@dbus_interface(CONSULTING_USER.interface_name)
class ConsultingUserInterface(KickstartModuleInterface):

    def connect_signals(self):
        super().connect_signals()
        self.watch_property("Tick", self.implementation.tick_changed)
        self.watch_property("Lines", self.implementation.lines_changed)

    @property
    def Tick(self) -> Bool:
        return self.implementation.tick

    @emits_properties_changed
    def SetTick(self, tick: Bool):
        self.implementation.set_tick(tick)

    @property
    def Lines(self) -> List[Str]:
        return self.implementation.lines

    @emits_properties_changed
    def SetLines(self, lines: List[Str]):
        self.implementation.set_lines(lines)
