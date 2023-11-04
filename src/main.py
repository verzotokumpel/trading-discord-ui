import os
from db import DatabaseController, Strategy, StrategyStatus
from uuid import uuid4
from datetime import datetime
from client import Client
from dotenv import load_dotenv


def main():
    controller = DatabaseController()

    example_strategy = Strategy(
        uuid4(), datetime.now(), 1, 1, "BTCUSDT", 100, StrategyStatus.INITIALIZED
    )
    controller.add_strategy(example_strategy)

    fetched_strategy = controller.get_strategy_by_discord_id(1)

    client = Client(controller)

    print(fetched_strategy)

    load_dotenv()
    client.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
