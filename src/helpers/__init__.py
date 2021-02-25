from datetime import timedelta


def timer_to_str(timer: timedelta) -> str:
    if timer.total_seconds() < 0.0:
        timer = timer * -1.0
        return "-" + str(timer)[:9]
    return str(timer)[:9]
