from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Float
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Integer, Enum
"""
Task list:
- Finish Order data model
- Use tasty trades API to search order history on account (will need to populate dummy data for this to work)
- Save data from API call into Postgres with Order model
- Set up jupyter notebook with pandas to pull data in from postgres 
"""

class TimeInForce(enum.Enum):
    day = 1
    gtc = 2
    gtd = 3


class OrderType(enum.Enum):
    limit = 1
    market = 2
    stop = 3
    stop_limit = 4
    notional_market = 5

class PriceEffect(enum.Enum):
    debit = 1
    credit = 2

class OrderStatus(enum.Enum):
    received = 1
    routed = 2
    in_flight = 3
    live = 4
    cancel_requested = 5
    replace_requested = 6
    contingent = 7
    filled = 8
    cancelled = 9
    expired = 10
    rejected = 11
    removed = 12
    partially_removed = 13

def is_status_terminal(status: OrderStatus):
    return status.value <= 7
class Base(DeclarativeBase):
    pass


class Order(Base):
    """
    Docs:
    - https://developer.tastytrade.com/order-submission/#order-attributes
    - https://developer.tastytrade.com/open-api-spec/orders/#/
    TODO:
    - Finish modeling this example trade
    - Find what fields could be missing from this example and add them in
    - Figure out which fields should be nullable and which shouldn't (optional)
    -
    """
    """{
    "id": 54758825,
    "account-number": "4WT00001",
    "time-in-force": "GTC",
    "order-type": "Limit",
    "size": 0,
    "underlying-symbol": "QQQ",
    "price": "2.0",
    "price-effect": "Debit",
    "status": "Live",
    "cancellable": true,
    "editable": true,
    "edited": false,
    "legs": [
        {
            "instrument-type": "Equity Option",
            "symbol": "QQQ   191114C00187000",
            "quantity": 0,
            "remaining-quantity": 0,
            "action": "Buy to Close",
            "fills": []
        }
        ]
    }
    """
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_number: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))
    time_in_force: Mapped[TimeInForce]
    order_type: Mapped[OrderType]
    size: Mapped[int]
    underlying_symbol: Mapped[str] = mapped_column(String(8))
    price: Mapped[float] = mapped_column(Float(5))
    price_effect: Mapped[PriceEffect]
    status: Mapped[OrderStatus]

    legs: Mapped[List["Leg"]] = relationship("TODO")

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, name={self.underlying_symbol!r}, price={self.price!r} )"


class Leg(Base):
    __tablename__ = "leg"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
