# Copyright (C) JackTEK 2018-2020
# -------------------------------

# =====================
# Import PATH libraries
# =====================
# ------------
# Type imports
# ------------
from typing import Any, Iterable, List, Optional, Union


# --------------------
# Builtin dependencies
# --------------------
from datetime import datetime

# ------------------------
# Third-party dependencies
# ------------------------
from flask import jsonify
from psutil import boot_time, cpu_freq, cpu_percent, disk_partitions, disk_usage, sensors_temperatures, swap_memory, virtual_memory

# -------------------------
# Local extension libraries
# -------------------------
from util import console
from util.blueprints import Core, CPU, Disk, RAM, Swap
from util.constants import stats


def respond(code: Optional[int] = 200,
            msg: Optional[str] = "OK",
            **extras: dict):
    """Responds with a JSON payload."""

    return jsonify(dict(code=code,message=msg,**extras)), code


def compile_stats():
    """Compiles statistics about the Raspberry Pi and reports it back as a Statistics object."""

    _ = swap_memory()
    stats.swap = Swap(total=_.total,
                      used=_.used)

    _ = virtual_memory()
    stats.ram = RAM(total=_.total,
                    used=_.used,
                    available=_.available)

    stats.disks = []
    for index, disk in enumerate(disk_partitions()):
        _ = disk_usage(path=disk.mountpoint)
        stats.disks.append(Disk(total=_.total,
                                used=_.used,
                                id=index,
                                path=disk.mountpoint))

    stats.cores = []
    for core in cpu_percent(percpu=True):
        stats.cores.append(Core(used=core))

    _frequencies = cpu_freq(percpu=True)
    for index, core in enumerate(_frequencies):
        stats.cores[index].frequency = core.current * 1000 ** 2
        stats.cores[index].id = index

    stats.uptime = time_since(since=datetime.fromtimestamp(boot_time()),
                              pretty=True,
                              ms=False,
                              granularity=7,
                              skip_empty=True)

    try:
        _temp = sensors_temperatures()["cpu-thermal"][0].current
    
    except:
        _temp = "???"

    stats.cpu = CPU(max_clock=max(core.max * 1000 ** 2 for core in _frequencies),
                    min_clock=min(core.min * 1000 ** 2 for core in _frequencies),
                    cores=len(stats.cores),
                    temp=_temp)

def time_since(seconds: int = None,
               since: datetime = None,
               pretty: Optional[bool] = False,
               granularity: Optional[int] = 2,
               skip_empty: Optional[bool] = False,
               ms: Optional[bool] = True) -> Union[dict, str]:
    """Calculates the time in each unit of time.
    
    If seconds is passed, then the values we are finding are of the duration of those seconds.
    If since is passed, then we're finding the values of the seconds between now and the provided datetime.
    If both are provided, since takes priority.

    This normally returns a dictionary in the form::
        {
            "unit": number
        }
        
    However, if the pretty kwarg is provided as True, it will be turned into a more human-readable string that looks something like::
        1 year, 1 month, 1 week, 1 day, 1 hour, 1 minute and 1 second
        
    Granularity refers to the accuracy of the result. This function is accurate from the year to the millisecond.
    Therefore a granularity of 8 will return a result accurate to a millisecond, a granularity of 1 will return a result accurate to the year.
    
    If you don't wish to see values such as 0 years etc. in your result, skip_empty should be parsed as True rather than False.
    This also has an impact on accuracy, if the empties are skipped, the granularity range is decreased.
    
    If you don't want milliseconds to be included in the result, pass ms as False.

    [Note]: If the granularity is higher than the granularity range, the issue is silently ignored and the entire result is returned."""

    result = []
    seconds = (datetime.utcnow() - since).total_seconds() if since else seconds

    for name, count in (("years", 60 ** 2 * 24 * 365), 
                        ("months", 60 ** 2 * 24 * 30), 
                        ("weeks", 60 ** 2 * 24 * 7), 
                        ("days", 60 ** 2 * 24), 
                        ("hours", 60 ** 2), 
                        ("minutes", 60), 
                        ("seconds", 1),
                        ("milliseconds", 1 / 1000)):
        if name == "milliseconds" and not ms:
            continue

        value = seconds // count

        if skip_empty and value == 0:
            continue

        seconds -= value * count

        if value == 1 and pretty:
            name = name.rstrip("s")
        
        result.append((round(number=value), name))

    if pretty:
        return human_list(values=[f"{value} {name}" for value, name in result[:granularity]])

    return {name: value for value, name in result[:granularity]}

def human_list(values: Any) -> str:
    """Returns a grammatically correct list.
    
    Usually, lists simply use commas to separate every item, however, English grammar states that the last item should have and instead of a comma."""

    if len(values) == 1:
        return values[0]

    return ", ".join(values[:-1]) + f" and {values[-1]}"

def split_list(iterable: Iterable,
               size: Optional[int] = 5) -> List[list]:
    """Takes an iterable and splits it into lists of its elements.
    
    The size of each sub-list depends on the provided size argument."""

    for i in range(0, len(iterable), size):  
        yield iterable[i:i + size] 

def bytes_4_humans(count: int) -> str:
    """Returns a human friendly interpretation of bytes."""

    # Bytes
    if 1024 > count >= 1:
        return f"{round(count, 2)} B"

    # Kilobytes
    if 1024 > count / 1024 >= 1:
        return f"{round(count / 1024, 2)} KB"

    # Megabytes
    if 1024 > count / 1024 ** 2 >= 1:
        return f"{round(count / 1024 ** 2, 2)} MB"

    # Gigabytes
    if 1024 > count / 1024 ** 3 >= 1:
        return f"{round(count / 1024 ** 3, 2)} GB"

    # Terabytes
    if 1024 > count / 1024 ** 4 >= 1:
        return f"{round(count / 1024 ** 4, 2)} TB"

    # Return in Petabytes if all else fails
    return f"{round(count / 1024 ** 5, 2)} PB"

def hertz_4_humans(count: int) -> str:
    """Returns a human friendly interpretation of hertz."""

    # Hertz
    if 1000 > count >= 1:
        return f"{round(count, 2)} Hz"

    # Kilohertz
    if 1000 > count / 1000 >= 1:
        return f"{round(count / 1000, 2)} KHz"

    # Megahertz
    if 1000 > count / 1000 ** 2 >= 1:
        return f"{round(count / 1000 ** 2, 2)} MHz"

    # Gigahertz
    if 1000 > count / 1000 ** 3 >= 1:
        return f"{round(count / 1000 ** 3, 2)} GHz"

    # Return in Teraahertz if all else fails
    return f"{round(count / 1000 ** 4, 2)} THz"