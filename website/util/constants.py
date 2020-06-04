# Copyright (C) JackTEK 2018-2020
# -------------------------------

# =====================
# Import PATH libraries
# =====================
# --------------------
# Builtin dependencies
# --------------------
import socket

from urllib import request

# ------------------------
# Third-party dependencies
# ------------------------
from attrdict import AttrDict
from yaml import safe_load

# -------------------------
# Local extension libraries
# -------------------------
from custos import version

from util.blueprints import IPs, Statistics


config = AttrDict(safe_load(stream=open(file="config.yml")))
const = AttrDict(dict(version=version(**config.version)))

app = None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# credits to https://www.w3resource.com/python-exercises/python-basic-exercise-55.php for this monstrosity
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
stats = Statistics(ips=IPs(local=[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0],
                           public=request.urlopen("https://api.ipify.org").read().decode("utf-8")))