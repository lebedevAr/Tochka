import json


def check_capacity(max_capacity: int, guests: list) -> bool:
    events = []
    for guest in guests:
        events.append((guest["check-in"], 1))
        events.append((guest["check-out"], -1))

    # Сортируем события по дате
    events.sort()

    current_guests = 0
    for event in events:
        current_guests += event[1]
        if current_guests > max_capacity:
            return False

    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)

