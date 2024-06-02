import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

# Точки
points = np.array([
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
])

# Створюємо KD-дерево
tree = cKDTree(points)

# Визначаємо регіон пошуку
region_min = np.array([2, 6])
region_max = np.array([12, 11])

# Виконуємо пошук точок у заданому регіоні
results = tree.query_ball_point((region_min + region_max) / 2, np.linalg.norm(region_max - region_min) / 2)

# Фільтруємо точки, що дійсно потрапляють у регіон
region_points = [points[i] for i in results if all(region_min <= points[i]) and all(points[i] <= region_max)]

# Візуалізація точок та регіону пошуку
plt.figure(figsize=(10, 10))

# Всі точки
plt.scatter(points[:,0], points[:,1], color='blue', label='Всі точки')

# Точки у регіоні
if region_points:
    region_points = np.array(region_points)
    plt.scatter(region_points[:,0], region_points[:,1], color='red', label='Точки у регіоні')

# Візуалізація регіону пошуку
rect = plt.Rectangle(region_min, region_max[0] - region_min[0], region_max[1] - region_min[1],
                     linewidth=1, edgecolor='green', facecolor='none', label='Регіон пошуку')
plt.gca().add_patch(rect)

# Підписуємо точки
for i, txt in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']):
    plt.annotate(txt, (points[i,0], points[i,1]), textcoords="offset points", xytext=(0,5), ha='center')

plt.title('Регіональний пошук точок методом дерева регіонів')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()

print("Точки у регіоні:", region_points)