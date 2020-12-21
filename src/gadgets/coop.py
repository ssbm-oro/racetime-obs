from datetime import datetime, timedelta, timezone
import logging
from helpers import timer_to_str

from models.race import Entrant, Race


class Coop:
    logger: logging.Logger = logging.Logger("racetime-obs")
    enabled = False
    partner = None
    opponent2 = None
    opponent1 = None
    our_time_source = None
    opponent_time_source = None
    our_time_text = " "
    opponent_time_text = " "
    our_time_color: int = 0x000000
    opponent_time_color: int = 0x000000
    winner_color = 0xFF00FF00
    loser_color = 0xFF0000FF
    still_racing_color = 0xFFFFFFFF

    def update_coop_text(self, race: Race, full_name):
        if not self.is_enabled():
            return

        entrant = race.get_entrant_by_name(full_name)
        partner = race.get_entrant_by_name(self.partner)
        opponent1 = race.get_entrant_by_name(self.opponent1)
        opponent2 = race.get_entrant_by_name(self.opponent2)

        self.logger.debug(f"self.enabled: {self.enabled}")

        our_total = self.get_coop_times(entrant, partner)
        self.logger.info(f"our_total: {our_total}")
        opponent_total = self.get_coop_times(opponent1, opponent2)
        self.logger.info(f"opponent_total: {opponent_total}")

        if our_total and opponent_total:
            self.update_text_if_both_finished(our_total, opponent_total)
        elif our_total and not opponent_total:
            self.update_text_if_we_finished(
                race, our_total, opponent1, opponent2)
        elif opponent_total and not our_total:
            self.update_text_if_they_finished(
                race, opponent_total, entrant, partner)
        else:
            self.our_time_text = " "
            self.our_time_color = self.still_racing_color
            self.opponent_time_text = " "
            self.opponent_time_color = self.still_racing_color

    def update_text_if_they_finished(
        self, race: Race, opponent_total, entrant: Entrant, partner: Entrant
    ):
        current_timer = datetime.now(timezone.utc) - race.started_at
        entrant_timer = self.get_finish_time_or_default(entrant, current_timer)
        partner_timer = self.get_finish_time_or_default(partner, current_timer)
        our_current_total = entrant_timer + partner_timer
        if our_current_total > opponent_total:
            self.opponent_time_color = self.winner_color
            self.our_time_color = self.loser_color
        else:
            our_current_total = opponent_total - our_current_total
            self.opponent_time_color = self.still_racing_color
            self.our_time_color = self.still_racing_color
        self.our_time_text = timer_to_str(our_current_total/2)
        self.opponent_time_text = timer_to_str(opponent_total/2)

    def update_text_if_we_finished(
        self, race: Race, our_total, opponent1: Entrant, opponent2: Entrant
    ):
        current_timer = datetime.now(timezone.utc) - race.started_at
        opp1_timer = self.get_finish_time_or_default(opponent1, current_timer)
        opp2_timer = self.get_finish_time_or_default(opponent2, current_timer)
        opponent_current_total = opp1_timer + opp2_timer
        if opponent_current_total > our_total:
            self.opponent_time_color = self.loser_color
            self.our_time_color = self.winner_color
        else:
            opponent_current_total = our_total - opponent_current_total
            self.opponent_time_color = self.still_racing_color
            self.our_time_color = self.still_racing_color
        self.our_time_text = timer_to_str(our_total/2)
        self.opponent_time_text = timer_to_str(opponent_current_total/2)

    @staticmethod
    def get_finish_time_or_default(player: Entrant, default: timedelta):
        if player and player.finish_time:
            return player.finish_time
        else:
            return default

    def update_text_if_both_finished(self, our_total, opponent_total):
        if our_total and opponent_total:
            self.our_time_text = timer_to_str(our_total/2)
            self.opponent_time_text = timer_to_str(opponent_total/2)
            if our_total > opponent_total:
                self.our_time_color = self.loser_color
                self.opponent_time_color = self.winner_color
            elif our_total < opponent_total:
                self.opponent_time_color = self.loser_color
                self.our_time_color = self.winner_color
            else:
                # a tie?!?!
                self.opponent_time_color = self.still_racing_color
                self.our_time_color = self.still_racing_color
        # self.set_text_if_two_finishers(race, our_total, opponent_total)
        # self.set_text_if_three_finishers(
        #     race, entrant, partner, opponent1, opponent2)
        # self.set_text_if_four_finishers(
        #     race, entrant, partner, opponent1, opponent2)

    # def set_text_if_four_finishers(self, race, entrant, partner,
    #                                opponent1, opponent2):
    #     if race.entrants_count_finished == 4:
    #         our_total = entrant.finish_time + partner.finish_time
    #         opponent_total = opponent1.finish_time + opponent2.finish_time
    #         if our_total < opponent_total:
    #             self.label_text = "We won!!! Average time:"
    #             self.text = timer_to_str(our_total / 2)
    #         else:
    #             self.label_text = "Opponents won, average time:"
    #             self.text = timer_to_str(opponent_total / 2)

    # def set_text_if_three_finishers(self, race, entrant, partner,
    #                                 opponent1, opponent2):
    #     if race.entrants_count_finished == 3:
    #         current_timer = datetime.now(timezone.utc) - race.started_at
    #         if not entrant.finish_time:
    #             self.label_text, self.text = self.get_coop_text(
    #                 "I need ", partner, opponent1, opponent2, current_timer)
    #         elif not partner.finish_time:
    #             prefix = partner.user.name + " needs "
    #             self.label_text, self.text = self.get_coop_text(
    #                 prefix, entrant, opponent1, opponent2, current_timer)
    #         elif not opponent1.finish_time:
    #             prefix = opponent1.user.name + " needs "
    #             self.label_text, self.text = self.get_coop_text(
    #                 prefix, opponent2, entrant, partner, current_timer)
    #         elif not opponent2.finish_time:
    #             prefix = opponent2.user.name + " needs "
    #             self.label_text, self.text = self.get_coop_text(
    #                 prefix, opponent1, entrant, partner, current_timer)

    # def set_text_if_two_finishers(self, race, our_total, opponent_total):
    #     if race.entrants_count_finished == 2:
    #         if our_total is not None:
    #             self.label_text = "We won!"
    #             self.text = timer_to_str(our_total / 2)
    #         elif opponent_total is not None:
    #             self.label_text = "They won. :("
    #             self.text = timer_to_str(opponent_total / 2)

    @staticmethod
    def get_coop_text(label_text_start: str, finished_partner: Entrant,
                      finished1: Entrant, finished2: Entrant,
                      current_timer: timedelta):
        finished_team_total = finished1.finish_time + finished2.finish_time
        time_to_beat = finished_team_total - finished_partner.finish_time
        if time_to_beat > current_timer:
            coop_text = timer_to_str(time_to_beat)
            coop_label_text = label_text_start + "to finish before"
        else:
            coop_label_text = str.format(
                f"{finished1.user.name} and {finished2.user.name} won")
            coop_text = timer_to_str(finished_team_total / 2)
        return coop_label_text, coop_text

    def get_coop_times(self, player1: Entrant, player2: Entrant):
        self.logger.debug(f"player1: {player1}")
        self.logger.debug(f"player2: {player2}")
        team_total = None
        if player1 and player1.finish_time and player2 and player2.finish_time:
            team_total = player1.finish_time + player2.finish_time
            self.logger.debug(
                f"calculated {player1.user.name} and {player2.user.name} "
                f"average is {team_total / 2}"
            )
        return team_total

    def is_enabled(self) -> bool:
        return (
            self.enabled and self.opponent_time_source != ""
            and self.our_time_source != ""  # and
            # self.partner is not None and self.opponent1 is not None and
            # self.opponent2 is not None
        )
