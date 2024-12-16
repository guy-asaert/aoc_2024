from utils import read_lines
from dataclasses import dataclass
from collections import namedtuple
import copy

SAMPLE_INPUT = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""


wall = namedtuple("wall", ["x", "y"])

@dataclass
class Positionable:
    x: int
    y: int
    is_robot: bool = False

    def __repr__(self):
        return f"({self.x}, {self.y})"

@dataclass
class Tracker:
    boxes_moved: int = 0


def print_warehouse(robot, walls, boxes):
    width = max([x.x for x in walls]) + 1
    height = max([x.y for x in walls]) + 1
    for y in range(height):
        for x in range(width):
            if robot.x == x and robot.y == y:
                print("@", end="")
            elif Positionable(x, y) in boxes:
                print("O", end="")
            elif wall(x, y) in walls:
                print("#", end="")
            else:
                print(".", end="")
        print()

    print()


def print_double_width_warehouse(robot, walls, boxes, file_handle=None):
    width = max([x.x for x in walls]) + 1
    height = max([x.y for x in walls]) + 1

    ware_house_state = []
    for y in range(height):
        x = 0
        row_string = ""
        while x < width:
            if robot.x == x and robot.y == y:
                row_string += "@"
                # print("@", end="")
                x += 1
            elif Positionable(x, y) in boxes:
                row_string += "[]"
                # print("[]", end="")
                x += 2
            elif wall(x, y) in walls:
                row_string += "##"
                # print("##", end="")
                x += 2
            else:
                row_string += "."
                # print(".", end="")
                x += 1
        ware_house_state.append(row_string)

    if file_handle:
        file_handle.write("\n".join(ware_house_state))
        file_handle.write("\n")
    else:
        print("\n".join(ware_house_state))
        print()

def move_object(object, move):
    if move == "^":
        return (object.x, object.y-1)
    elif move == "v":
        return (object.x, object.y+1)
    elif move == "<":
        return (object.x-1, object.y)
    elif move == ">":
        return (object.x+1, object.y)
    else:
        raise ValueError(f"Invalid move: {move}")

def process_moving_thing(x, y, direction, walls, boxes):

    if wall(x, y) in walls:
        return False

    if Positionable(x, y) in boxes:
        colliding_box = boxes[boxes.index(Positionable(x, y))]
        move_x, move_y = move_object(colliding_box, direction)
        if process_moving_thing(move_x, move_y, True, direction, walls, boxes):
            colliding_box.x = move_x
            colliding_box.y = move_y
            return True
        else:
            return False

    return True # no obstacles



def solve_part1():
    robot_moves = ""
    walls = []
    boxes = []
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        if not report_line:
            continue
        elif '>' in report_line or '<' in report_line or '^' in report_line or 'v' in report_line:
            robot_moves += report_line
        else:
            for col, char in enumerate(report_line):
                if char == "@":
                    robot = Positionable(x=col, y=row, is_robot=True)
                elif char == "#":
                    walls.append(wall(x=col, y=row))
                elif char == "O":
                    boxes.append(Positionable(x=col, y=row))

    for move in robot_moves:
        x, y = move_object(robot, move)
        if process_moving_thing(x, y, move, walls, boxes):
            robot = Positionable(x, y)
        # print_warehouse(robot, walls, boxes)

    sum_of_gps_coordinates = 0
    for box in boxes:
        sum_of_gps_coordinates += box.x + 100 * box.y

    print(sum_of_gps_coordinates)
        

def process_moving_thing_wide(x, y, direction, walls, boxes, tracker, box_movements, last_collision_box_index=-1):

    for wall in walls:
        if (last_collision_box_index == -1 and wall.y == y and wall.x <= x <= wall.x + 1) or \
           (last_collision_box_index != -1 and wall.y == y and abs(wall.x -x) < 2):
            return False

    can_move = True
    boxes_moved = 0
    for box_index, box in enumerate(boxes):
        if box_index == last_collision_box_index:
            continue
        if (last_collision_box_index == -1 and box.y == y and box.x <= x <= box.x + 1) or \
           (last_collision_box_index != -1 and box.y == y and abs(box.x -x) < 2):
            # collide with box
            boxes_moved += 1
            move_x, move_y = move_object(box, direction)
            if process_moving_thing_wide(move_x, move_y, direction, walls, boxes, tracker, box_movements, box_index):
                box_movements.add((box_index, move_x, move_y)) 
            else:
                can_move = False



    return can_move # no obstacles

SAMPLE_INPUT_WIDE = """##########
#........#
#........#
#.....#..#
#...OOO..#
#...OO...#
#..@O....#
#........#
#........#
##########

>>><<^><vv>>>^"""


def result(boxes):
    gps_coords = sum([box.x + 100 * box.y for box in boxes])
    return gps_coords

def solve_part2():
    """ Double width walls and boxes """
    robot_moves = ""
    walls = []
    boxes = []

    # for row, report_line in enumerate(SAMPLE_INPUT_WIDE.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        if not report_line:
            continue
        elif '>' in report_line or '<' in report_line or '^' in report_line or 'v' in report_line:
            robot_moves += report_line
        else:
            for col, char in enumerate(report_line):
                if char == "@":
                    robot = Positionable(x=2*col, y=row, is_robot=True)
                elif char == "#":
                    walls.append(wall(x=2*col, y=row))
                elif char == "O":
                    boxes.append(Positionable(x=2*col, y=row))

    print_double_width_warehouse(robot, walls, boxes)

    max_boxes_moved = 0
    print(f'We have {len(boxes)} boxes')
    with open("day_15/warehouse.txt", "w") as f:
        for move_index, move in enumerate(robot_moves):
            x, y = move_object(robot, move)
            tracker = Tracker()
            box_movements = set()
            if process_moving_thing_wide(x, y, move, walls, boxes, tracker, box_movements):
                robot = Positionable(x, y)
                for box_index, move_x, move_y in box_movements:
                    boxes[box_index].x = move_x
                    boxes[box_index].y = move_y

            # print(f'Completed {move_index + 1} moves')
            # print_double_width_warehouse(robot, walls, boxes)

        # print(f'Max boxes moved: {max_boxes_moved}')
        print(f'Result {result(boxes)}.')

if __name__ == "__main__":
    solve_part2()

# 1352076 is too low
