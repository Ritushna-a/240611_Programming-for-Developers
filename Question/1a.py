from collections import defaultdict
import math

def max_points_on_line(customer_locations):
    if len(customer_locations) < 3:
        return len(customer_locations)

    max_points = 0

    for i in range(len(customer_locations)):
        slopes = defaultdict(int)
        x1, y1 = customer_locations[i]
        duplicates = 1

        for j in range(i + 1, len(customer_locations)):
            x2, y2 = customer_locations[j]
            dx = x2 - x1
            dy = y2 - y1

            if dx == 0 and dy == 0:
                duplicates += 1
                continue

            gcd = math.gcd(dx, dy)
            dx //= gcd
            dy //= gcd

            slopes[(dx, dy)] += 1
            max_points = max(max_points, slopes[(dx, dy)] + duplicates)

    return max_points
