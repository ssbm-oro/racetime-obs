import logging
from datetime import timedelta
from typing import List

from helpers import timer_to_str
import clients.ladder_client as ladder_client
from models.ladder import Racer


class LadderTimer:
    logger: logging.Logger = None
    enabled: bool = False
    source_name = ""
    timer_text = ""
    racer_id: int
    pre_color: int
    racing_color: int
    winner_color: int
    loser_color: int
    ff_color: int
    timer: timedelta
    active_racers: List[Racer]

    def get_timer_text(self):
        return self.racing_color, timer_to_str(self.timer)

    def update_settings(self, racer_name: str):
        racer_id = self.get_racer_id(racer_name)
        if racer_id == 0:
            return False
        else:
            self.racer_id = racer_id
            return True

    def get_racer_id(self, racer_name: str) -> Racer:
        self.update_active_racers()
        for racer in self.active_racers:
            if racer.RacerName == racer_name:
                return racer.racer_id
        return 0

    def update_active_racers(self):
        if self.active_racers is None or self.active_racers == []:
            self.active_racers = ladder_client.get_active_racers()
