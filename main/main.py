"""Main entry file for question 1a"""
from typing import List, Union


from main.exceptions import (
    FloorCountException,
    RoomCountException,
    RoomStatusException,
    RoomToBeAvailable,
    RoomToBeOccupied,
    RoomToBeRepair,
    RoomToBeVacant,
)
from main.global_vars import ROOM_STATUSES, HOTEL_COLUMNS


class Hotel:
    """
    Hotel class that represents the hotel system.
    There are always 5 rooms for each floor.
    """

    def __init__(
        self, m_floors: int, rooms_w_status: Union[List[List[str]], None] = None
    ) -> None:
        if not isinstance(m_floors, int) or m_floors < 1:
            raise FloorCountException()
        self.floor_count = m_floors
        self._rooms = []
        if rooms_w_status is not None:
            if m_floors != len(rooms_w_status):
                raise FloorCountException(custom=True)
            for i in range(len(rooms_w_status)):
                if len(rooms_w_status[i]) != len(HOTEL_COLUMNS):
                    raise RoomCountException(i + 1, len(rooms_w_status[i]))
                self._rooms.append(
                    [
                        Room(f"{i+1}{HOTEL_COLUMNS[j]}", status=v)
                        for j, v in enumerate(rooms_w_status[i])
                    ]
                )
        else:
            for i in range(m_floors):
                self._rooms.append([Room(f"{i+1}{j}") for j in HOTEL_COLUMNS])

    def assign_room(self) -> Union[str, None]:
        for i in range(self.floor_count):
            if i % 2:
                for j in reversed(self._rooms[i]):
                    if j.status == ROOM_STATUSES[0]:
                        j.check_in()
                        return j.number
            else:
                for j in self._rooms[i]:
                    if j.status == ROOM_STATUSES[0]:
                        j.check_in()
                        return j.number
        return None

    def list_available_rooms(self):
        avail_rooms = []
        for i in range(self.floor_count):
            if i % 2:
                for j in reversed(self._rooms[i]):
                    if j.status == ROOM_STATUSES[0]:
                        avail_rooms.append(j.number)
            else:
                for j in self._rooms[i]:
                    if j.status == ROOM_STATUSES[0]:
                        avail_rooms.append(j.number)
        return avail_rooms


class Room:
    """Room class"""

    def __init__(self, number: str, status: str = ROOM_STATUSES[0]) -> None:
        if status not in ROOM_STATUSES:
            raise RoomStatusException(status=status)
        self._number = number
        self._status = status

    @property
    def number(self) -> str:
        return self._number

    @property
    def status(self) -> str:
        return self._status

    def check_in(self) -> bool:
        if self._status != ROOM_STATUSES[0]:
            raise RoomToBeOccupied()
        self._status = ROOM_STATUSES[1]
        return True

    def check_out(self) -> bool:
        if self._status != ROOM_STATUSES[1]:
            raise RoomToBeVacant()
        self._status = ROOM_STATUSES[2]
        return True

    def clean(self) -> bool:
        if self._status != ROOM_STATUSES[2]:
            raise RoomToBeAvailable()
        self._status = ROOM_STATUSES[0]
        return True

    def repair(self) -> bool:
        if self._status != ROOM_STATUSES[2]:
            raise RoomToBeRepair()
        self._status = ROOM_STATUSES[3]
        return True

    def repaired(self) -> bool:
        if self._status != ROOM_STATUSES[3]:
            raise RoomToBeVacant()
        self._status = ROOM_STATUSES[2]
        return True
