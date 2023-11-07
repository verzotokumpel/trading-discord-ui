from dataclasses import dataclass
import sqlite3
from uuid import UUID
from datetime import datetime
from enum import Enum, auto


class StrategyStatus(Enum):
    INITIALIZED = auto()
    OPENING = auto()
    OPENED = auto()
    CLOSING = auto()
    CLOSED = auto()
    CANCELLED = auto()

@dataclass
class Strategy:
    id: UUID
    created_at: datetime
    strategy_discord_id: int
    op_discord_id: int
    currency_ticker: str
    op_initial_contribution: int
    status: StrategyStatus


@dataclass
class Contribution:
    id: UUID
    created_at: datetime
    strategy_id: str
    user_id: int
    value: int


@dataclass
class Trade:
    id: UUID
    created_at: datetime
    strategy_id: UUID
    sell_volume: int
    buy_volume: int

@dataclass
class ProfitMessage:
    message_id: str
    strategy_name: str
    channel_id: int


class DatabaseController:
    def __init__(self) -> None:
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        self.cur.executescript(
            """
                CREATE TABLE IF NOT EXISTS "strategies" (
                    "id" TEXT PRIMARY KEY NOT NULL, -- assuming you'll use UUID strings
                    "created_at" TIMESTAMP NOT NULL, -- you'll have to set this in your application
                    "strategy_discord_id" INTEGER NOT NULL,
                    "op_discord_id" TEXT NOT NULL,
                    "currency_ticker" TEXT NOT NULL,
                    "op_initial_contribution" INTEGER NOT NULL,
                    "status" TEXT NOT NULL -- changed from ENUM to TEXT
                );

                CREATE TABLE IF NOT EXISTS "contributions" (
                    "id" TEXT PRIMARY KEY NOT NULL, -- assuming you'll use UUID strings
                    "created_at" TIMESTAMP NOT NULL, -- you'll have to set this in your application
                    "strategy_id" TEXT NOT NULL,
                    "user_id" TEXT NOT NULL,
                    "value" INTEGER NOT NULL,
                    FOREIGN KEY ("strategy_id") REFERENCES "strategies" ("id")
                );

                CREATE TABLE IF NOT EXISTS "trades" (
                    "id" TEXT PRIMARY KEY NOT NULL, -- assuming you'll use UUID strings
                    "created_at" TIMESTAMP NOT NULL, -- you'll have to set this in your application
                    "strategy_id" TEXT NOT NULL,
                    "sell_volume" INTEGER NOT NULL,
                    "buy_volume" INTEGER NOT NULL,
                    FOREIGN KEY ("strategy_id") REFERENCES "strategies" ("id")
                );

                CREATE TABLE IF NOT EXISTS "messages_to_follow_profit" (
                    "message_id" TEXT PRIMARY_KEY NOT NULL,
                    "strategy_name" TEXT NOT NULL,
                    "channel_id" INTEGER NOT NULL
                );
            """
        )

    def add_strategy(self, strategy: Strategy) -> None:
        self.cur.execute(
            """
            INSERT INTO "strategies" (id, created_at, strategy_discord_id, op_discord_id, currency_ticker, op_initial_contribution, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(strategy.id),
                strategy.created_at,
                strategy.strategy_discord_id,
                strategy.op_discord_id,
                strategy.currency_ticker,
                strategy.op_initial_contribution,
                strategy.status.name,
            ),
        )
        self.con.commit()
    
    def add_message_to_follow_profit(self, message_id, strategy_name, channel_id) -> None:
        self.cur.execute(
            """
            INSERT INTO "messages_to_follow_profit" (message_id, strategy_name, channel_id) 
            VALUES (?, ?, ?)
            """,
            (
                message_id,
                strategy_name,
                channel_id,
            )
        )
        self.con.commit()
    
    def remove_message_to_follow_profit(self, strategy_name) -> None:
        self.cur.execute(
            """
            DELETE FROM "messages_to_follow_profit" WHERE strategy_name = ?
            """,
            (
                strategy_name,
            )
        )
        self.con.commit()

    def add_contribution(self, contribution: Contribution) -> None:
        self.cur.execute(
            """
            INSERT INTO "contributions" (id, created_at, strategy_id, user_id, value)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(contribution.id),
                contribution.created_at,
                str(contribution.strategy_id),
                str(contribution.user_id),
                contribution.value,
            ),
        )
        self.con.commit()

    def change_contribution_value(self, new_value, user_id, strategy_id) -> None:
        self.cur.execute(
            "SELECT value FROM contributions WHERE strategy_id=? AND user_id=?", (strategy_id, user_id,)
        )
        value = self.cur.fetchone()
        self.cur.execute(
            """
            UPDATE "contributions" SET value=? WHERE user_id=? AND strategy_id=?
            """,
            (
                int(new_value[0]) + value[0],
                user_id, 
                strategy_id,
            ),
        )
        self.con.commit()
    
    def change_status(self, strategy_discord_id, new_status) -> None:
        self.cur.execute(
            """
            UPDATE "strategies" SET status=? WHERE strategy_discord_id=?
            """,
            (
                new_status.name,
                strategy_discord_id,
            ),
        )
        self.con.commit()

    def add_trade(self, trade: Trade) -> None:
        self.cur.execute(
            """
            INSERT INTO "trades" (id, created_at, strategy_id, sell_volume, buy_volume)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(trade.id),
                trade.created_at,
                str(trade.strategy_id),
                trade.sell_volume,
                trade.buy_volume,
            ),
        )
        self.con.commit()

    def get_all_strategies(self) -> list[Strategy]:
        self.cur.execute("SELECT * FROM strategies")
        strategies = []
        for row in self.cur.fetchall():
            strategies.append(
                Strategy(
                    id=UUID(row[0]),
                    created_at=row[1],
                    strategy_discord_id=row[2],
                    op_discord_id=row[3],
                    currency_ticker=row[4],
                    op_initial_contribution=row[5],
                    status=StrategyStatus[row[6]],
                )
            )
        return strategies
    
    def get_strategy_status(self, strategy_discord_id: int) -> StrategyStatus:
        self.cur.execute(
            "SELECT status FROM strategies WHERE strategy_discord_id=?", (strategy_discord_id,)
        )
        status = self.cur.fetchone()
        return status
    
    def get_messages_to_follow_profit(self):
        self.cur.execute(
            "SELECT * FROM messages_to_follow_profit"
        )
        strategies = []
        for row in self.cur.fetchall():
            strategies.append(
                ProfitMessage(
                    message_id = row[0],
                    strategy_name = row[1],
                    channel_id = row[2]
                )
            )
        return strategies

    def get_user_positon_value(self, strategy_id: int, user_id: str) -> int:
        self.cur.execute(
            "SELECT value FROM contributions WHERE strategy_id=? AND user_id=?", (strategy_id, user_id,)
        )
        value = self.cur.fetchone()
        return value

    def get_strategy_by_discord_id(self, discord_id: int) -> Strategy:
        self.cur.execute(
            "SELECT * FROM strategies WHERE strategy_discord_id=?", (discord_id,)
        )
        row = self.cur.fetchone()
        if row:
            return Strategy(
                id=UUID(row[0]),
                created_at=row[1],
                strategy_discord_id=row[2],
                op_discord_id=row[3],
                currency_ticker=row[4],
                op_initial_contribution=row[5],
                status=StrategyStatus[row[6]],
            )
        return None
