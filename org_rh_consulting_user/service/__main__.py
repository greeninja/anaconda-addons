from pyanaconda.modules.common import init
init()  # must be called before importing the service code

from org_rh_consulting_user.service.user import ConsultingUser
service = ConsultingUser()
service.run()