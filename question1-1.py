from main.main import Hotel


def main():
    # create hotel with 4 floors, each has 5 rooms, all default to Available
    hotel = Hotel(4)
    print("List all rooms that are Available:")
    print(hotel.list_available_rooms())
    print("Assign guestA - guestF each to a room:")
    guestA_room_num = hotel.assign_room()
    guests_room_num = []
    for i in range(5):
        guests_room_num.append(hotel.assign_room())
    print("After assigning rooms:")
    print(hotel.list_available_rooms())
    print("Get guestA room:")
    guestA_room = hotel.get_room(guestA_room_num)
    print(f"room num={guestA_room.number} status={guestA_room.status}")
    print("guestA checks out:")
    guestA_room.check_out()
    print(f"room num={guestA_room.number} status={guestA_room.status}")
    print(f"repair room {guestA_room_num}:")
    guestA_room.repair()
    print(f"room num={guestA_room.number} status={guestA_room.status}")
    print(f"finished repairing room {guestA_room_num}:")
    guestA_room.repaired()
    print(f"room num={guestA_room.number} status={guestA_room.status}")
    print(f"clean room {guestA_room_num}:")
    guestA_room.clean()
    print(f"room num={guestA_room.number} status={guestA_room.status}")
    print("After cleaning guestA room:")
    print(hotel.list_available_rooms())


if __name__ == "__main__":
    main()
