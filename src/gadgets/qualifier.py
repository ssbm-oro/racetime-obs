import websockets
from websockets.client import WebSocketClientProtocol
from datetime import timedelta
from gadgets.timer import Timer
from models.race import Race
import websockets
import logging

class Qualifier:
    logger: logging.Logger = logging.Logger("racetime-obs")
    enabled = False
    qualifier_cutoff = 3
    par_source = ""
    score_source = ""
    par_text = " "
    entrant_score = " "

    def update_qualifier_text(self, race: Race, full_name: str):
        self.logger.debug("entered update_qualifier_text")
        if not self.enabled:
            return
        entrant = race.get_entrant_by_name(full_name)
        self.logger.debug(entrant)

        self.par_text = " "
        self.entrant_score = " "
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
            self.par_text = Timer.timer_to_str(par_time)

            if entrant and entrant.finish_time is not None:
                self.entrant_score = "{:04.2f}".format(2 - (entrant.finish_time / par_time))
            self.logger.debug(self.entrant_score)