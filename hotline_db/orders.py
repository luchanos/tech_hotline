import json
from datetime import datetime

from asyncpg.pool import Pool

CREATE_TECH_ORDER = """
INSERT INTO tech_orders (
order_id,
order_messages, 
order_images, 
order_sounds, 
order_videos, 
created_dt)
VALUES ($1, $2, $3, $4, $5, $6) RETURNING order_id
"""


class TechOrder:
    # todo luchanos возможно перевести на dataclass и валидировать схемой
    def __init__(self, order_id: int, order_messages: list, order_images: list, order_videos: list, order_sounds: list,
                 created_dt: datetime = datetime.now()):
        self.order_id = order_id
        self.order_messages = order_messages
        self.order_images = order_images
        self.order_videos = order_videos
        self.order_sounds = order_sounds
        self.created_dt = created_dt


async def insert_tech_order_to_db(tech_order: TechOrder, db_pool: Pool):
    order_id = tech_order.order_id
    order_messages = tech_order.order_messages
    order_images = tech_order.order_images
    order_videos = tech_order.order_videos
    order_sounds = tech_order.order_sounds
    created_dt = tech_order.created_dt
    return await db_pool.fetchval(CREATE_TECH_ORDER,
                                  order_id,
                                  order_messages,
                                  order_images,
                                  order_sounds,
                                  order_videos,
                                  created_dt)
