from datetime import timedelta


def timer_to_str(timer: timedelta) -> str:
    if timer.total_seconds() < 0.0:
        return "-0:00:{:04.1f}".format(timer.total_seconds() * -1.0)
    else:
        return str(timer)[:9]
