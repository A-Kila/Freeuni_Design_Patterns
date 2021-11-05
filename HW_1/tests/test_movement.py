from app.movement import Crawl


def test_Crawl() -> None:
    Crawl()
    assert Crawl().move(10) == (1, 1)
