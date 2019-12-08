"""
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest intersection?
"""
#------------------------------------------------------------------------------#
import csv

def read_codes(filename):
    """
    >>> #read_codes('day_3_input.txt')
    """
    codes = []
    with open(filename, 'r') as f:
        codes = list(csv.reader(f, delimiter=','))
    return codes

#------------------------------------------------------------------------------#
direction_map = {
    'U': (0, 1),
    'D': (0,-1),
    'R': ( 1, 0),
    'L': (-1, 0)
}

def parse_input_node(origin, node):
    """
    >>> parse_input_node((0,0), 'U5')
    (0, 5)
    >>> parse_input_node((0,0), 'U10')
    (0, 10)
    >>> parse_input_node((0,0), 'D5')
    (0, -5)
    >>> parse_input_node((0,0), 'R10')
    (10, 0)
    >>> parse_input_node((1,1), 'R10')
    (11, 1)
    """
    direction = direction_map[node[0]]
    value = int(node[1:])

    scaled_delta = (direction[0] * value, direction[1] * value)
    new_node_position = (origin[0] + scaled_delta[0], origin[1] + scaled_delta[1])

    return new_node_position

def parse_input_sequence(sequence):
    """
    >>> parse_input_sequence(['R8','U5','L5','D3'])
    [(0, 0), (8, 0), (8, 5), (3, 5), (3, 2)]
    >>> parse_input_sequence(['U7','R6','D4','L4'])
    [(0, 0), (0, 7), (6, 7), (6, 3), (2, 3)]
    """
    node_sequence = [(0,0)]

    for node in sequence:
        new_node = parse_input_node(node_sequence[-1], node)
        node_sequence.append(new_node)

    return node_sequence

def contained(a, b, x):
    return min(a, b) < x < max(a, b)

def linear_interp_intersect(seg1, seg2):
    """"
    >>> linear_interp_intersect([(-2,1),(2,1)],[(0,0),(0,5)])
    (0, 1)
    >>> linear_interp_intersect([(2,1),(-2,1)],[(0,0),(0,5)])
    (0, 1)
    >>> linear_interp_intersect([(0,0),(5,0)],[(2,1),(2,-1)])
    (2, 0)
    >>> linear_interp_intersect([(2,1),(2,-1)],[(0,0),(5,0)])
    >>> linear_interp_intersect([(0,5),(0,0)],[(2,1),(-2,1)])
    >>> linear_interp_intersect([(0,0),(0,5)],[(2,1),(-2,1)])
    >>> linear_interp_intersect([(8, 0), (8, 5)], [(6, 3), (2, 3)])
    >>> linear_interp_intersect([(6, 3), (2, 3)], [(8, 0), (8, 5)])
    >>> linear_interp_intersect([(0, 0), (8, 0)], [(0, 0), (0, 7)])
    >>> linear_interp_intersect([(0, 0), (8, 0)], [(6, 7), (6, 3)])
    """
    x_intersect = contained(seg1[0][0], seg1[1][0], seg2[0][0])
    y_intersect = contained(seg2[0][1], seg2[1][1], seg1[0][1])

    if x_intersect and y_intersect:
        return (seg2[0][0], seg1[0][1])
    else:
        return None

def find_intersections(node_seq_a, node_seq_b):
    """
    >>> find_intersections([(-5,5), (5,5)], [(0,0), (0,10)])
    [(0, 5)]
    >>> find_intersections([(5,-5), (5,5)], [(0,0), (10,0)])
    [(5, 0)]
    >>> find_intersections([(-5,5), (5,5)], [(0,10), (0,0)])
    [(0, 5)]
    >>> find_intersections([(5,-5), (5,5)], [(10,0), (0,0)])
    [(5, 0)]
    >>> find_intersections([(5,5), (-5,5)], [(0,0), (0,10)])
    [(0, 5)]
    >>> find_intersections([(5,5), (5,-5)], [(0,0), (10,0)])
    [(5, 0)]
    >>> find_intersections([(5,5), (-5,5)], [(0,10), (0,0)])
    [(0, 5)]
    >>> find_intersections([(5,5), (5,-5)], [(10,0), (0,0)])
    [(5, 0)]
    >>> find_intersections([(5,5), (5,0)], [(10,0), (0,0)])
    []
    >>> find_intersections([(1,5), (5,5)], [(0,0), (0,10)])
    []
    >>> find_intersections([(0,0),(8,0),(8,5),(3,5),(3,2)],[(0,0),(0,7),(6,7),(6,3),(2,3)])
    [(6, 5), (3, 3)]
    """
    prev_node_a = node_seq_a[0]
    prev_node_b = node_seq_b[0]

    intersections = []

    for node_a in node_seq_a[1:]:
        for node_b in node_seq_b[1:]:
            # print([prev_node_a, node_a], [prev_node_b, node_b])
            intersection = linear_interp_intersect([prev_node_a, node_a], [prev_node_b, node_b])

            if intersection:
                # print([prev_node_a, node_a], [prev_node_b, node_b], intersection)
                intersections.append(intersection)

            # Check reverse
            intersection = linear_interp_intersect([prev_node_b, node_b], [prev_node_a, node_a])

            if intersection:
                # print([prev_node_b, node_b], [prev_node_a, node_a], intersection)
                intersections.append(intersection)

            prev_node_b = node_b
        prev_node_a = node_a
        prev_node_b = node_seq_b[0]

    return intersections

def find_minimal_tuple_sum(tuple_seq):
    return min([abs(tpl[0]) + abs(tpl[1]) for tpl in tuple_seq])

def find_manhattan_distance(seq_a, seq_b):
    """
    >>> find_manhattan_distance( \
        ['R8','U5','L5','D3'],['U7','R6','D4','L4'])
    6
    >>> find_manhattan_distance( \
        ['R75','D30','R83','U83','L12','D49','R71','U7','L72'], \
        ['U62','R66','U55','R34','D71','R55','D58','R83'])
    159
    >>> find_manhattan_distance( \
        ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'], \
        ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7'])
    135
    """
    node_seq_a = parse_input_sequence(seq_a)
    node_seq_b = parse_input_sequence(seq_b)

    intersections = find_intersections(node_seq_a, node_seq_b)

    nearest_node = find_minimal_tuple_sum(intersections)

    return nearest_node

def solve_fuel_wirring():
    """
    >>> solve_fuel_wirring()
    207
    """
    codes = read_codes('day_3_input.txt')
    return find_manhattan_distance(codes[0], codes[1])

"""
--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?
"""

def compute_cost(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_intersection_costs(node_seq_a, node_seq_b):
    prev_node_a = node_seq_a[0]
    prev_node_b = node_seq_b[0]
    cost_a = 0
    cost_b = 0

    intersection_costs = []

    for node_a in node_seq_a[1:]:
        for node_b in node_seq_b[1:]:
            intersection = linear_interp_intersect([prev_node_a, node_a], [prev_node_b, node_b])

            if intersection:
                intersection_costs.append((compute_cost(prev_node_a, intersection) + cost_a, \
                                          compute_cost(prev_node_b, intersection) + cost_b))

            # Check reverse
            intersection = linear_interp_intersect([prev_node_b, node_b], [prev_node_a, node_a])

            if intersection:
                intersection_costs.append((compute_cost(prev_node_a, intersection) + cost_a, \
                                          compute_cost(prev_node_b, intersection) + cost_b))

            cost_b += compute_cost(prev_node_b, node_b)
            prev_node_b = node_b
        cost_a += compute_cost(prev_node_a, node_a)
        prev_node_a = node_a
        prev_node_b = node_seq_b[0]
        cost_b = 0

    return intersection_costs

def find_closest_by_wire(seq_a, seq_b):
    """
    >>> find_closest_by_wire( \
        ['R8','U5','L5','D3'],['U7','R6','D4','L4'])
    30
    >>> find_closest_by_wire( \
        ['R75','D30','R83','U83','L12','D49','R71','U7','L72'], \
        ['U62','R66','U55','R34','D71','R55','D58','R83'])
    610
    >>> find_closest_by_wire( \
        ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'], \
        ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7'])
    410
    """
    node_seq_a = parse_input_sequence(seq_a)
    node_seq_b = parse_input_sequence(seq_b)

    intersection_costs = find_intersection_costs(node_seq_a, node_seq_b)

    return find_minimal_tuple_sum(intersection_costs)

def find_closest_fuel_wire():
    """
    >>> find_closest_fuel_wire()
    21196
    """
    codes = read_codes('day_3_input.txt')
    return find_closest_by_wire(codes[0], codes[1])

#------------------------------------------------------------------------------#
if __name__ == "__main__":
    import doctest
    doctest.testmod()