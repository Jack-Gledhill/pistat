# Copyright (C) JackTEK 2018-2020
# -------------------------------

# =====================
# Import PATH libraries
# =====================
# ------------
# Type imports
# ------------
from typing import Optional


# --------------------
# Builtin dependencies
# --------------------
from datetime import datetime
from json import loads

# ------------------------
# Third-party dependencies
# ------------------------
from attrdict import AttrDict

# -------------------------
# Local extension libraries
# -------------------------
from custos import blueprint


class Swap(blueprint):
    def __init__(self,
                 total: int,
                 used: int):
        self.total = total
        self.used = used

    @property
    def free(self) -> int:
        return self.total - self.used

    @property
    def percent(self) -> float:
        return self.used / self.total * 100


class Disk(blueprint):
    def __init__(self,
                 total: int,
                 used: int,
                 id: int,
                 path: str):
        self.total = total
        self.used = used
        self.id = id
        self.path = path

    @property
    def free(self) -> int:
        return self.total - self.used

    @property
    def percent(self) -> float:
        return self.used / self.total * 100


class RAM(blueprint):
    def __init__(self,
                 total: int,
                 used: int,
                 available: int):
        self.total = total
        self.used = used
        self.available = available

    @property
    def percent(self) -> float:
        return self.used / self.total * 100


class Core(blueprint):
    def __init__(self,
                 used: int,
                 frequency: Optional[float] = None,
                 id: Optional[int] = None):
        self.used = used
        self.frequency = frequency
        self.id = id


class CPU(blueprint):
    def __init__(self,
                 max_clock: int,
                 min_clock: int,
                 cores: int,
                 temp: float):
        self.max = max_clock
        self.min = min_clock
        self.cores = cores
        self.temp = temp


class IPs(blueprint):
    def __init__(self,
                 local: str,
                 public: str):
        self.local = local
        self.public = public


class Statistics(blueprint):
    def __init__(self,
                 **data: dict):
        self.swap = data.pop("swap", None)
        self.ram = data.pop("ram", None)
        self.cpu = data.pop("cpu", None)

        self.cores = data.pop("cores", [])
        self.disks = data.pop("disks", [])

        self.ips = data.pop("ips", None)
        self.uptime = data.pop("uptime", None)