from subprocess import Popen, PIPE
from urllib.parse import urlparse
import os

import pytest
import asyncpg

from hotline_db.orders import TechOrder, insert_tech_order_to_db

TEST_DATABASE_URL = "postgres://postgres:dbpass@0.0.0.0:5432/db"
path_to_migrations = "./hotline_db/migrations/"

TABLES_TO_BE_CLEANED = ["tech_orders"]


def _execute_psql(cmd: str):
    database_url = urlparse(TEST_DATABASE_URL)
    command = (
        f"psql "
        f"-U {database_url.username} "
        f"-h {database_url.hostname} "
        f"-p {database_url.port or 5432} "
        f"-c '{cmd}' {database_url.path.strip('/')} "
    )

    proc = Popen(
        command, stdout=PIPE, stderr=PIPE, env=dict(os.environ, PGPASSWORD=database_url.password), shell=True
    )

    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise Exception("Error during running command %s: \n %s" % (command, stderr))


@pytest.fixture(scope="session", autouse=True)
def db_initialer():
    _execute_psql(
        """
        DROP SCHEMA IF EXISTS public CASCADE;
        CREATE SCHEMA IF NOT EXISTS public;
        GRANT USAGE ON SCHEMA public to PUBLIC;
        GRANT CREATE ON SCHEMA public to PUBLIC;
    """
    )
    _run_migrations("./hotline_db/migrations")


def _run_migrations(path_to_migrations):
    command = f"yoyo apply --database '{TEST_DATABASE_URL}' {path_to_migrations} -b"
    proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise Exception("Error during running command %s: \n %s" % (command, stderr))


@pytest.fixture
@pytest.mark.asyncio
async def db_pool_test():
    pool = await asyncpg.create_pool(dsn=TEST_DATABASE_URL)
    yield pool
    pool.close()


@pytest.fixture
@pytest.mark.asyncio
async def clean_test_tables(db_pool_test):
    TRUNCATE_TEST_TABLE_QUERY = """TRUNCATE TABLE %s"""
    for table in TABLES_TO_BE_CLEANED:
        await db_pool_test.fetchval(TRUNCATE_TEST_TABLE_QUERY % table)

GET_ORDER = """
SELECT order_id, order_messages, order_images, order_sounds, order_videos, created_dt, status
FROM tech_orders
WHERE order_id = $1"""


@pytest.mark.usefixtures("clean_test_tables")
@pytest.mark.asyncio
async def test_create_tech_order(db_pool_test):
    """Проверяем, что заявка создаётся в БД"""
    order_messages = ["test_message_1", "test_message_2"]
    order_images = ["test_image_url_1", "test_image_url_2"]
    order_videos = ["test_video_url_1", "test_video_url_2"]
    order_sounds = ["test_sound_url_1", "test_sound_url_2"]
    test_order = TechOrder(
                           order_messages=order_messages,
                           order_images=order_images,
                           order_videos=order_videos,
                           order_sounds=order_sounds,
                           status=1
    )
    order_id = await insert_tech_order_to_db(tech_order=test_order, db_pool=db_pool_test)
    getted_order = await db_pool_test.fetchrow(GET_ORDER, order_id)
    result = dict(getted_order)
    assert result["order_messages"] == order_messages
    assert result["order_images"] == order_images
    assert result["order_videos"] == order_videos
    assert result["order_sounds"] == order_sounds
    assert order_id == order_id
