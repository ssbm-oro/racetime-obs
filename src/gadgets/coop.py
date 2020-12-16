from datetime import datetime, timedelta, timezone
from models.race import Entrant, Race
import logging
from .timer import Timer

class Coop:
    logger = logging.Logger("racetime-obs")
    enabled = False
    partner = None
    opponent2 = None
    opponent1 = None
    source_name = None
    label_source_name = None
    text = " "
    label_text = "Race still in progress"
    
    def update_coop_text(self, race: Race, full_name):
        entrant = race.get_entrant_by_name(full_name)
        partner = race.get_entrant_by_name(self.partner)
        opponent1 = race.get_entrant_by_name(self.opponent1)
        opponent2 = race.get_entrant_by_name(self.opponent2)

        if not self.enabled or entrant is None or partner is None or opponent1 is None or opponent2 is None:
            return

        self.logger.debug(f"use_coop: {self.enabled}")
        self.logger.debug(f"entrant name: {full_name}, entrant: {entrant}")
        self.logger.debug(f"entrant name: {self.partner}, entrant: {partner}")
        self.logger.debug(f"entrant name: {self.opponent1}, entrant: {opponent1}")
        self.logger.debug(f"entrant name: {self.opponent2}, entrant: {opponent2}")

        our_total, opponent_total = self.get_coop_times(
            entrant, partner, opponent1, opponent2)
        if race.entrants_count_finished == 2:
            if our_total is not None:
                label_text = "We won!"
                text = self.timer_to_str(our_total / 2)
            elif opponent_total is not None:
                label_text = "They won. :("
                text = self.timer_to_str(opponent_total / 2)
        if race.entrants_count_finished == 3:
            current_timer = datetime.now(timezone.utc) - race.started_at
            if not entrant.finish_time:
                coop_label_text, coop_text = self.get_coop_text(
                    "I need ", partner, opponent_total, current_timer)
            elif not partner.finish_time:
                prefix = partner.user.name + " needs to finish before"
                coop_label_text, coop_text = self.get_coop_text(
                    prefix, entrant, opponent1, opponent2, current_timer)
            elif not opponent1.finish_time:
                prefix = opponent1.user.name + " needs "
                coop_label_text, coop_text = self.get_coop_text(
                    prefix, opponent2, entrant, partner, current_timer)
            elif not opponent2.finish_time:
                prefix = opponent2.user.name + " needs "
                coop_label_text, coop_text = self.get_coop_text(
                    prefix, opponent1, entrant, partner, current_timer)
        if race.entrants_count_finished == 4:
            our_total = entrant.finish_time + partner.finish_time
            opponent_total = opponent1.finish_time + opponent2.finish_time
            if our_total < opponent_total:
                coop_label_text = "We won!!! Average time:"
                coop_text = Timer.timer_to_str(our_total / 2)
            else:
                coop_label_text = "Opponents won, average time:"
                coop_text = Timer.timer_to_str(opponent_total / 2)


    def get_coop_text(label_text_start: str, finished_partner: Entrant, finished1: Entrant, finished2: Entrant, current_timer: timedelta):
        finished_team_total = finished1.finish_time + finished2.finish_time
        time_to_beat = finished_team_total - finished_partner.finish_time
        if time_to_beat < current_timer:
            coop_text = Timer.timer_to_str(time_to_beat)
            coop_label_text = label_text_start + "to finish before"
        else:
            coop_label_text = finished1.user.name + finished2.user.name + " won"
            coop_text = Timer.timer_to_str(finished_team_total / 2)
        return coop_label_text, coop_text


    def get_coop_times(self, entrant, partner, opponent1, opponent2):
        our_total = None
        opponent_total = None
        if entrant.finish_time and partner.finish_time:
            our_total = entrant.finish_time + partner.finish_time
            self.logger.debug(f"calculated our average is {our_total / 2}")
        else:
            self.logger.debug(f"we haven't finished yet")
        if opponent1.finish_time and opponent2.finish_time:
            opponent_total = opponent1.finish_time + opponent2.finish_time
            self.logger.debug(
                f"calculated our opponent's average is {opponent_total / 2}")
        else:
            self.logger.debug(f"our opponents haven't finished")
        return our_total, opponent_total