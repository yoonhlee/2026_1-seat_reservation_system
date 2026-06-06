import pytest

from seat_reservation_system.seat_store import SeatStore


def test_reserve_and_cancel_flow():
    store = SeatStore([1, 2])
    seat_id, name = store.reserve(1, "Alex")
    assert (seat_id, name) == (1, "Alex")

    seat_id, name = store.status(1)
    assert (seat_id, name) == (1, "Alex")

    seat_id, name = store.cancel(1, "Alex")
    assert (seat_id, name) == (1, None)


def test_stats_counts_reserved_and_available():
    store = SeatStore([1, 2, 3])
    store.reserve(2, "Mina")
    assert store.stats() == {"total": 3, "reserved": 1, "available": 2}


def test_set_and_get_note():
    store = SeatStore([1])
    store.reserve(1, "Alice")
    seat_id, note = store.set_note(1, "창가 자리 원해요")
    assert seat_id == 1
    assert note == "창가 자리 원해요"
    assert store.get_note(1) == "창가 자리 원해요"


def test_set_note_on_unreserved_seat_raises():
    store = SeatStore([1])
    with pytest.raises(ValueError):
        store.set_note(1, "some note")


def test_cancel_clears_note():
    store = SeatStore([1])
    store.reserve(1, "Bob")
    store.set_note(1, "VIP")
    store.cancel(1)
    assert store.get_note(1) is None