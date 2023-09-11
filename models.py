from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Float
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
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
Base = declarative_base
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
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    account_number: Mapped[str] = mapped_column(String(64))
    time_in_force: Mapped[TimeInForce] = mapped_column(Enum(TimeInForce))
    gtc_date: Mapped[str] = mapped_column(String)
    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType))
    size: Mapped[str] = mapped_column(String)
    underlying_symbol: Mapped[str] = mapped_column(String)
    underlying_instrument_type: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Numeric)
    price_effect: Mapped[PriceEffect] = mapped_column(Enum(PriceEffect))
    value: Mapped[float] = mapped_column(Numeric)
    value_effect: Mapped[str] = mapped_column(String)
    stop_trigger: Mapped[str] = mapped_column(String)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
    contingent_status: Mapped[str] = mapped_column(String)
    confirmation_status: Mapped[str] = mapped_column(String)
    cancellable: Mapped[bool] = mapped_column(Boolean)
    cancelled_at: Mapped[str] = mapped_column(String)
    cancel_user_id: Mapped[str] = mapped_column(String)
    cancel_username: Mapped[str] = mapped_column(String)
    editable: Mapped[bool] = mapped_column(Boolean)
    edited: Mapped[bool] = mapped_column(Boolean)
    replacing_order_id: Mapped[str] = mapped_column(String)
    replaces_order_id: Mapped[str] = mapped_column(String)
    received_at: Mapped[str] = mapped_column(String)
    updated_at: Mapped[str] = mapped_column(String)
    in_flight_at: Mapped[str] = mapped_column(String)
    live_at: Mapped[str] = mapped_column(String)
    reject_reason: Mapped[str] = mapped_column(String)
    user_id: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    terminal_at: Mapped[str] = mapped_column(String)
    complex_order_id: Mapped[str] = mapped_column(String)
    complex_order_tag: Mapped[str] = mapped_column(String)
    preflight_id: Mapped[str] = mapped_column(String)
    global_request_id: Mapped[str] = mapped_column(String)

    legs: Mapped[List["Leg"]] = relationship("Leg", back_populates="order")

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, name={self.underlying_symbol!r}, price={self.price!r} )"


class Leg(Base):
    __tablename__: str = 'legs'
    
    id: int = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: str = mapped_column(String, ForeignKey('orders.id'))
    action: str = mapped_column(String, nullable=False)
    instrument_type: str = mapped_column(String, nullable=False)
    quantity: float = mapped_column(Numeric)
    symbol: str = mapped_column(String, nullable=False)
    
    # Relationship to Order table
    order: 'Order' = relationship("Order", back_populates="legs")
    
    __table_args__ = (
        CheckConstraint("instrument_type IN ('Equity', 'Futures', 'Cryptocurrency', 'Equity Option', 'Future Option')"),
        # Add more constraints if needed
    )



def is_status_terminal(status: OrderStatus):
    return status.value <= 7

"""
# TODO: 
Run 
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# engine = create_engine('postgresql://localhost/mydatabase')
# Session = sessionmaker(bind=engine)
# session = Session()

# live_orders = Order.find_by_status(session, OrderStatus.live)

# Pull from TastyTrades to get data
# Get orders back
# go in to TT and place fake orders in Sandbox
# once we have orders coming in, then use ORM to put that data into the database
"""
