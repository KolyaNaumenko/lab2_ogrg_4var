import numpy as np
import matplotlib.pyplot as plt

# Клас для вузла KD-дерева
class KDTreeNode:
    def __init__(self, point, axis, left=None, right=None):
        self.point = point
        self.axis = axis
        self.left = left
        self.right = right

# Функція для побудови KD-дерева
def build_kd_tree(points, depth=0):
    if len(points) == 0:
        return None

    k = len(points[0])  # Вимірність простору
    axis = depth % k

    points.sort(key=lambda x: x[axis])
    median = len(points) // 2

    return KDTreeNode(
        point=points[median],
        axis=axis,
        left=build_kd_tree(points[:median], depth + 1),
        right=build_kd_tree(points[median + 1:], depth + 1)
    )

# Функція для друку KD-дерева
def print_kd_tree(node, depth=0):
    if node is None:
        return

    print(' ' * depth * 2, f"Level {depth} | Point: {node.point} | Axis: {node.axis}")
    print_kd_tree(node.left, depth + 1)
    print_kd_tree(node.right, depth + 1)

# Точки
points = [
    (2, 0),  # A
    (0, 4),  # B
    (10, 0), # C
    (7, 2),  # D
    (11, 4), # E
    (9, 5),  # F
    (6, 9),  # G
    (3, 8),  # H
    (8, 8),  # I
    (5, 5)   # J
]

# Створюємо KD-дерево
kd_tree = build_kd_tree(points)

# Виводимо структуру дерева в консоль
print("KD-Tree structure:")
print_kd_tree(kd_tree)

# Функція для виконання регіонального пошуку
def range_search(node, region_min, region_max, depth=0, results=None):
    if node is None:
        return results

    if results is None:
        results = []

    axis = depth % len(region_min)

    # Перевірка, чи точка в регіоні
    if all(region_min[i] <= node.point[i] <= region_max[i] for i in range(len(region_min))):
        results.append(node.point)

    # Рекурсивний пошук у піддеревах
    if region_min[axis] <= node.point[axis]:
        range_search(node.left, region_min, region_max, depth + 1, results)
    if node.point[axis] <= region_max[axis]:
        range_search(node.right, region_min, region_max, depth + 1, results)

    return results

# Визначаємо регіон пошуку
region_min = np.array([0,0])
region_max = np.array([9, 10])

# Виконуємо пошук точок у заданому регіоні
region_points = range_search(kd_tree, region_min, region_max)

# Візуалізація точок та регіону пошуку
plt.figure(figsize=(10, 10))

# Всі точки
points_array = np.array(points)
plt.scatter(points_array[:,0], points_array[:,1], color='blue', label='Всі точки')

# Точки у регіоні
if region_points:
    region_points_array = np.array(region_points)
    plt.scatter(region_points_array[:,0], region_points_array[:,1], color='red', label='Точки у регіоні')

# Візуалізація регіону пошуку
rect = plt.Rectangle(region_min, region_max[0] - region_min[0], region_max[1] - region_min[1],
                     linewidth=1, edgecolor='green', facecolor='none', label='Регіон пошуку')
plt.gca().add_patch(rect)

# Підписуємо точки
for i, txt in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']):
    plt.annotate(txt, (points_array[i,0], points_array[i,1]), textcoords="offset points", xytext=(0,5), ha='center')

plt.title('Регіональний пошук точок методом дерева регіонів')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()

print("Точки у регіоні:", region_points)