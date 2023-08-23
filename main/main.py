import logging
from typing import List, Tuple, Union


from main.exceptions import (
    FloorCountException,
    RoomCountException,
    RoomStatusException,
    RoomToBeAvailable,
    RoomToBeOccupied,
    RoomToBeRepair,
    RoomToBeVacant,
)
from main.global_vars import DEBUGGING, ROOM_STATUSES, HOTEL_COLUMNS

if DEBUGGING:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


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


class VirusMap:
    def __init__(self, m: int, n: int, matrix: List[List[int]]) -> None:
        self.m = m
        self.n = n
        self.matrix = matrix
        self.unit_time = 0
        self.healthy_guests: List[Tuple[int, int]] = []
        self.rooms_to_infect: List[Tuple[int, int]] = []

    def solve(self) -> str:
        while True:
            visited_matrix = [[False] * self.n for _ in range(self.m)]
            logging.debug(self.matrix)
            # input("pause")
            for row in range(self.m):
                for col in range(self.n):
                    self._visit_room(row, col, visited_matrix)
            logging.debug(self.rooms_to_infect)
            logging.debug(self.healthy_guests)
            if not self.rooms_to_infect:
                if not self.healthy_guests:
                    return f"{self.unit_time}"
                else:
                    return "-1"
            else:
                for room in self.rooms_to_infect:
                    self.matrix[room[0]][room[1]] = 2
                    self.healthy_guests.remove((room[0], room[1]))
                self.rooms_to_infect[:] = []
                self.unit_time += 1
            logging.debug("updating rooms_to_infect and healthy_guests list:")
            logging.debug(self.rooms_to_infect)
            logging.debug(self.healthy_guests)

    def _visit_room(self, row, col, v_m, to_be_infected=False):
        if to_be_infected and self.matrix[row][col] == 1:
            if (row, col) not in self.rooms_to_infect:
                self.rooms_to_infect.append((row, col))
        if v_m[row][col]:
            return
        v_m[row][col] = True
        if self.matrix[row][col] == 0:
            return
        if self.matrix[row][col] == 1:
            if (row, col) not in self.healthy_guests:
                self.healthy_guests.append((row, col))
        if self.matrix[row][col] == 2:
            neighbours = self._get_neighbours(row, col)
            for neighbour in neighbours:
                self._visit_room(neighbour[0], neighbour[1], v_m, True)

    def _get_neighbours(self, row, col):
        neighbours = []
        if row != 0:
            neighbours.append((row - 1, col))
        if row != self.m - 1:
            neighbours.append((row + 1, col))
        if col != 0:
            neighbours.append((row, col - 1))
        if col != self.n - 1:
            neighbours.append((row, col + 1))
        return neighbours
