class Result:
    message: str
    status_code: int

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


class Review:
    content: str
    stars: int
    bot_id: str
    user_id: str

    def __init__(self, content: str, stars: int, user_id: str, bot_id: str):
        self.content = content
        self.stars = int(stars)
        self.bot_id = bot_id
        self.user_id = user_id


def ensure_is_ok(status_code: int) -> bool:
    return status_code >= 200 and status_code < 300
