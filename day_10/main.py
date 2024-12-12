from utils import read_lines

SAMPLE_INPUT = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""



def solve_part1():

    map = []
    trail_heads = []
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        row_data = []
        for col, height in enumerate(report_line):
            height = int(height)
            row_data.append(height)
            if height == 0:
                trail_heads.append((row, col))
        map.append(row_data)
    
    trail_head_count  = 0
    for trail_head in trail_heads:
        process_list = [trail_head]
        
        nine_height_reacheable = list()
        while process_list:
            row, col = process_list.pop()
            target_height = map[row][col] + 1
            if target_height == 10:
                nine_height_reacheable.append((row, col))
                continue
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj_row, adj_col = row + dr, col + dc
                if 0 <= adj_row < len(map) and 0 <= adj_col < len(map[0]):
                    if map[adj_row][adj_col] == target_height:
                        # print(f'({row}, {col} [{target_height-1}]) -> ({adj_row}, {adj_col}) [{target_height}]')
                        process_list.append((adj_row, adj_col))

        print(f'Number of trails for trail head {trail_head}: {len(nine_height_reacheable)}')
        trail_head_count += len(nine_height_reacheable)

    print(f'Total number of trails: {trail_head_count}')


if __name__ == "__main__":
    solve_part1()
