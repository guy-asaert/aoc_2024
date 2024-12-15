from utils import read_lines
from dataclasses import dataclass
from collections import namedtuple

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


def print_double_width_warehouse(robot, walls, boxes):
    width = max([x.x for x in walls]) + 1
    height = max([x.y for x in walls]) + 1
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
        print(row_string)
        # print()

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
        

def process_moving_thing_wide(x, y, direction, walls, boxes, last_collision_box_index=-1):

    for wall in walls:
        if (last_collision_box_index == -1 and wall.y == y and wall.x <= x <= wall.x + 1) or \
           (last_collision_box_index != -1 and wall.y == y and abs(wall.x -x) < 2):
            return False

    can_move = True
    movements = []
    for box_index, box in enumerate(boxes):
        if box_index == last_collision_box_index:
            continue
        if (last_collision_box_index == -1 and box.y == y and box.x <= x <= box.x + 1) or \
           (last_collision_box_index != -1 and box.y == y and abs(box.x -x) < 2):
            # collide with box        
            move_x, move_y = move_object(box, direction)
            if process_moving_thing_wide(move_x, move_y, direction, walls, boxes, box_index):
                movements.append((box_index, move_x, move_y)) 
            else:
                can_move = False

    if can_move:
        for box_index, move_x, move_y in movements:
            boxes[box_index].x = move_x
            boxes[box_index].y = move_y

    return can_move # no obstacles

SAMPLE_INPUT_WIDE = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

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

    for move_index, move in enumerate(robot_moves):
        x, y = move_object(robot, move)
        # if move_index == 94:
        #     print("check this")

        if process_moving_thing_wide(x, y, move, walls, boxes):
            robot = Positionable(x, y)
        
        # print((f'Move: ({move_index}) {move}'))
        # print_double_width_warehouse(robot, walls, boxes)
        # pass

    print(f'Completed {move_index + 1} moves')
    print_double_width_warehouse(robot, walls, boxes)

    sum_of_gps_coordinates = 0
    for box in boxes:
        sum_of_gps_coordinates += box.x + 100 * box.y

    print(sum_of_gps_coordinates)    

if __name__ == "__main__":
    solve_part2()

# 1352076 is too low