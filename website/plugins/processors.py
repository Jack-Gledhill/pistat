# Copyright (C) JackTEK 2018-2020
# -------------------------------

# =====================
# Import PATH libraries
# =====================
# -------------------------
# Local extension libraries
# -------------------------
import util.constants as constants
import util.utilities as utils

from util.constants import app, const


@app.context_processor
def inject_globals():
    """This handles the injection of information we want to be available to every page."""

    utils.compile_stats()

    return dict(version=dict(const.version),
                stats=constants.stats,
                split_list=utils.split_list,
                bytes_4_humans=utils.bytes_4_humans,
                hertz_4_humans=utils.hertz_4_humans)