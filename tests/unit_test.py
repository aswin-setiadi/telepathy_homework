import pytest
from main.exceptions import (
    FloorCountException,
    RoomCountException,
    RoomStatusException,
    RoomToBeAvailable,
    RoomToBeOccupied,
    RoomToBeRepair,
    RoomToBeVacant,
)

from main.main import Hotel, Room


class TestHotel:
    status = {0: "Available", 1: "Occupied", 2: "Vacant", 3: "Repair"}

    def test_hotel_creation(self):
        Hotel(4)
        hotel = Hotel(
            4,
            [
                [TestHotel.status[0] for i in range(5)],
                [TestHotel.status[1] for i in range(5)],
                [TestHotel.status[2] for i in range(5)],
                [TestHotel.status[3] for i in range(5)],
            ],
        )
        assert isinstance(hotel, Hotel)

    def test_invalid_floor_count(self):
        with pytest.raises(FloorCountException):
            Hotel("fish")

    def test_invalid_hotel_custom_status_floor_count(self):
        with pytest.raises(FloorCountException):
            Hotel(
                2,
                [
                    [TestHotel.status[3] for i in range(5)],
                    [TestHotel.status[2] for i in range(5)],
                    [TestHotel.status[1] for i in range(5)],
                ],
            )

    def test_invalid_hotel_room_status_init(self):
        with pytest.raises(RoomStatusException):
            Hotel(
                4,
                [
                    ["Invalid" for i in range(5)],
                    [TestHotel.status[3] for i in range(5)],
                    [TestHotel.status[2] for i in range(5)],
                    [TestHotel.status[1] for i in range(5)],
                ],
            )

    def test_invalid_room_count(self):
        with pytest.raises(RoomCountException):
            Hotel(
                2,
                [
                    [TestHotel.status[0] for i in range(5)],
                    [TestHotel.status[1] for i in range(4)],
                ],
            )

    def test_assign_room_odd(self):
        hotel = Hotel(4)
        assert hotel.assign_room() == "1A"

    def test_assign_room_even_floor(self):
        hotel = Hotel(
            2,
            [
                [TestHotel.status[1] for i in range(5)],
                [TestHotel.status[0] for i in range(5)],
            ],
        )
        assert hotel.assign_room() == "2E"

    def test_assign_room_full(self):
        hotel = Hotel(
            3,
            [
                [TestHotel.status[1] for i in range(5)],
                [TestHotel.status[2] for i in range(5)],
                [TestHotel.status[3] for i in range(5)],
            ],
        )
        assert hotel.assign_room() is None

    def test_list_available_rooms(self):
        hotel = Hotel(4)
        hotel2 = Hotel(4)
        hotel2.assign_room()
        expected_list = [
            "1A",
            "1B",
            "1C",
            "1D",
            "1E",
            "2E",
            "2D",
            "2C",
            "2B",
            "2A",
            "3A",
            "3B",
            "3C",
            "3D",
            "3E",
            "4E",
            "4D",
            "4C",
            "4B",
            "4A",
        ]
        assert hotel.list_available_rooms() == expected_list
        assert hotel2.list_available_rooms() == expected_list[1:]


class TestRoom:
    def test_room_creation(self):
        Room("1A")
        room = Room("1B", "Available")
        assert isinstance(room, Room)
        assert room.number == "1B"
        assert room.status == "Available"

    def test_check_in(self):
        room1 = Room("1A")
        room2 = Room("1B", "Occupied")
        assert room1.check_in()
        assert room1.status == "Occupied"
        with pytest.raises(RoomToBeOccupied):
            room2.check_in()

    def test_check_out(self):
        room1 = Room("1A", "Occupied")
        room2 = Room("1B")
        assert room1.check_out()
        assert room1.status == "Vacant"
        with pytest.raises(RoomToBeVacant):
            room2.check_out()

    def test_clean(self):
        room1 = Room("1A", "Vacant")
        room2 = Room("1B")
        assert room1.clean()
        assert room1.status == "Available"
        with pytest.raises(RoomToBeAvailable):
            room2.clean()

    def test_repair(self):
        room1 = Room("1A", "Vacant")
        room2 = Room("1B")
        assert room1.repair()
        assert room1.status == "Repair"
        with pytest.raises(RoomToBeRepair):
            room2.repair()

    def test_repaired(self):
        room1 = Room("1A", "Repair")
        room2 = Room("1B")
        assert room1.repaired()
        assert room1.status == "Vacant"
        with pytest.raises(RoomToBeVacant):
            room2.repaired()
