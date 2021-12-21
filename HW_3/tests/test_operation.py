import pytest
from database import DummyDataBase
from event_manager import EventManger
from operation import Publish, Subscribe


@pytest.fixture
def event_man() -> EventManger:
    return EventManger(DummyDataBase())


def test_subscribe(event_man: EventManger) -> None:
    sub: Subscribe = Subscribe()

    assert sub.execute(event_man, "subscribe <user> to <channel>")

    assert not sub.execute(event_man, "buhehehehehe")
    assert not sub.execute(event_man, "subscribe user to channel")
    assert not sub.execute(event_man, "subscribe <user> to <channel")
    assert not sub.execute(event_man, "subscribe user> to <channel>")
    assert not sub.execute(event_man, "publish video on <channel>")


def test_publish(event_man: EventManger) -> None:
    pub: Publish = Publish()

    assert pub.execute(event_man, "publish video on <channel>")

    assert not pub.execute(event_man, "buzuzuzuzuzu")
    assert not pub.execute(event_man, "publish video on channel")
    assert not pub.execute(event_man, "publish video on <channel")
    assert not pub.execute(event_man, "publish video on channel>")
    assert not pub.execute(event_man, "subscribe <user> to <channel>")
