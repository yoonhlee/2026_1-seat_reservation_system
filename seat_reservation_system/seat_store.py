class SeatStore:
    def __init__(self, seat_ids):
        self._seats = {seat_id: None for seat_id in seat_ids}
        self._notes: dict = {}

    def list_seats(self):
        return self._seats.items()

    def reserve(self, seat_id, name):
        current = self._get(seat_id)
        if current is not None:
            raise ValueError("Seat is already reserved.")
        self._seats[seat_id] = name
        return seat_id, name

    def cancel(self, seat_id, name=None):
        current = self._get(seat_id)
        if current is None:
            raise ValueError("Seat is not reserved.")
        if name and current != name:
            raise ValueError("Name does not match the reservation.")
        self._seats[seat_id] = None
        self._notes.pop(seat_id, None)
        return seat_id, None

    def status(self, seat_id):
        return seat_id, self._get(seat_id)

    def stats(self):
        reserved = sum(1 for name in self._seats.values() if name)
        total = len(self._seats)
        return {"total": total, "reserved": reserved, "available": total - reserved}

    def set_note(self, seat_id, note: str):
        if self._get(seat_id) is None:
            raise ValueError("Cannot add a note to an unreserved seat.")
        self._notes[seat_id] = note
        return seat_id, note

    def get_note(self, seat_id) -> str | None:
        self._get(seat_id)
        return self._notes.get(seat_id)

    def _get(self, seat_id):
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")
        return self._seats[seat_id]