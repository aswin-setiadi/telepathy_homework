from main.main import Hotel


if __name__ == "__main__":
    hotel = Hotel(4)
    print(vars(hotel))
    print(hotel.list_available_rooms())
    print(hotel.assign_room())
    print(hotel.list_available_rooms())
