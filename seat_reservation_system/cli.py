from seat_reservation_system.seat_store import SeatStore
from seat_reservation_system.seats import SEAT_IDS

HELP_TEXT = """Commands:
list                      - List all seats
reserve <seat_id> <name>  - Reserve a seat
cancel <seat_id> [name]   - Cancel a reservation
status <seat_id>          - Show seat status
search <name>             - Search seats reserved by name
note <seat_id> [text]     - View or set a note on a reserved seat
stats                     - Show summary stats
help                      - Show this help
exit                      - Exit the program"""


def run_cli():
    store = SeatStore(SEAT_IDS)
    print("Seat Reservation System CLI")
    print("Type 'help' to see available commands.")
    while True:
        try:
            raw = input("seat> ").strip()
        except EOFError:
            print()
            break
        if not raw:
            continue

        parts = raw.split()
        command, args = parts[0].lower(), parts[1:]
        if command in {"exit", "quit"}:
            break
        if command == "help":
            print(HELP_TEXT)
            continue
        try:
            if command == "list":
                for seat_id, name in store.list_seats():
                    _print_seat(seat_id, name)
            elif command == "reserve":
                _require_args(command, args, 2)
                seat_id, name = store.reserve(int(args[0]), args[1])
                _print_seat(seat_id, name)
            elif command == "cancel":
                _require_args(command, args, 1)
                name = args[1] if len(args) > 1 else None
                seat_id, name = store.cancel(int(args[0]), name)
                _print_seat(seat_id, name)
            elif command == "status":
                _require_args(command, args, 1)
                seat_id, name = store.status(int(args[0]))
                note = store.get_note(seat_id)
                _print_seat(seat_id, name, note)
            elif command == "note":
                _require_args(command, args, 1)
                seat_id = int(args[0])
                if len(args) >= 2:
                    note_text = " ".join(args[1:])
                    seat_id, note = store.set_note(seat_id, note_text)
                    print(f"Seat {seat_id}: note set to '{note}'")
                else:
                    note = store.get_note(seat_id)
                    if note:
                        print(f"Seat {seat_id}: note - {note}")
                    else:
                        print(f"Seat {seat_id}: no note.")
            elif command == "search":
                _require_args(command, args, 1)
                results = [
                    (seat_id, name)
                    for seat_id, name in store.list_seats()
                    if name and args[0].lower() == name.lower()
                ]
                if results:
                    for seat_id, name in results:
                        _print_seat(seat_id, name)
                else:
                    print(f"No reservations found for '{args[0]}'.")
            elif command == "stats":
                stats = store.stats()
                print(
                    "Total: {total}, Reserved: {reserved}, Available: {available}".format(
                        **stats
                    )
                )
            else:
                print("Unknown command. Type 'help' for commands.")
        except ValueError as exc:
            print(f"Error: {exc}")


def _print_seat(seat_id, name, note=None):
    label = f"reserved by {name}" if name else "available"
    if note and name:
        label += f" [{note}]"
    print(f"Seat {seat_id}: {label}")


def _require_args(command, args, count):
    if len(args) < count:
        raise ValueError(f"Usage: {command} requires {count} argument(s).")