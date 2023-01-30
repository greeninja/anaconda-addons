import logging
import re

from simpleline.render.prompt import Prompt
from simpleline.render.screen import InputState
from simpleline.render.containers import ListColumnContainer
from simpleline.render.widgets import CheckboxWidget, EntryWidget

from pyanaconda.core.constants import PASSWORD_POLICY_ROOT
from pyanaconda.ui.tui.spokes import NormalTUISpoke
from pyanaconda.ui.common import FirstbootSpokeMixIn
# Simpleline's dialog configured for use in Anaconda
from pyanaconda.ui.tui.tuiobject import Dialog, PasswordDialog

# the path to addons is in sys.path so we can import things from org_fedora_hello_world
from org_rh_consulting_user.categories.user import ConsultingUserCategory
from org_rh_consulting_user.constants import CONSULTING_USER

log = logging.getLogger(__name__)

__all__ = ["UserSpoke", "UserEditSpoke"]


def _(x): return x
def N_(x): return x


class UserSpoke(FirstbootSpokeMixIn, NormalTUISpoke):
    category = ConsultingUserCategory

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = N_("Consulting User")
        self._consulting_user_module = CONSULTING_USER.get_proxy()
        self._container = None
        self._tick = False
        self._lines = ""

    def initialize(self):
        super().initialize()

    def setup(self, args=None):
        super().setup(args)
        self._tick = self._consulting_user_module.Tick
        self._line = self._consulting_user_module.Lines
        return True

    def refresh(self, args=None):
        super().refresh(args)
        self._container = ListColumnContainer(
            columns=1
        )
        self._container.add(
            CheckboxWidget(
                title="Tick",
                completed=self._tick
            ),
            callback=self._change_tick
        )
        self._container.add(
            EntryWidget(
                title="User Text",
                value="".join(self._lines)
            ),
            callback=self._change_lines
        )

        self.window.add_with_separator(self._container)

    def apply(self):
        self._consulting_user_module.SetTick(self._tick)
        self._consulting_user_module.SetLines(self._lines)

    def execute(self):
        pass

    @property
    def completed(self):
        return bool(self._consulting_user_module.Lines)

    @property
    def status(self):
        lines = self._consulting_user_module.Lines

        if not lines:
            return _("No text set")

        reverse = self._consulting_user_module.Tick

        if reverse:
            return _("Text set with {} lines to tick").format(len(lines))
        else:
            return _("Text set with {} lines").format(len(lines))

    def input(self, args, key):
        if self._container.process_user_input(key):
            return InputState.PROCESSED_AND_REDRAW

        if key.lower() == Prompt.CONTINUE:
            self.apply()
            self.execute()
            return InputState.PROCESSED_AND_CLOSE

        return super().input(args, key)

    def _change_tick(self, data):
        self._tick = not self._tick

    def _change_lines(self, data):
        dialog = Dialog("Lines")
        result = dialog.run()
        self._lines = result.splitlines(True)
