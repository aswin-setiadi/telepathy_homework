"""Custom Exceptions module"""
from main.global_vars import ROOM_STATUSES


class RoomStatusException(Exception):
    def __init__(self, status) -> None:
        super().__init__(f"{status} is not an acceptable room status")


class RoomCountException(Exception):
    def __init__(self, floor, room_count) -> None:
        self.message = f"Room count must be 5, floor {floor} got {room_count}"
        super().__init__(self.message)


class FloorCountException(Exception):
    def __init__(self, custom: bool = False) -> None:
        if custom:
            super().__init__(
                f"Length of floor with custom room status must be equal to m_floors"
            )
        else:
            super().__init__(f"Floor count must be int and minimum floor count is 1")


class RoomToBeOccupied(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Room status must be {ROOM_STATUSES[0]} to be {ROOM_STATUSES[1]}"
        )


class RoomToBeVacant(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Room status must be {ROOM_STATUSES[1]}/ {ROOM_STATUSES[3]} to be {ROOM_STATUSES[2]}"
        )


class RoomToBeAvailable(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Room status must be {ROOM_STATUSES[2]} to be {ROOM_STATUSES[0]}"
        )


class RoomToBeRepair(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Room status must be {ROOM_STATUSES[2]} to be {ROOM_STATUSES[3]}"
        )
