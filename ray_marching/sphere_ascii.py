import numpy as np
import os

# Config

WIGHT = 120
HEIGHT = 30
aspect = HEIGHT / WIGHT
colors = " .-~=+oxO0X%@"


class RayMarching:
    def __init__(self):
        self.radius = 0.3

        self.screen = [[colors[0] for m in range(WIGHT)] for n in range(HEIGHT)]
        self.x_line = np.linspace(-1, 1, WIGHT)
        self.y_line = np.linspace(1, -1, HEIGHT)

        self.sphere = np.array([0, 0, 0])
        self.light = np.array([-1, 1, 0])

    def show_screen(self):
        """ Визуализирует рабочую поверхность """

        os.system("clear")

        for row in self.screen:
            print("".join(row))

    def lenght(self, p1, p2=(0, 0, 0)):
        """ Возвращает расстояние между двумя точками """

        return np.sqrt(
            (p1[0] - p2[0]) ** 2 + 
            (p1[1] - p2[1]) ** 2 * aspect + 
            (p1[2] - p2[2]) ** 2
        )

    def vec_cosines(self, point_1, point_2):
        """ Возвращает косинус между двумя векторами """

        return (
            (point_2[0] * point_1[0] + point_2[1] * point_1[1] + point_2[2] * point_1[2]) / 
            (self.lenght(point_2) * self.lenght(point_1)) ** 2 * 0.02 + 0.2
        )

    def rotate_point(self, point, axis, angle):
        rotation_X = np.array([[1, 0, 0],
                               [0, np.cos(angle), -np.sin(angle)],
                               [0, np.sin(angle), np.cos(angle)]])

        rotation_Y = np.array([[np.cos(angle), 0, np.sin(angle)],
                               [0, 1, 0],
                               [-np.sin(angle), 0, np.cos(angle)]])

        rotation_Z = np.array([[np.cos(angle), -np.sin(angle), 0],
                               [np.sin(angle), np.cos(angle), 0],
                               [0, 0, 1]])
        
        rotation_XY = np.dot(rotation_X, rotation_Y)
        rotation_YZ = np.dot(rotation_Y, rotation_Z)
        rotation_XZ = np.dot(rotation_X, rotation_Z)
        rotation_XYZ = np.dot(rotation_XY, rotation_YZ)
        
        if axis == "X":
            return np.dot(point, rotation_X)
        elif axis == "Y":
            return np.dot(point, rotation_Y)
        elif axis == "Z":
            return np.dot(point, rotation_Z)
        elif axis in ["XY", "YX"]:
            return np.dot(point, rotation_XY)
        elif axis in ["XZ", "ZX"]:
            return np.dot(point, rotation_XZ)
        elif axis in ["YZ", "ZY"]:
            return np.dot(point, rotation_YZ)
        elif axis == "XYZ":
            return np.dot(point, rotation_XYZ)
        else:
            return point
        
        pass

    def SDF_sphere(self, p):
        """ Знаковая функция сферы """

        return self.lenght([p[0], p[1], p[2]], self.sphere)  - self.radius
    
    def get_sphere(self, axis, angle):
        """ Вычисления поверхности сферы """

        for x_, x in enumerate(self.x_line):
            for y_, y in enumerate(self.y_line):
                z = 0
                for step in range(10):
                    point = [x, y, z]
                    distance = self.SDF_sphere(point)
                    z += distance

                    if distance < 0.01:
                        light = self.rotate_point(self.light, axis, angle)

                        cos = self.vec_cosines([x, y, z], light)
                        if cos < 0:
                            cos = 0

                        color = ((len(colors) - 1) * cos) 
                        if color > (len(colors) - 1):
                            color = (len(colors) - 1)

                        self.screen[y_][x_] = colors[int(color)]
                        break

        self.show_screen()


rm = RayMarching()
angle = 0
axis = "Y"

while angle < 10:
    rm.get_sphere(axis, angle)
    angle += 0.3

# rm.get_sphere(axis, 1)