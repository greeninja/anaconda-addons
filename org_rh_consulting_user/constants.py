from dasbus.identifier import DBusServiceIdentifier
from pyanaconda.core.dbus import DBus
from pyanaconda.modules.common.constants.namespaces import ADDONS_NAMESPACE

CONSULTING_USER_NAMESPACE = (*ADDONS_NAMESPACE, "ConsultingUser")

CONSULTING_USER = DBusServiceIdentifier(
    namespace=CONSULTING_USER_NAMESPACE,
    message_bus=DBus
)

CONSULTING_USER_FILE_PATH = "root/consulting_user.txt"
