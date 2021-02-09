import logging
from datetime import timedelta

from models.race import Race
from helpers import timer_to_str


class Qualifier:
    logger: logging.Logger = logging.Logger("racetime-obs")
    enabled = False
    qualifier_cutoff = 3
    par_source = ""
    score_source = ""
    par_text = " "
    entrant_score = " "

    def update_qualifier_text(self, race: Race, full_name: str):
        if not self.is_enabled():
            return
        entrant = race.get_entrant_by_name(full_name)
        self.logger.debug(entrant)

        self.par_text = " "
        self.entrant_score = " "
        if race.entrants_count_finished >= self.qualifier_cutoff:
            par_time = self.calculate_par_time(race)
            self.logger.debug(par_time)
            self.par_text = timer_to_str(par_time)

            if entrant and entrant.finish_time is not None:
                entrant_score = min(2 - (entrant.finish_time / par_time), 1.05)
                self.entrant_score = "{:04.2f}".format(
                    entrant_score)
            self.logger.debug(self.entrant_score)

    def calculate_par_time(self, race: Race) -> timedelta:
        par_time = timedelta(microseconds=0)
        for i in range(1, self.qualifier_cutoff + 1):
            if race.get_entrant_by_place(i).finish_time is None:
                self.logger.error("error: qualifier finish time is None")
                return
            self.logger.debug(
                f"finish time for rank {i} is "
                f"{race.get_entrant_by_place(i).finish_time}"
            )
            par_time += race.get_entrant_by_place(i).finish_time
        par_time = par_time / self.qualifier_cutoff
        return par_time

    def is_enabled(self) -> bool:
        return (
            self.enabled and self.par_source != "" and self.score_source != ""
        )

    def update_qualifier_text_preview(self):
        self.par_text = "1:23:45.6"
        self.entrant_score = "0.69"
