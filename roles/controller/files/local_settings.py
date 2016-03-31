# -*- coding: utf-8 -*-

import os

from django.utils.translation import ugettext_lazy as _

from horizon.utils import secret_key

from openstack_dashboard import exceptions
from openstack_dashboard.settings import HORIZON_CONFIG

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# WEBROOT is the location relative to Webserver root
# should end with a slash.
WEBROOT = '/'
LOGIN_URL='/auth/login/'
LOGOUT_URL='/auth/logout/'
LOGIN_REDIRECT_URL='/'

# LOGIN_REDIRECT_URL can be used as an alternative for
# HORIZON_CONFIG.user_home, if user_home is not set.
# Do not set it to '/home/', as this will cause circular redirect loop
#LOGIN_REDIRECT_URL = WEBROOT

# If horizon is running in production (DEBUG is False), set this
# with the list of host/domain names that the application can serve.
# For more information see:
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
#ALLOWED_HOSTS = ['horizon.example.com', ]
ALLOWED_HOSTS = ['*' ]

# Set SSL proxy settings:
# Pass this header from the proxy after terminating the SSL,
# and don't forget to strip it from the client's request.
# For more information see:
# https://docs.djangoproject.com/en/1.8/ref/settings/#secure-proxy-ssl-header
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# If Horizon is being served through SSL, then uncomment the following two
# settings to better secure the cookies from security exploits
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True

#HORIZON_CONFIG["disable_password_reveal"] = False

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = secret_key.generate_or_read_from_file('/var/lib/openstack-dashboard/secret_key')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
}

OPENSTACK_HOST = "127.0.0.1"
OPENSTACK_KEYSTONE_URL = "http://%s:5000/v2.0" % OPENSTACK_HOST
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "_member_"


# Disable SSL certificate checks (useful for self-signed certificates):
#OPENSTACK_SSL_NO_VERIFY = True

# The CA certificate to use to verify SSL connections
#OPENSTACK_SSL_CACERT = '/path/to/cacert.pem'

OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_group': True,
    'can_edit_project': True,
    'can_edit_domain': True,
    'can_edit_role': True,
}

OPENSTACK_HYPERVISOR_FEATURES = {
    'can_set_mount_point': False,
    'can_set_password': False,
    'requires_keypair': False,
}

OPENSTACK_CINDER_FEATURES = {
    'enable_backup': False,
}

OPENSTACK_NEUTRON_NETWORK = {
    'enable_router': True,
    'enable_quotas': True,
    'enable_ipv6': True,
    'enable_distributed_router': False,
    'enable_ha_router': False,
    'enable_lb': True,
    'enable_firewall': True,
    'enable_vpn': True,
    'enable_fip_topology_check': True,
    'default_ipv4_subnet_pool_label': None,
    'default_ipv6_subnet_pool_label': None,
    'profile_support': None,
    #'profile_support': 'cisco',
    'supported_provider_types': ['*'],
    'supported_vnic_types': ['*'],
}

# The OPENSTACK_HEAT_STACK settings can be used to disable password
# field required while launching the stack.
OPENSTACK_HEAT_STACK = {
    'enable_user_pass': True,
}

# The IMAGE_CUSTOM_PROPERTY_TITLES settings is used to customize the titles for
# image custom property attributes that appear on image detail pages.
IMAGE_CUSTOM_PROPERTY_TITLES = {
    "architecture": _("Architecture"),
    "kernel_id": _("Kernel ID"),
    "ramdisk_id": _("Ramdisk ID"),
    "image_state": _("Euca2ools state"),
    "project_id": _("Project ID"),
    "image_type": _("Image Type"),
}

# The number of objects (Swift containers/objects or images) to display
# on a single page before providing a paging element (a "more" link)
# to paginate results.
API_RESULT_LIMIT = 1000
API_RESULT_PAGE_SIZE = 20

# The size of chunk in bytes for downloading objects from Swift
SWIFT_FILE_TRANSFER_CHUNK_SIZE = 512 * 1024

# Specify a maximum number of items to display in a dropdown.
DROPDOWN_MAX_ITEMS = 30

# The timezone of the server. This should correspond with the timezone
# of your entire OpenStack installation, and hopefully be in UTC.
TIME_ZONE = "UTC"

# The Horizon Policy Enforcement engine uses these values to load per service
# policy rule files. The content of these files should match the files the
# OpenStack services are using to determine role based access control in the
# target installation.

# Path to directory containing policy.json files
#POLICY_FILES_PATH = os.path.join(ROOT_PATH, "conf")

# Map of local copy of service policy files.
# Please insure that your identity policy file matches the one being used on
# your keystone servers. There is an alternate policy file that may be used
# in the Keystone v3 multi-domain case, policy.v3cloudsample.json.
# This file is not included in the Horizon repository by default but can be
# found at
# http://git.openstack.org/cgit/openstack/keystone/tree/etc/ \
# policy.v3cloudsample.json
# Having matching policy files on the Horizon and Keystone servers is essential
# for normal operation. This holds true for all services and their policy files.
#POLICY_FILES = {
#    'identity': 'keystone_policy.json',
#    'compute': 'nova_policy.json',
#    'volume': 'cinder_policy.json',
#    'image': 'glance_policy.json',
#    'orchestration': 'heat_policy.json',
#    'network': 'neutron_policy.json',
#    'telemetry': 'ceilometer_policy.json',
#}

LOGGING = {
    'version': 1,
    # When set to True this will disable all logging except
    # for loggers specified in this configuration dictionary. Note that
    # if nothing is specified here and disable_existing_loggers is True,
    # django.db.backends will still log unless it is disabled explicitly.
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'horizon': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_dashboard': {
            'handlers': ['console'],

            'level': 'DEBUG',
            'propagate': False,
        },
        'novaclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'cinderclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'keystoneclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'glanceclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'neutronclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'heatclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ceilometerclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'swiftclient': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'nose.plugins.manager': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'iso8601': {
            'handlers': ['null'],
        },
        'scss': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

# 'direction' should not be specified for all_tcp/udp/icmp.
# It is specified in the form.
SECURITY_GROUP_RULES = {
    'all_tcp': {
        'name': _('All TCP'),
        'ip_protocol': 'tcp',
        'from_port': '1',
        'to_port': '65535',
    },
    'all_udp': {
        'name': _('All UDP'),
        'ip_protocol': 'udp',
        'from_port': '1',
        'to_port': '65535',
    },
    'all_icmp': {
        'name': _('All ICMP'),
        'ip_protocol': 'icmp',
        'from_port': '-1',
        'to_port': '-1',
    },
    'ssh': {
        'name': 'SSH',
        'ip_protocol': 'tcp',
        'from_port': '22',
        'to_port': '22',
    },
    'smtp': {
        'name': 'SMTP',
        'ip_protocol': 'tcp',
        'from_port': '25',
        'to_port': '25',
    },
    'dns': {
        'name': 'DNS',
        'ip_protocol': 'tcp',
        'from_port': '53',
        'to_port': '53',
    },
    'http': {
        'name': 'HTTP',
        'ip_protocol': 'tcp',
        'from_port': '80',
        'to_port': '80',
    },
    'pop3': {
        'name': 'POP3',
        'ip_protocol': 'tcp',
        'from_port': '110',
        'to_port': '110',
    },
    'imap': {
        'name': 'IMAP',
        'ip_protocol': 'tcp',
        'from_port': '143',
        'to_port': '143',
    },
    'ldap': {
        'name': 'LDAP',
        'ip_protocol': 'tcp',
        'from_port': '389',
        'to_port': '389',
    },
    'https': {
        'name': 'HTTPS',
        'ip_protocol': 'tcp',
        'from_port': '443',
        'to_port': '443',
    },
    'smtps': {
        'name': 'SMTPS',
        'ip_protocol': 'tcp',
        'from_port': '465',
        'to_port': '465',
    },
    'imaps': {
        'name': 'IMAPS',
        'ip_protocol': 'tcp',
        'from_port': '993',
        'to_port': '993',
    },
    'pop3s': {
        'name': 'POP3S',
        'ip_protocol': 'tcp',
        'from_port': '995',
        'to_port': '995',
    },
    'ms_sql': {
        'name': 'MS SQL',
        'ip_protocol': 'tcp',
        'from_port': '1433',
        'to_port': '1433',
    },
    'mysql': {
        'name': 'MYSQL',
        'ip_protocol': 'tcp',
        'from_port': '3306',
        'to_port': '3306',
    },
    'rdp': {
        'name': 'RDP',
        'ip_protocol': 'tcp',
        'from_port': '3389',
        'to_port': '3389',
    },
}

# AngularJS requires some settings to be made available to
# the client side. Some settings are required by in-tree / built-in horizon
# features. These settings must be added to REST_API_REQUIRED_SETTINGS in the
# form of ['SETTING_1','SETTING_2'], etc.
#
# You may remove settings from this list for security purposes, but do so at
# the risk of breaking a built-in horizon feature. These settings are required
# for horizon to function properly. Only remove them if you know what you
# are doing. These settings may in the future be moved to be defined within
# the enabled panel configuration.
# You should not add settings to this list for out of tree extensions.
# See: https://wiki.openstack.org/wiki/Horizon/RESTAPI
REST_API_REQUIRED_SETTINGS = ['OPENSTACK_HYPERVISOR_FEATURES',
                              'LAUNCH_INSTANCE_DEFAULTS']

