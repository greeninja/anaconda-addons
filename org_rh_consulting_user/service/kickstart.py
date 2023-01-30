import logging

from pykickstart.options import KSOptionParser

from pyanaconda.core.kickstart import VERSION, KickstartSpecification
from pyanaconda.core.kickstart.addon import AddonData

log = logging.getLogger(__name__)


class ConsultingUserData(AddonData):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.tick = False

    def handle_header(self, args, line_number=None):
        op = KSOptionParser(
            prog="%addon org_rh_consulting_user",
            version=VERSION,
            description="Configure the Custom User Addon"
        )

        op.add_argument(
            "--tick",
            action="store_true",
            default=False,
            version=VERSION,
            dest="tick",
            help="Shows that the option was ticked"
        )

        ns = op.parse_args(args=args, lineno=line_number)

        self.tick = ns.tick

    def handle_line(self, line, line_number=None):
        self.lines.append(line)

    def __str__(self):
        section = "\n%addon org_rh_consulting_user"

        if self.tick:
            section += " --reverse"

        section += "\n"

        for line in self.lines:
            section += line

        if not section.endswith("\n"):
            section += "\n"

        section += "%end\n"
        return section


class ConsultingUserKickstartSpecification(KickstartSpecification):
    addons = {
        "org_rh_consulting_user": ConsultingUserData
    }
