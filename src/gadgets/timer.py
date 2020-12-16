from datetime import datetime, timedelta, timezone
from models.race import Race
import logging

# ------------------------------------------------------------

class Timer:
    logger = logging.Logger("racetime-obs")
    enabled: bool = False
    source_name = ""
    timer_text = ""
    use_podium_colors = False
    pre_color = 0xFFFFFF
    racing_color = 0xFFFFFF
    first_color = 0xFF0000
    second_color = 0x00FF00
    third_color = 0x0000FF
    finished_color = 0xFFFFFF
    cancel_dq_color = 0xFF0000

    def get_timer_text(self, race: Race, full_name: str):
        entrant = race.get_entrant_by_name(full_name)
        color = self.racing_color
        time = "--:--:--.-"
        if race.status.value == "open" or race.status.value == "invitational":
            time = self.timer_to_str(race.start_delay)
            color = self.pre_color
        elif race.status.value == "cancelled":
            color = self.cancel_dq_color
        elif entrant is not None:
            if entrant.finish_time is not None:
                time = self.timer_to_str(entrant.finish_time)
                color = self.get_color(entrant.place)
            elif entrant.status.value == "dnf" or entrant.status.value == "dq":
                color = self.cancel_dq_color
            elif race.started_at is not None:
                timer = datetime.now(timezone.utc) - race.started_at
                time = self.timer_to_str(timer)
        elif race.status.value == "finished":
            # race is finished and our user is not an entrant
            time = self.timer_to_str(race.ended_at - race.started_at)
        elif race.started_at is not None:
            timer = datetime.now(timezone.utc) - race.started_at
            time = self.timer_to_str(timer)
        else:
            return
        if not self.use_podium_colors:
            color = None
        return color, time


    def get_color(self, place: int) -> int:
        if place == 1:
            return self.first_color
        elif place == 2:
            return self.second_color
        elif place == 3:
            return self.third_color
        else:
            return self.finished_color


    @staticmethod
    def timer_to_str(timer: timedelta) -> str:
        if timer.total_seconds() < 0.0:
            return "-0:00:{:04.1f}".format(timer.total_seconds() * -1.0)
        else:
            return str(timer)[:9]
