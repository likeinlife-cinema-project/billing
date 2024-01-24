import httpx
import pytest
import psycopg2

from .settings import settings


@pytest.fixture
def api_client() -> httpx.Client:
    return httpx.Client(base_url=settings.api_base_url)


@pytest.fixture(scope="session")
def setup_database():
    conn = psycopg2.connect(
        dbname=settings.postgres.db_name,
        user=settings.postgres.user,
        password=settings.postgres.password,
        host=settings.postgres.host,
    )
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO public.template (slug, content, params)
    VALUES ('test_template', '<p>Hello {{ name }}!</p>', '{"name"}');
    """
    cursor.execute(insert_query)
    conn.commit()
    yield
    conn.close()
