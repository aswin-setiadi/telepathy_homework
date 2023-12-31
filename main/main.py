import logging
import re
from typing import List, Tuple, Union


from main.exceptions import (
    CheckInException,
    CheckOutException,
    CleanException,
    FloorCountException,
    RepairException,
    RepairedException,
    RoomCountException,
    RoomStatusException,
)
from main.global_vars import DEBUGGING, ROOM_STATUSES, HOTEL_COLUMNS

if DEBUGGING:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


class Room:
    """
    Room class.

    Parameters:

        number <str>: room number, format is {i}{j} where i is floor number (1-M) and j is room column (A-E).

        status <str>: room status, acceptable values are "Available", "Occupied", "Vacant", "Repair".
    """

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
        """Set room status from Available to Occupied, returns True if success."""
        if self._status != ROOM_STATUSES[0]:
            raise CheckInException()
        self._status = ROOM_STATUSES[1]
        return True

    def check_out(self) -> bool:
        """Set room status from Occupied to Vacant, returns True if success."""
        if self._status != ROOM_STATUSES[1]:
            raise CheckOutException()
        self._status = ROOM_STATUSES[2]
        return True

    def clean(self) -> bool:
        """Set room status from Vacant to Available, returns True if success."""
        if self._status != ROOM_STATUSES[2]:
            raise CleanException()
        self._status = ROOM_STATUSES[0]
        return True

    def repair(self) -> bool:
        """Set room status from Vacant to Repair, returns True if success."""
        if self._status != ROOM_STATUSES[2]:
            raise RepairException()
        self._status = ROOM_STATUSES[3]
        return True

    def repaired(self) -> bool:
        """Set room status from Repair to Vacant, returns True if success."""
        if self._status != ROOM_STATUSES[3]:
            raise RepairedException()
        self._status = ROOM_STATUSES[2]
        return True


class Hotel:
    """
    Hotel class that represents the hotel system. There must be always 5 rooms for each floor.

    Parameters:
        m_floors <int>: number of floor

        rooms_w_status <List[List[str]]>: floor matrix with each room set with user defined status (optional, default to all Available)

    Acceptable statuses are "Available", "Occupied", "Vacant", "Repair".
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
        """Assign Available room nearest to the hotel entrance. Will return room number or None if no Available room."""
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

    def list_available_rooms(self) -> List:
        """Will return a list of Available room number in order from closest to furthest room from the hotel entrance."""
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

    def get_room(self, num: str) -> Union[Room, None]:
        """Retrieve Room object given the room number.

        Parameters:
            num <int> : room number, format is {i}{j} where i is floor number (1-M) and j is room column (A-E).
        """
        result = re.search(r"^(\d+)([ABCDE]+)$", num)
        if not result:
            logging.error(
                f"Invalid num value {num}. Format is (i)(j) where i is floor number (1-{self.floor_count}) and j is room column (A-E)."
            )
            return None
        # group(0) will be the whole match as it is a group itself
        row = int(result.group(1))
        col = result.group(2)
        if row < 1 or row > len(self._rooms):
            logging.error(f"floor must be 1-{len(self._rooms)}, received {row}.")
            return None
        if col not in HOTEL_COLUMNS:
            logging.error(f"room column must be in {HOTEL_COLUMNS}, received {col}.")
            return None
        return self._rooms[row - 1][HOTEL_COLUMNS.index(col)]


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


class VirusMapBfs:
    def __init__(self, m: int, n: int, matrix: List[List[int]]) -> None:
        self.m = m
        self.n = n
        self.matrix = matrix
        self.unit_time = 0
        self.healthy_guests: set[Tuple[int, int]] = set()
        self.infection_list_today: List[Tuple[int, int]] = []
        self.infection_list_tmr: List[Tuple[int, int]] = []

    def solve(self) -> str:
        """
        pseudo code:
        - find all the infected person, add them to infection_today
        - find all the healthy_guests, add them to healthy_guests set
        - if infection_today empty, if healthy_guests empty return 0 else return 1
        - loop infected room:
            - if the neighbour is healthy, add to visited list, add to infection_tmr
        - loop infection_tmr, change their status to 2/ infected and remove the room from healthy_guests
        - if infection_tmr not empty, unit_time+1, infection_today= infection_tmr, infection_tmr=[]
        - else if healthy_guests not empty, return -1, else: return unit_time
        """

        def _get_neighbours(coord: Tuple[int, int]) -> List[Tuple[int, int]]:
            row = coord[0]
            col = coord[1]
            neighbours: List[Tuple[int, int]] = []
            if row != 0:
                neighbours.append((row - 1, col))
            if row != self.m - 1:
                neighbours.append((row + 1, col))
            if col != 0:
                neighbours.append((row, col - 1))
            if col != self.n - 1:
                neighbours.append((row, col + 1))
            return neighbours

        for row in range(self.m):
            for col in range(self.n):
                if self.matrix[row][col] == 1:
                    self.healthy_guests.add((row, col))
                if self.matrix[row][col] == 2:
                    self.infection_list_today.append((row, col))

        if not self.infection_list_today:
            if not self.healthy_guests:
                return "0"
            else:
                return "-1"

        while True:
            visited_1: List[Tuple[int, int]] = []
            for room_coord in self.infection_list_today:
                neighbours = _get_neighbours(room_coord)
                for n in neighbours:
                    if self.matrix[n[0]][n[1]] == 1:
                        if n not in visited_1:
                            visited_1.append(n)
                            self.infection_list_tmr.append(n)
            for coord in self.infection_list_tmr:
                self.matrix[coord[0]][coord[1]] = 2
                self.healthy_guests.remove(coord)
            if self.infection_list_tmr:
                self.unit_time += 1
                self.infection_list_today = self.infection_list_tmr
                self.infection_list_tmr = []
            else:
                if len(self.healthy_guests):
                    return "-1"
                else:
                    return str(self.unit_time)
