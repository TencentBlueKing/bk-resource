# -*- coding: utf-8 -*-
"""Collections for component client"""

from blueking.component.apis.bk_login import CollectionsBkLogin
from blueking.component.apis.bk_paas import CollectionsBkPaas

# Available components
AVAILABLE_COLLECTIONS = {
    "bk_login": CollectionsBkLogin,
    "bk_paas": CollectionsBkPaas,
}
