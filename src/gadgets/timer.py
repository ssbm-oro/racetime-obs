import logging
from datetime import datetime, timedelta, timezone

from models.race import Entrant, Race
from helpers import timer_to_str

# ------------------------------------------------------------


class Timer:
    logger: logging.Logger = None
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
    decimals: bool = True

    def get_timer_text(self, race: Race, full_name: str):
        entrant = race.get_entrant_by_name(full_name)
        color = self.racing_color
        time = "--:--:--.-"

        # default value used if user is not in race and race is running
        #  currently
        color, time = self.get_color_and_text_by_started_at(
            race.started_at, race.status.value, race.ended_at)

        # if race is has not started or cancelled
        color, time = self.get_color_and_text_by_race_status(
            race.status.value, race.start_delay, color, time)

        # value if user is an entrant in this race
        color, time = self.get_color_and_text_by_entrant(
            entrant, race.started_at, color, time)
        if not self.use_podium_colors:
            color = None
        return color, time

    def get_color_and_text_by_race_status(
        self, status_value: str, start_delay: timedelta,
        fallback_color: int = None, fallback_text: str = None
    ):
        if status_value == "open" or status_value == "invitational":
            time = timer_to_str(start_delay * -1.0, self.decimals)
            color = self.pre_color
        elif status_value == "cancelled":
            color = self.cancel_dq_color
            time = "--:--:--.-"
        else:
            return fallback_color, fallback_text
        return color, time

    def get_color_and_text_by_started_at(
        self, started_at: datetime, status_value: str,
        ended_at: datetime = None, fallback_color: int = None,
        fallback_text: str = None
    ):
        if status_value == "finished":
            # race is finished and assume user is not an entrant
            time = timer_to_str(ended_at - started_at, self.decimals)
            color = self.finished_color
        elif started_at is not None:
            timer = datetime.now(timezone.utc) - started_at
            time = timer_to_str(timer, self.decimals)
            color = self.racing_color
        else:
            return fallback_color, fallback_text
        return color, time

    def get_color_and_text_by_entrant(
        self, entrant: Entrant = None, started_at: datetime = None,
        fallback_color: int = None, fallback_text: str = None
    ):
        time = fallback_text
        color = fallback_color
        if entrant is not None:
            if entrant.finish_time is not None:
                time = timer_to_str(entrant.finish_time, self.decimals)
                color = self.get_color_by_place(entrant.place)
            elif entrant.status.value == "dnf" or entrant.status.value == "dq":
                time = "--:--:--.-"
                color = self.cancel_dq_color
            elif started_at is not None:
                timer = datetime.now(timezone.utc) - started_at
                time = timer_to_str(timer, self.decimals)
        return color, time

    def get_color_by_place(self, place: int) -> int:
        if place == 1:
            return self.first_color
        elif place == 2:
            return self.second_color
        elif place == 3:
            return self.third_color
        else:
            return self.finished_color

    def is_enabled(self) -> bool:
        return self.enabled and self.source_name != ""

    def get_timer_text_preview(self):
        return (
            self.racing_color,
            timer_to_str(
                timedelta(hours=1, minutes=23, seconds=45.6),
                self.decimals)
        )
