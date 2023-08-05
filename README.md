# Radarcord.py

The best way to interact with the Radarcord API, now available in the Python flavor!

## Features

- Easy to use, less pressure on writing HTTP yourself.
- Supports `discord.py` and may support other libraries soon.
- May come with Webhook support soon.

## Installation

Installation is as easy as running one command.

```bash
pip install radarcord.py
```

## Usage

Using the package is super easy as well! Open up your Python project, and let's go!

```python
from typing import Any
import discord
import radarcord


class Client(discord.Client):
    radar: radarcord.RadarcordClient

    def __init__(self, intents: discord.Intents, **options: Any):
        super().__init__(intents=intents, options=options)
        self.radar = radarcord.RadarcordClient(self, "some_authorization") # Replace `some_authorization` with your Radarcord API token

    async def on_ready(self):
        print("The client is ready!")

        # shard_count defaults to 1 if not explicitly passed in.
        self.radar.post_stats()

        # If you have a sharded client:
        self.radar.post_stats(self.shard_count)

intents = discord.Intents.default()
client = Client(intents=intents)
client.run("TOKEN") # Replace TOKEN with your Discord bot's token.
```

## Getting reviews

Your bot reviews are super important to the image of your bot, so we have given support to get those reviews!

```python
from typing import Any
from radarcord import Review
import discord
import radarcord


class Client(discord.Client):
    radar: radarcord.RadarcordClient

    def __init__(self, intents: discord.Intents, **options: Any):
        super().__init__(intents=intents, options=options)
        self.radar = radarcord.RadarcordClient(self, "some_authorization")  # Replace `some_authorization` with your Radarcord API token

    async def on_ready(self):
        print("The client is ready!")
        reviews: list[Review] = self.radar.get_reviews() # Typing is a bit buggy currently, explicitly type reviews as `list[Review]` for now.

        # This is an example to make sure you got the reviews.
        # You can also embed these into your website if preferred.
        for review in reviews:
            print(review)


intents = discord.Intents.default()
client = Client(intents=intents)
client.run("TOKEN") # Replace TOKEN with your Discord bot's token.
```

## License

This package is licensed under the **[MIT License](https://github.com/Yoshiboi18303/radarcord-py/blob/main/LICENSE)**

## Bugs?

Report those bugs **[here](https://github.com/Yoshiboi18303/radarcord-py/issues)**!

---

Copyright © 2023 - present Yoshiboi18303

**[Radarcord](https://radarcord.net)** is owned by Scorprian.

**Do not reach out to Yoshiboi18303 for any Radarcord issues that do not involve the package.**

**If you have an issue with Radarcord, reach out to Scorprian in the [Discord server](https://discord.gg/km8xRh2atD).**
