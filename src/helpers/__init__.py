from datetime import timedelta


def timer_to_str(timer: timedelta, decimals: bool = True) -> str:
    substring = 9
    if not decimals:
        substring = 7
    if timer.total_seconds() < 0.0:
        timer = timer * -1.0
        return "-" + str(timer)[:substring]
    return str(timer)[:substring]
