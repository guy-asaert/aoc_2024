from utils import read_lines
from collections import namedtuple
from dataclasses import dataclass

SAMPLE_INPUT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


# Robot = namedtuple('Robot', ['loc_x', 'loc_y', 'velocity_x', 'velocity_y']) 

@dataclass
class Robot:
    loc_x: int
    loc_y: int
    velocity_x: int
    velocity_y: int

def solve_part1():

    robots = []
    # width = 11
    # height = 7
    width = 101
    height = 103
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        loc, velocity = report_line.split(" ")
        loc_x ,loc_y = int(loc[2:].split(",")[0]), int(loc[2:].split(",")[1])
        velocity_x, velocity_y = int(velocity[2:].split(",")[0]), int(velocity[2:].split(",")[1])
        robots.append(Robot(loc_x, loc_y, velocity_x, velocity_y))

    for i in range(100):
        for robot in robots:
            robot.loc_x = (robot.loc_x + robot.velocity_x) % width
            robot.loc_y  = (robot.loc_y + robot.velocity_y) % height
    
    quadrant_count = [0, 0, 0, 0]
    for robot in robots:
        if robot.loc_x < width // 2 and robot.loc_y < height // 2:
            quadrant_count[0] += 1
        elif robot.loc_x > width // 2 and robot.loc_y < height // 2:
            quadrant_count[1] += 1
        elif robot.loc_x < width // 2 and robot.loc_y > height // 2:
            quadrant_count[2] += 1
        elif robot.loc_x > width // 2 and robot.loc_y > height // 2:
            quadrant_count[3] += 1

    print(f'Safety factor is {quadrant_count[0] * quadrant_count[1] * quadrant_count[2] * quadrant_count[3]}')


def show_robots(f, iteration, robots, width, height): 
    coordinates = {(robot.loc_x, robot.loc_y) for robot in robots}
    output = []

    output.append(f"Iteration {iteration}")
    for y in range(height):
        line = []
        for x in range(width):
            if (x, y) in coordinates:
                line.append("#")
            else:
                line.append(".")
        output.append("".join(line))
    output.append("\n")
    f.write("\n".join(output))
    

def solve_part2():
    robots = []
    # width = 11
    # height = 7
    width = 101
    height = 103
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        loc, velocity = report_line.split(" ")
        loc_x ,loc_y = int(loc[2:].split(",")[0]), int(loc[2:].split(",")[1])
        velocity_x, velocity_y = int(velocity[2:].split(",")[0]), int(velocity[2:].split(",")[1])
        robots.append(Robot(loc_x, loc_y, velocity_x, velocity_y))

    continue_search = True
    iteration = 0
    with open("output.txt", "w") as f:
        for i in range(width * height):
            iteration +=1
            for robot in robots:
                robot.loc_x = (robot.loc_x + robot.velocity_x) % width
                robot.loc_y  = (robot.loc_y + robot.velocity_y) % height

            centralised_robots = set()
            for robot in robots:
                if robot.loc_x == width // 2 + 1:
                    centralised_robots.add(robot.loc_y)

            show_robots(f, iteration, robots, width, height)
            # if len(centralised_robots) > height * 0.5:
            #     print(f"Found at iteration {iteration}") 

            if iteration % 1000 == 0:
                print(f"Iteration {iteration}")
            # show_robots(robots, width, height)


if __name__ == "__main__":
    solve_part2()
