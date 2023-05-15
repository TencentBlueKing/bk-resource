# -*- coding: utf-8 -*-

from api.constants import APIProvider
from api.utils import get_endpoint

# User Manage
USER_MANAGE_URL = get_endpoint("usermanage", APIProvider.ESB)
