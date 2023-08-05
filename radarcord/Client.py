import discord
import requests
import threading
from .enums import IntervalPreset
from .errors.RadarcordException import RadarcordException
from .utils import Result, Review, ensure_is_ok


class RadarcordClient:
    discord_client: discord.Client
    authorization: str
    _base = "https://radarcord.net"
    _apiStart = f"{_base}/api"

    def __init__(self, discord_client: discord.Client, authorization: str) -> None:
        self.discord_client = discord_client
        self.authorization = authorization

    def _does_client_exists(self) -> bool:
        """Ensures the client exists.

        ## NOTE:

        This is a private method, and thus should not be used in your project.
        """
        return self.discord_client.user != None

    def post_stats(self, shard_count: int = 1) -> Result:
        """Posts your stats to the Radarcord API.

        ## Args:

            shard_count (int, optional): The amount of shards your bot has (if any). Defaults to 1.

        ## Raises:

            RadarcordException: Occurs on either the client not being logged in or the request status code not being a `200` status code.

        ## Returns:

            Result: A custom class representing the result of the post.
        """
        if not self._does_client_exists():
            raise RadarcordException(
                "No client exists, please try this method again in your ready event."
            )

        assert self.discord_client.user != None

        guild_count = len(self.discord_client.guilds)

        res = requests.post(
            f"{self._apiStart}/bot/{self.discord_client.user.id}/stats",
            headers={"Authorization": self.authorization},
            data={"guilds": guild_count, "shards": shard_count},
        )

        if not ensure_is_ok(res.status_code):
            raise RadarcordException(
                f"Stats failed to post.\nStatus: {res.status_code}\nBody: {res.json()}"
            )

        return Result(res.json()["message"], res.status_code)

    def autopost_stats(
        self, shard_count: int = 1, interval: IntervalPreset = IntervalPreset.Default
    ):
        """Autoposts your stats in a thread.

        ## Args:

            shard_count (int, optional): The amount of shards your bot has (if any). Defaults to 1.

            interval (IntervalPreset, optional): How long between posts. Defaults to IntervalPreset.Default (120 seconds).
        """

        def post():
            try:
                self.post_stats(shard_count)
            except RadarcordException as e:
                print(f"Autopost failed: {str(e)}")

        autopost_thread = threading.Thread(target=post)

        while True:
            autopost_thread.start()

    def get_reviews(self) -> list[Review]:
        """Gets all the reviews for your bot.

        ## Raises:
            RadarcordException: Occurs on either the client not being logged in or the request status code not being a `200` status code.

        ## Returns:
            list[Review]: All your reviews put into a list.
        """
        if not self._does_client_exists():
            raise RadarcordException(
                "No client exists, please try this method again in your ready event."
            )

        assert self.discord_client.user != None

        res = requests.get(
            f"{self._apiStart}/bot/{str(self.discord_client.user.id)}/reviews"
        )

        if not ensure_is_ok(res.status_code):
            raise RadarcordException(
                f"Failed to get reviews.\nStatus: {res.status_code}\nBody: {res.json()}"
            )

        reviews: list[Review] = []

        for review in res.json()["reviews"]:
            reviews.append(
                Review(review.content, int(review.stars), review.userid, review.botid)
            )

        return reviews
