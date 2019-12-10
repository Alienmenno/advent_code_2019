"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 256310-732736.
"""
#------------------------------------------------------------------------------#
def int_to_char_list(val):
    """
    >>> int_to_char_list(10)
    ['1', '0']
    >>> int_to_char_list(1234)
    ['1', '2', '3', '4']
    """
    return list(str(val))

def check_for_digit_pairs(int_list):
    """
    >>> check_for_digit_pairs(['1', '1'])
    True
    >>> check_for_digit_pairs(['1', '1', '1', '1'])
    True
    >>> check_for_digit_pairs(['1', '0'])
    False
    >>> check_for_digit_pairs(['1', '0', '2', '1'])
    False
    """
    return any([a == b for a, b in zip(int_list, int_list[1:])])

def check_for_acending_order(int_list):
    """
    >>> check_for_acending_order(['1', '1', '1', '1'])
    True
    >>> check_for_acending_order(['1', '2', '3', '4'])
    True
    >>> check_for_acending_order(['3', '2', '1', '0'])
    False
    >>> check_for_acending_order(['1', '0', '1', '2'])
    False
    """
    return int_list == sorted(int_list)

def check_passcode_validity(passcode_nr):
    """
    >>> check_passcode_validity(1111)
    True
    >>> check_passcode_validity(1134)
    True
    >>> check_passcode_validity(2100)
    False
    >>> check_passcode_validity(1234)
    False
    """
    passcode_chars = int_to_char_list(passcode_nr)
    return check_for_digit_pairs(passcode_chars) \
       and check_for_acending_order(passcode_chars)

def find_valid_passcodes_in_range(start, end, pass_check=check_passcode_validity):
    """
    >>> find_valid_passcodes_in_range(10, 12)
    [11]
    >>> find_valid_passcodes_in_range(100, 113)
    [111, 112, 113]
    >>> find_valid_passcodes_in_range(12, 19)
    []
    """
    return [p for p in range(start, end+1) if pass_check(p)]

def split_range_input(range_input):
    """
    >>> split_range_input("256310-732736")
    [256310, 732736]
    """
    return list(map(int, range_input.split('-')))

def count_number_of_valid_passcodes(range_input):
    """
    >>> count_number_of_valid_passcodes("256310-732736")
    979
    """
    passcode_range = split_range_input(range_input)
    valid_passcodes = find_valid_passcodes_in_range(passcode_range[0],
                                                    passcode_range[1])
    return len(valid_passcodes)

#------------------------------------------------------------------------------#
"""
--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?
"""

from itertools import groupby

def check_for_even_digit_pairs(int_list):
    """
    >>> check_for_even_digit_pairs(['1', '1'])
    True
    >>> check_for_even_digit_pairs(['1', '1', '2', '2', '3', '3'])
    True
    >>> check_for_even_digit_pairs(['1', '1', '1', '1', '2', '2'])
    True
    >>> check_for_even_digit_pairs(['1', '1', '1', '1'])
    False
    >>> check_for_even_digit_pairs(['1', '1', '1', '4'])
    False
    >>> check_for_even_digit_pairs(['1', '0'])
    False
    >>> check_for_even_digit_pairs(['1', '0', '2', '1'])
    False
    >>> check_for_even_digit_pairs(['1', '2', '3', '4', '4', '4'])
    False
    """
    duplicate_sequences = [len(list(group)) for _, group in groupby(int_list)]
    return any((t == 2) for t in duplicate_sequences)

def recheck_passcode_validity(passcode_nr):
    """
    >>> recheck_passcode_validity(1134)
    True
    >>> recheck_passcode_validity(1111)
    False
    >>> recheck_passcode_validity(1114)
    False
    >>> recheck_passcode_validity(2100)
    False
    >>> recheck_passcode_validity(1234)
    False
    """
    passcode_chars = int_to_char_list(passcode_nr)
    return check_for_even_digit_pairs(passcode_chars) \
       and check_for_acending_order(passcode_chars)

def recount_number_of_valid_passcodes(range_input):
    """
    >>> recount_number_of_valid_passcodes("256310-732736")
    635
    """
    passcode_range = split_range_input(range_input)
    valid_passcodes = find_valid_passcodes_in_range(passcode_range[0],
                                                    passcode_range[1],
                                                    recheck_passcode_validity)
    return len(valid_passcodes)

#------------------------------------------------------------------------------#
if __name__ == "__main__":
    import doctest
    doctest.testmod()