class UrlBuilder:
    def __init__(self):
        """
        For opap's REST API documentation check:
        https://www.opap.gr/en/web-services

        Only `get_in_date_range' is strictly required. The rest of the methods
        are shown as a demonostration on how to augment the class to handle
        more operations.
        """
        self.base_url = "https://api.opap.gr/"
        self.kino_game_id = 1100

    def get_in_date_range(self, from_date, to_date):
        url = (
            self.base_url
            + f"draws/v3.0/{self.kino_game_id}/draw-date/{from_date}/{to_date}"
        )
        return url

    def get_last_result_and_active(self):
        url = self.base_url + f"draws/v3.0/{self.kino_game_id}/last-result-and-active"
        return url

    def get_statistics(self, draw_range):
        """
        draw_range denotes the number of last draws that are taken into account for the
        calculation of the statistics. It is mandatory for Keno. The actual range
        can be either 12 or 1801 and all other values will be treated with a
        400 Bad Request.
        """
        if draw_range not in [12, 1801]:
            raise ValueError("draw_range must be either 12 or 1801!")
        url = (
            self.base_url
            + f"games/v1.0/{self.kino_game_id}/statistics?drawRange={draw_range}"
        )
        return url
