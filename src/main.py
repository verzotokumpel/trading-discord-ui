import os
from db import DatabaseController, Strategy, StrategyStatus
from uuid import uuid4
from datetime import datetime
from client import Client
from dotenv import load_dotenv


def main():
    controller = DatabaseController()

    client = Client(controller)

    load_dotenv()
    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    main()
