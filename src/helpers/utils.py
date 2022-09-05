import datetime
import contextlib

async def time_converter(time: str):
    with contextlib.suppress(ValueError):
        dur = int(time)
        return dur*60
    day = 24
    hour = 60
    minute = 60
    second = 1

    unit = 1
    try:
        duration = int(time[:-1])
    except ValueError:
        return 300

    if time[-1] == 'w':
        week = 7
        unit *= week * day * hour * minute * second
    elif time[-1] == 'd':
        unit *= day * hour * minute * second
    elif time[-1] == 'h':
        unit *= hour * minute * second
    elif time[-1] == 'm':
        unit *= minute * second
    elif time[-1] == 's':
        unit *= second
    else:
        return 300

    return duration * unit

async def time_formatter(obj):
    timestamp = datetime.datetime.timestamp(obj)
    return f'<t:{round(timestamp)}:R>'


async def grammar(amt: float, name):
    return name if amt == 1 else f'{name}s'
