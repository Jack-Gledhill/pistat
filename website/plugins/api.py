# Copyright (C) JackTEK 2018-2020
# -------------------------------

# ========================
# Import PATH dependencies
# ========================
# --------------------
# Builtin dependencies
# --------------------
from datetime import datetime

# ------------------------
# Third-party dependencies
# ------------------------
from attrdict import AttrDict
from flask import make_response, redirect, request

# -------------------------
# Local extension libraries
# -------------------------
import util.utilities as utils

from util.constants import app, config


BASE = "/api"

@app.route(rule=BASE + "/authenticate",
           methods=["POST"])
def authenticate():
    """Determines whether the appropriate username and password was provided."""

    json = request.json

    if not json:
        return utils.respond(code=422,
                             msg="Missing JSON data.")

    username = json.get("username")
    password = json.get("password")

    if None in (username, password):
        return utils.respond(code=422,
                             msg="Missing JSON data.")

    if username == config.login.username and password == config.login.password:
        return utils.respond(msg="Correct login credentials.",
                             token=config.login.token)

    return utils.respond(code=403,
                         msg="Incorrect login credentials.")

@app.route(rule=BASE + "/logout")
def logout():
    """Logs the user out of their account and sends them to the login screen.
    
    If they're not logged in, sends them to the login screen anyway."""

    res = make_response(redirect(location="/login",
                                 code=303))

    res.set_cookie(key="_auth_token",
                   expires=datetime(year=2000,
                                    month=1,
                                    day=1,
                                    hour=0,
                                    minute=0,
                                    second=1))

    return res