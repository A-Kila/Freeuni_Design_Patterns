import pytest
from interfaces import IMovement
from movement import Crawl, FlyDecorator, HopDecorator, RunDecorator, WalkDecorator


@pytest.fixture
def crawl() -> IMovement:
    return Crawl()


@pytest.fixture
def hop(crawl: IMovement) -> IMovement:
    return HopDecorator(crawl)


@pytest.fixture
def walk(hop: IMovement) -> IMovement:
    return WalkDecorator(hop)


@pytest.fixture
def run(walk: IMovement) -> IMovement:
    return RunDecorator(walk)


@pytest.fixture
def fly(run: IMovement) -> IMovement:
    return FlyDecorator(run)


@pytest.fixture
def fly_hop(hop: IMovement) -> IMovement:
    return FlyDecorator(hop)


@pytest.fixture
def hop_fly(crawl: IMovement) -> IMovement:
    return HopDecorator(FlyDecorator(crawl))


def test_crawl(crawl: IMovement) -> None:
    assert crawl.move(10) == (1, 1)
    assert crawl.move(1) == (1, 1)
    assert crawl.move(0) == (0, 0)
    assert crawl.move(-5) == (0, 0)


def test_hop(hop: IMovement) -> None:
    assert hop.move(30) == (3, 2)
    assert hop.move(20) == (3, 2)
    assert hop.move(10) == (1, 1)


def test_walk(walk: IMovement) -> None:
    assert walk.move(100) == (4, 2)
    assert walk.move(40) == (4, 2)
    assert walk.move(30) == (3, 2)
    assert walk.move(10) == (1, 1)


def test_run(run: IMovement) -> None:
    assert run.move(100) == (6, 4)
    assert run.move(60) == (6, 4)
    assert run.move(50) == (4, 2)
    assert run.move(30) == (3, 2)
    assert run.move(10) == (1, 1)


def test_fly(fly: IMovement) -> None:
    assert fly.move(100) == (8, 4)
    assert fly.move(80) == (8, 4)
    assert fly.move(60) == (6, 4)
    assert fly.move(50) == (4, 2)
    assert fly.move(30) == (3, 2)
    assert fly.move(10) == (1, 1)


def test_fly_hop(fly_hop: IMovement) -> None:
    assert fly_hop.move(80) == (8, 4)
    assert fly_hop.move(79) == (3, 2)
    assert fly_hop.move(10) == (1, 1)
    assert fly_hop.move(0) == (0, 0)


def test_hop_fly(hop_fly: IMovement) -> None:
    assert hop_fly.move(80) == (8, 4)
    assert hop_fly.move(79) == (3, 2)
    assert hop_fly.move(10) == (1, 1)
    assert hop_fly.move(0) == (0, 0)
