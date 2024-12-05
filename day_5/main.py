from utils import read_lines
import re

SAMPLE_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def solve_part1():
    # Read the input

    sort_order = list()
    the_first_answer = 0
    the_second_answer = 0
    # for report_line in SAMPLE_INPUT.split("\n"):
    for report_line in read_lines(__file__):
        order_line = report_line.split("|")
        if len(order_line) == 2:
            sort_order.append((int(order_line[0]), int(order_line[1])))
        elif report_line:
            print_pages = [int(p) for p in report_line.split(",")]

            order_is_good = True
            for index in range(1, len(print_pages)):
                if not (print_pages[index - 1], print_pages[index]) in sort_order:
                    order_is_good = False
                    break

            if order_is_good:
                the_first_answer += print_pages[len(print_pages)//2]
            else: # second part
                keep_going = True
                while keep_going:
                    keep_going = False
                    for index in range(1, len(print_pages)):
                        first_page, second_page = print_pages[index - 1], print_pages[index]
                        if (second_page, first_page) in sort_order: # swap
                            print_pages[index - 1], print_pages[index] = second_page, first_page
                            keep_going = True
                # now check in order
                order_is_good = True
                for index in range(1, len(print_pages)):
                    if not (print_pages[index - 1], print_pages[index]) in sort_order:
                        order_is_good = False
                        break
                if order_is_good:
                    the_second_answer += print_pages[len(print_pages)//2]

    print(f'The first answer is {the_first_answer}. The second answer is {the_second_answer}')
            
def solve_part2():
    pass

if __name__ == "__main__":
    solve_part1()

# 1919 is too low

