# -*- coding: utf-8 -*-

DATABASES = {
    "default": {
        "ENGINE": "{{ cookiecutter.db_engine }}",
        "NAME": "{{ cookiecutter.db_name }}",
        "USER": "{{ cookiecutter.db_user }}",
        "PASSWORD": "",
        "HOST": "{{ cookiecutter.db_host }}",
        "PORT": "{{ cookiecutter.db_port }}",
        "CONN_MAX_AGE": 9,
        "TEST": {"NAME": "test_{{ cookiecutter.db_name }}", "CHARSET": "utf8", "COLLATION": "utf8_general_ci"},
    },
}
