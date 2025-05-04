import sys

import collections


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def min_steps_to_collect_all_keys(data):
    main_graph = collections.defaultdict(set)
    keys = collections.defaultdict(str)

    doors = collections.defaultdict(lambda: (0, 0))

    dead_ends = collections.deque()
    queue = collections.deque()
    queue.append((0, 0))

    robots = set()
    visited_points = set()
    points = set()

    height = len(data)
    width = len(data[0])

    while True:
        if not queue:
            break

        cur_pos = queue.popleft()
        if cur_pos in visited_points:
            continue

        visited_points.add(cur_pos)
        points.clear()

        if cur_pos[0] < height - 1:
            queue.append((cur_pos[0] + 1, cur_pos[1]))
            points.add((cur_pos[0] + 1, cur_pos[1]))

        if cur_pos[0] > 0:
            points.add((cur_pos[0] - 1, cur_pos[1]))

        if cur_pos[1] < width - 1:
            queue.append((cur_pos[0], cur_pos[1] + 1))
            points.add((cur_pos[0], cur_pos[1] + 1))

        if cur_pos[1] > 0:
            points.add((cur_pos[0], cur_pos[1] - 1))


        for point in points:
            if data[point[0]][point[1]] != "#":
                main_graph[cur_pos].add(point)

        cur_val = data[cur_pos[0]][cur_pos[1]]

        if cur_val == '#':
            continue
        elif cur_val == '@':
            robots.add(cur_pos)
        elif cur_val.islower():
            keys[cur_pos] = cur_val
        elif cur_val.isupper():
            doors[cur_val] = cur_pos
        else:
            pass

        if len(main_graph[cur_pos]) < 2 and cur_pos not in keys.keys() and cur_pos not in robots:
            dead_ends.append(cur_pos)

    visited_points.clear()


    while True:
        if not dead_ends:
            break

        cur_pos = dead_ends.popleft()
        if len(main_graph[cur_pos]) > 1 or cur_pos in keys.keys() or cur_pos in robots:
            continue

        for point in main_graph[cur_pos]:
            main_graph[point].remove(cur_pos)
            dead_ends.appendleft(point)


    doors_unlocked = set()


    while True:
        delta = 0
        for robot in robots:
            queue.append(robot)
            visited_points.add(robot)

            while True:
                if not queue:
                    break

                cur_pos = queue.popleft()

                if cur_pos in doors.values() and cur_pos not in doors_unlocked:
                    continue

                if cur_pos in keys.keys() and doors[keys[cur_pos].upper()] not in doors_unlocked:
                    delta += 1
                    doors_unlocked.add(doors[keys[cur_pos].upper()])

                for v in main_graph[cur_pos]:
                    if v in visited_points:
                        continue
                    visited_points.add(v)
                    queue.append(v)

            visited_points.clear()

        if len(doors_unlocked) >= len(doors.values()) and len(doors_unlocked) >= len(keys.keys()):
            break

        if delta == 0:
            return -1

    visited_points.clear()
    steps_count = 0

    for robot in robots:
        queue.append((robot, 0))
        visited_points.add(robot)

        while True:
            if not queue:
                break

            cur_pos, cur_way = queue.popleft()

            if cur_pos in doors.values() and cur_pos not in doors_unlocked:
                continue

            if cur_pos in keys.keys():
                doors_unlocked.add(doors[keys[cur_pos].upper()])
                if len(main_graph[cur_pos]) > 1:
                    pass
                elif len(queue) == 0:
                    steps_count += cur_way
                    continue
                else:
                    steps_count += cur_way * 2
                    continue

            if len(main_graph[cur_pos]) > 2:
                if len(queue) > 0:
                    steps_count += cur_way * 2
                else:
                    steps_count += cur_way
                cur_way = 0

            for v in main_graph[cur_pos]:
                if v in visited_points:
                    continue
                visited_points.add(v)
                queue.append((v, cur_way + 1))

    return steps_count


def solve(data):
    return min_steps_to_collect_all_keys(data)


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()