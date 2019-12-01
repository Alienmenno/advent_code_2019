"""
--- Day 1: The Tyranny of the Rocket Equation ---

Santa has become stranded at the edge of the Solar System while delivering presents to other planets! To accurately calculate his position in space, safely align his warp drive, and return to Earth in time to save Christmas, he needs you to bring him measurements from fifty stars.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

The Elves quickly load you into a spacecraft and prepare to launch.

At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper. They haven't determined the amount of fuel required yet.

Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

For example:

    For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
    For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
    For a mass of 1969, the fuel required is 654.
    For a mass of 100756, the fuel required is 33583.

The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

What is the sum of the fuel requirements for all of the modules on your spacecraft?
"""
from math import floor

def calc_fuel_load_per_module(module_mass):
    """
    >>> calc_fuel_load_per_module(12)
    2
    >>> calc_fuel_load_per_module(14)
    2
    >>> calc_fuel_load_per_module(1969)
    654
    >>> calc_fuel_load_per_module(100756)
    33583
    """
    return floor(module_mass / 3) - 2

def calc_fuel_load_for_modules(modules):
    """
    >>> calc_fuel_load_for_modules([12, 14])
    4
    >>> calc_fuel_load_for_modules([1969, 100756])
    34237
    """
    return sum([calc_fuel_load_per_module(m) for m in modules])

def read_modules(filename):
    with open(filename) as f:
        return [int(x) for x in f]

def calc_fuel_load_for_modules_in_file(filename='day_1_input.txt'):
    """
    >>> calc_fuel_load_for_modules_in_file()
    3234871
    """
    module_list = read_modules(filename)
    return calc_fuel_load_for_modules(module_list)

#------------------------------------------------------------------------------#
"""
--- Part Two ---

During the second Go / No Go poll, the Elf in charge of the Rocket Equation Double-Checker stops the launch sequence. Apparently, you forgot to include additional fuel for the fuel you just added.

Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.

So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. For example:

    A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.
    At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
    The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.

What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the mass of the added fuel? (Calculate the fuel requirements for each module separately, then add them all up at the end.)
"""

def calc_total_fuel_load_per_module(module_mass):
    """
    >>> calc_total_fuel_load_per_module(14)
    2
    >>> calc_total_fuel_load_per_module(1969)
    966
    >>> calc_total_fuel_load_per_module(100756)
    50346
    """
    fuel_load = floor(module_mass / 3) - 2
    if fuel_load <= 0:
        return 0
    else:
        return fuel_load + calc_total_fuel_load_per_module(fuel_load)

def calc_total_fuel_load_for_modules(modules):
    """
    >>> calc_total_fuel_load_for_modules([12, 14])
    4
    >>> calc_total_fuel_load_for_modules([1969, 100756])
    51312
    """
    return sum([calc_total_fuel_load_per_module(m) for m in modules])

def calc_total_fuel_load_for_modules_in_file(filename='day_1_input.txt'):
    """
    >>> calc_total_fuel_load_for_modules_in_file()
    4849444
    """
    module_list = read_modules(filename)
    return calc_total_fuel_load_for_modules(module_list)

if __name__ == "__main__":
    import doctest
    doctest.testmod()