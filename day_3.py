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
    previous_node = node_sequence[0]
    
    for node in sequence:
        new_node = parse_input_node(previous_node, node)
        node_sequence.append(new_node)
        previous_node = new_node
    
    return node_sequence

def find_intersection(p1, p2, p3, p4):
    x12 = p1[0] - p2[0];
    x34 = p3[0] - p4[0];
    y12 = p1[1] - p2[1];
    y34 = p3[1] - p4[1];

    c = x12 * y34 - y12 * x34;

    if (abs(c) > 0.01):
        a = p1[0] * p2[1] - p1[1] * p2[0];
        b = p3[0] * p4[0] - p3[1] * p4[0];

        x = (a * x34 - b * x12) / c;
        y = (a * y34 - b * y12) / c;
        return (True, (int(x), int(y)))
    return (False, ())

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
    """
    prev_node_a = node_seq_a[0]
    prev_node_b = node_seq_b[0]

    intersections = []

    for node_a in node_seq_a[1:]:
        for node_b in node_seq_b[1:]:
            found, intersection = find_intersection(prev_node_a, node_a, prev_node_b, node_b)

            if found:
                intersections.append(intersection)

            prev_node_b = node_b
        prev_node_a = node_a

    return intersections

def func(seq_a, seq_b):
    """
    >>> func(['R8','U5','L5','D3'],['U7','R6','D4','L4'])
    """
    node_seq_a = parse_input_sequence(seq_a)
    node_seq_b = parse_input_sequence(seq_b)
    return find_intersections(node_seq_a, node_seq_b)

    pass

#------------------------------------------------------------------------------#
if __name__ == "__main__":
    import doctest
    doctest.testmod()