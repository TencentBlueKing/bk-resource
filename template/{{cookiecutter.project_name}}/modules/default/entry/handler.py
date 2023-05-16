# -*- coding: utf-8 -*-


class HealthzHandler(object):
    """
    HealthzHandler
    """

    @classmethod
    def healthz(cls) -> dict:
        result = {"healthy": True}
        return result
