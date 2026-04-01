# dollar_amt = 32779.77
# conversion_rate = 5.4794496
# hours = [940]
# rate_blr = [180.28]

# dollar_amt = 159898.32
# conversion_rate = 5.4794503
# hours = [1880, 1880, 940]
# rate_blr = [226.45, 123.12, 180.28]

# dollar_amt = 293815.40
# conversion_rate = 5.4794507
# hours = [1880, 1880, 1880, 1880, 1880, 1880]
# rate_blr = [123.12, 87.94, 183.58, 123.12, 167.09, 123.12]

# dollar_amt = 32864.25
# conversion_rate = 5.4794503
# hours = [450, 450]
# rate_blr = [152.80, 226.45]

# dollar_amt = 72461.83
# conversion_rate = 5.4794503
# hours = [472, 472, 472, 472, 472]
# rate_blr = [180.28, 134.11, 197.87, 167.09, 114.33]


# dollar_amt = 40983.79
# conversion_rate = 5.4794
# hours = [500, 800]
# rate_blr = [180.28, 152.80]

# dollar_amt = 525257.12
# conversion_rate = 5.4794
# hours = [1880, 1880, 1880, 940, 1880, 1880, 1880, 1880, 1880, 960, 940]
# rate_blr = [
#     134.11,
#     152.80,
#     197.87,
#     167.09,
#     83.54,
#     197.87,
#     197.87,
#     123.12,
#     111.03,
#     197.87,
#     123.12,
# ]


dollar_amt = 202096.67
conversion_rate = 5.4794520
hours = [792, 952, 952, 952, 472, 1720, 472]
rate_blr = [152.80, 123.12, 226.45, 226.45, 80.25, 134.11, 226.45]
month_list = [6, 7, 7, 7, 7, 11, 3]


blr_amm = round(dollar_amt * conversion_rate, 2)
rate_dlr = [round(r / conversion_rate, 2) for r in rate_blr]
DELTA = 0.01


def calculate_tax(amm):
    return round(amm * 0.05988341282458, 2)


def compute_total(data):
    total_before_tax = 0
    total_tax = 0
    for i in range(0, len(data)):
        h = data[i]
        rate_blr_i = rate_blr[i]
        total_amm_before_tax = round(rate_blr_i * h, 2)
        total_before_tax += total_amm_before_tax
        total_tax += calculate_tax(total_amm_before_tax)

    # print("total_before_tax-->", total_before_tax)
    # print("total_tax-->", total_tax)

    return round(total_before_tax + total_tax, 2)


def compute_total_dollar(data):
    total_before_tax = 0
    total_tax = 0
    for i in range(0, len(data)):
        h = data[i]
        rate_dollar_i = rate_blr[i] / conversion_rate
        total_amm_before_tax = round(rate_dollar_i * h, 2)
        total_before_tax += total_amm_before_tax
        total_tax += calculate_tax(total_amm_before_tax)
    return round(total_before_tax + total_tax, 2)


def calculate_delta(total, target):
    """
    Calculate DELTA adjustment based on difference between total and target.

    Args:
        total (float): Current calculated total
        target (float): Target amount to match

    Returns:
        float: DELTA adjustment value
    """
    abs_diff = abs(total - target)

    if total > target:
        if abs_diff <= 0.01:
            return -0.00001  # Fine adjustment
        elif abs_diff <= 0.1:
            return -0.0001  # Medium adjustment
        elif abs_diff <= 1.0:
            return -0.001  # Coarse adjustment
        else:
            return -0.01
    elif total < target:
        if abs_diff <= 0.01:
            return 0.00001  # Fine adjustment
        elif abs_diff <= 0.1:
            return 0.0001  # Medium adjustment
        elif abs_diff <= 1.0:
            return 0.001  # Coarse adjustment
        else:
            return 0.01

    return 0.0  # Exact match


def divide_values(values, divisions):
    """
    Divide each value into parts where all parts are integers except ONE that gets the decimal remainder.
    Parts are uneven but not too different, max is 180.

    Args:
        values: List of float values to divide
        divisions: List of integers specifying how many parts for each value

    Returns:
        List of lists, where each inner list contains the divided parts
    """
    result = []

    for value, num_parts in zip(values, divisions):
        # Get integer and decimal parts
        integer_part = int(value)
        decimal_part = value - integer_part

        # Distribute integer part
        base = integer_part // num_parts
        extra = integer_part % num_parts

        parts = []

        # Give base value to all parts
        for i in range(num_parts):
            parts.append(base)

        # Distribute the extra integers to some parts
        extra_indices = random.sample(range(num_parts), min(extra, num_parts))
        for idx in extra_indices:
            parts[idx] += 1

        # Make parts slightly uneven by transferring between them
        for _ in range(num_parts // 2):
            i = random.randint(0, num_parts - 1)
            j = random.randint(0, num_parts - 1)
            if i != j and parts[i] > 1:
                transfer = random.randint(1, min(5, parts[i] // 2))
                if parts[j] + transfer <= 180:  # Respect max limit
                    parts[i] -= transfer
                    parts[j] += transfer

        # Pick random index for decimal remainder
        decimal_idx = random.randint(0, num_parts - 1)
        parts[decimal_idx] = round(parts[decimal_idx] + decimal_part, 5)

        result.append(parts)

    return result


def recurse(data, index=0, depth=0, blr_first=True):
    if depth > 980:  # Adjust this limit as needed
        return False

    DELTA = 0.0001

    # ------------------------------------------------------------------------------------------------------------------------
    if blr_first == True:
        total_blr = compute_total(data)
        DELTA = calculate_delta(total_blr, blr_amm)
        if total_blr == blr_amm:
            total_dollar = compute_total_dollar(data)
            if total_dollar == dollar_amt:
                return True

    else:
        # -----------------------------------------------------------------------------------------------
        total_dollar = compute_total_dollar(data)
        DELTA = calculate_delta(total_dollar, dollar_amt)
        if total_dollar == dollar_amt:
            total_blr = compute_total(data)
            if total_blr == blr_amm:
                month_dist = divide_values(data, month_list)
                return True

    # --------------------------------------------------------------------------------------------------------

    if index >= len(data):
        return False

    original = data[index]  # ← Use data[index], not hours[index]

    data[index] = round(original + DELTA, 5)
    if recurse(
        data, (index + 1) % len(data), depth + 1, blr_first
    ):  # Move to next index
        return True
    return False


# recurse(hours.copy())


import random


def find_multiple_solutions(hours, num_solutions=1):
    all_solutions = []
    for attempt in range(num_solutions * 100):  # Try multiple times
        perturbed = [h + random.uniform(-10, 10) for h in hours]
        solution = recurse(perturbed.copy(), 0, 0, False)
        if solution and solution not in all_solutions:
            all_solutions.append(solution)

        if len(all_solutions) >= num_solutions:
            break

    return all_solutions


total_blr_with_curent_hours = compute_total(hours)
print()
solutions = find_multiple_solutions(hours, num_solutions=5)
