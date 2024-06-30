import random
from typing import List, Tuple

def generate_rectilinear_polygon(min_points: int = 8, max_points: int = 20) -> List[Tuple[int, int]]:
    def is_valid_step(points: List[Tuple[int, int]], new_point: Tuple[int, int]) -> bool:
        # Check if the new point would create a self-intersection
        if new_point in points:
            return False
        # Check if the new edge would intersect any existing edge
        for i in range(len(points) - 1):
            if intersect(points[i], points[i+1], points[-1], new_point):
                return False
        return True

    def intersect(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int], p4: Tuple[int, int]) -> bool:
        # Check if two line segments intersect
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    num_points = random.randint(min_points, max_points)
    if num_points % 2 != 0:
        num_points += 1  # Ensure even number of points

    polygon = [(0, 0)]
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, up, left, down
    current_direction = 0

    while len(polygon) < num_points:
        dx, dy = directions[current_direction]
        step = random.randint(1, 5)
        new_point = (polygon[-1][0] + dx * step, polygon[-1][1] + dy * step)
        
        if is_valid_step(polygon, new_point):
            polygon.append(new_point)
            current_direction = (current_direction + 1) % 4
        else:
            # If the step is not valid, try changing direction without moving
            current_direction = (current_direction + 1) % 4

    # Ensure the polygon is closed
    while len(polygon) > 1 and not is_valid_step(polygon, polygon[0]):
        if polygon[-1][0] == polygon[0][0]:
            polygon.append((polygon[0][0], polygon[-1][1]))
        else:
            polygon.append((polygon[-1][0], polygon[0][1]))
    polygon.append(polygon[0])

    # Normalize coordinates to start from (1,1)
    min_x = min(p[0] for p in polygon)
    min_y = min(p[1] for p in polygon)
    normalized_polygon = [(p[0] - min_x + 1, p[1] - min_y + 1) for p in polygon]

    return normalized_polygon

def plot_polygon(polygon: List[Tuple[int, int]]):
    import matplotlib.pyplot as plt
    x, y = zip(*polygon)
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, 'b-')
    plt.fill(x, y, alpha=0.3)
    for i, (x, y) in enumerate(polygon):
        plt.annotate(f'P{i}', (x, y), xytext=(5, 5), textcoords='offset points')
    plt.title("Generated Rectilinear Polygon")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# Generate and plot a rectilinear polygon
polygon = generate_rectilinear_polygon()
print("Generated rectilinear polygon points:")
print(polygon)

plot_polygon(polygon)