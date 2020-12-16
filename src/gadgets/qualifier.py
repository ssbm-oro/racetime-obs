import websockets
from websockets.client import WebSocketClientProtocol
from datetime import timedelta
from models.race import Race
import websockets
import logging

class Qualifier:
    logger = logging.Logger("racetime-obs")
    enabled = False
    qualifier_cutoff = 3
    qualifier_par_source = ""
    qualifier_score_source = ""
    qualifier_par_text = " "
    entrant_score = " "

    def update_qualifier_text(self, race: Race, full_name: str):
        if not self.enabled:
            return
        entrant = race.get_entrant_by_name(full_name)
        self.logger.debug(entrant)

        self.qualifier_par_text = " "
        entrant_score = " "
        if race.entrants_count_finished >= self.qualifier_cutoff:
            par_time = timedelta(microseconds=0)
            for i in range(1, self.qualifier_cutoff + 1):
                if race.get_entrant_by_place(i).finish_time is None:
                    self.logger.error("error: qualifier finish time is None")
                    return
                self.logger.debug(
                    f"finish time for rank {i} is {race.get_entrant_by_place(i).finish_time}")
                par_time += race.get_entrant_by_place(i).finish_time
            par_time = par_time / self.qualifier_cutoff
            self.logger.debug(par_time)
            self.qualifier_par_text = self.timer_to_str(par_time)

            if entrant and entrant.finish_time is not None:
                entrant_score = str(2 - (entrant.finish_time / par_time))[:4]
            self.logger.debug(entrant_score)