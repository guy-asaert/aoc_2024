from utils import read_lines
import itertools
from collections import defaultdict, Counter

SAMPLE_INPUT = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""


NEIGHTBOURS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find_region(garden_plots, plot):
    region = [plot]

    neighbour_seach = [plot]
    while neighbour_seach:
        plot = neighbour_seach.pop(0)
        for neighbour in NEIGHTBOURS:
            neighbour_plot = (plot[0] + neighbour[0], plot[1] + neighbour[1], plot[2])
            if neighbour_plot in garden_plots:
                garden_plots.remove(neighbour_plot)
                region.append(neighbour_plot)
                neighbour_seach.append(neighbour_plot)
    return region

def get_all_regions(garden_plots):
    regions = []
    while garden_plots:
        plot = garden_plots.pop(0)
        region = find_region(garden_plots, plot)
        regions.append(region)
    return regions

def solve_part1(regions):
    # now determine the perimeter of the regions
    price = 0

    for region in regions:
        adjacent_plots = 0
        for plot1, plot2 in itertools.combinations(region, 2):
            if abs(plot1[0] - plot2[0]) + abs(plot1[1] - plot2[1]) == 1:
                adjacent_plots += 1
    
        perimeter = len(region) * 4 - 2 * adjacent_plots
        price += perimeter * len(region)

    print(f'Part 1: {price}')

def solve_part2(regions, garden_width, garden_height):
    #  determine how many perimeter the regions have
    price = 0
    for region in regions:
        row_perimeters = defaultdict(lambda: defaultdict(list))
        col_perimeters = defaultdict(lambda: defaultdict(list))
        for plot in region:
            row_perimeters[plot[0]][plot[1]].append('t')
            row_perimeters[plot[0] + 1][plot[1]].append('b')
            col_perimeters[plot[1]][plot[0]].append('l')
            col_perimeters[plot[1] + 1][plot[0]].append('r')
        
        row_fences = 0
        for row, row_counter in row_perimeters.items():
            on_perimeter = False
            fence_direction = None
            for col in range(garden_width):
                if len(row_counter.get(col, [])) == 1:
                    if not on_perimeter:
                        row_fences += 1
                        on_perimeter = True
                        fence_direction = row_counter[col][0]
                    elif fence_direction != row_counter[col][0]:
                        row_fences += 1
                        fence_direction = row_counter[col][0]
                elif on_perimeter:
                    on_perimeter = False

        col_fences = 0
        for col, col_counter in col_perimeters.items():
            on_perimeter = False
            fence_direction = None
            for row in range(garden_height):
                if len(col_counter.get(row, [])) == 1:
                    if not on_perimeter:
                        col_fences += 1
                        on_perimeter = True
                        fence_direction = col_counter[row][0]
                    elif fence_direction != col_counter[row][0]:
                        col_fences += 1
                        fence_direction = col_counter[row][0]
                elif on_perimeter:
                    on_perimeter = False

        # print(f'Region: {perimeters * len(region)}')
        price += (row_fences + col_fences) * len(region)

    print(f'Part 2: {price}')

if __name__ == "__main__":
    garden_plots = []
    
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        garden_plots.extend((row, col, plot) for col, plot in enumerate(report_line))   
    
    garden_width = max(plot[1] for plot in garden_plots) + 1
    garden_height = max(plot[0] for plot in garden_plots) + 1    
    # solve_part1(get_all_regions(garden_plots))
    solve_part2(get_all_regions(garden_plots), garden_width, garden_height)

# 942774 is too low
