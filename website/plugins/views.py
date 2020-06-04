# Copyright (C) JackTEK 2018-2020
# -------------------------------

# ========================
# Import PATH dependencies
# ========================
# ------------------------
# Third-party dependencies
# ------------------------
from attrdict import AttrDict
from flask import render_template, redirect, request

# -------------------------
# Local extension libraries
# -------------------------
import util.constants as constants
import util.utilities as utils

from util.constants import app, config


BASE = "/"

@app.route(rule=BASE)
def index_page():
    """Shows an overview of the Pi."""

    if request.cookies.get("_auth_token") != config.login.token:
        return redirect(location="/login")

    return render_template(template_name_or_list="index.html")

@app.route(rule=BASE + "/cpu")
def cpu_page():
    """Shows CPU information."""

    if request.cookies.get("_auth_token") != config.login.token:
        return redirect(location="/login")

    return render_template(template_name_or_list="cpu.html")

@app.route(rule=BASE + "/mem")
def mem_page():
    """Shows RAM + swap info."""

    if request.cookies.get("_auth_token") != config.login.token:
        return redirect(location="/login")

    return render_template(template_name_or_list="mem.html")

@app.route(rule=BASE + "/disk")
def disk_page():
    """Shows disk usage info."""

    if request.cookies.get("_auth_token") != config.login.token:
        return redirect(location="/login")

    return render_template(template_name_or_list="disk.html")

@app.route(rule=BASE + "login")
def login_page():
    """This displays the login page."""

    if request.cookies.get("_auth_token") == config.login.token:
        return redirect(location="/")

    return render_template(template_name_or_list="login.html")