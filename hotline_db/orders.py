from dataclasses import dataclass
from datetime import datetime
from typing import List

from asyncpg.pool import Pool

CREATE_TECH_ORDER = """
INSERT INTO tech_orders (
order_messages,
order_images,
order_sounds,
order_videos,
created_dt,
status
)
VALUES ($1, $2, $3, $4, $5, $6) RETURNING order_id
"""


class TechOrder:
    def __init__(self, order_messages: list, order_images: list, order_videos: list, order_sounds: list,
                 status: int, created_dt: datetime = datetime.now(), order_id: int = None):
        self.order_id = order_id
        self.order_messages = order_messages
        self.order_images = order_images
        self.order_videos = order_videos
        self.order_sounds = order_sounds
        self.created_dt = created_dt
        self.status = status


@dataclass
class TechOrderOther:
    # todo luchanos потом перевести на датакласс всю работу с заявками
    order_messages: List[str]
    order_images: List[str]
    order_videos: List[str]
    order_sounds: List[str]
    order_id: int = None


async def insert_tech_order_to_db(tech_order: TechOrder, db_pool: Pool):
    order_messages = tech_order.order_messages
    order_images = tech_order.order_images
    order_videos = tech_order.order_videos
    order_sounds = tech_order.order_sounds
    created_dt = tech_order.created_dt
    status = tech_order.status
    return await db_pool.fetchval(CREATE_TECH_ORDER,
                                  order_messages,
                                  order_images,
                                  order_sounds,
                                  order_videos,
                                  created_dt,
                                  status)
