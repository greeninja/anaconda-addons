from pyanaconda.ui.categories import SpokeCategory

__all__ = ["ConsultingUserCategory"]


def _(x): return x


class ConsultingUserCategory(SpokeCategory):

    @staticmethod
    def get_title():
        return _("Consulting User")

    @staticmethod
    def get_sort_order():
        return 0
