"""
    Applications of Elliptic Curve Cryptography
    Russell Harkanson
    Copyright 2016

    Supplemental software for publication.
"""


__title__       = "Applications of Elliptic Curve Cryptography"
__author__      = "Russell Harkanson"
__copyright__   = "Copyright 2016"
__license__     = "MIT"
__version__     = "1.0.0"
__email__       = "harkanso@unlv.nevada.edu"


import numpy as np
import matplotlib.pyplot as plt
import math


class Curve(object):

    def __init__(self, a, b):
        self.a = float(a)
        self.b = float(b)
        self.points = []
        self.res = 50

    def string(self):
        return "y^2 = x^3 + ({})x + ({})".format(self.a, self.b)

    def display(self):
        y, x = np.ogrid[-self.res:self.res:3000j, -self.res:self.res:3000j]
        con = plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * self.a - self.b, [0])
        plt.grid()
        #lbl = plt.figure().add_subplot(111)

        xs = []
        ys = []
        for i, p in enumerate(self.points):
            xs.append(p.x)
            ys.append(p.y)
            x_str = "{0:.3f}".format(p.x)
            y_str = "{0:.3f}".format(p.y)
            plt.annotate(" {}: {}, {}".format(i, x_str, y_str), xy=(p.x, p.y), textcoords='data')
            #lbl.annotate("{}: {}, {}".format(i, p.x, p.y), xy=(p.x, p.y + 1), textcoords='data')


        plt.plot(xs, ys, 'or')
        plt.show()

    def add_point(self, x, y):
        if y == "+" or y == "-":
            try:
                x = float(x)
                y_in = math.sqrt(x**3 + (self.a * x) + self.b).real if y == "+" \
                    else -math.sqrt(x**3 + (self.a * x) + self.b).real

                point = Point(x, y_in)
                self.points.append(point)
                self.res = max(self.res, x, y_in)
                return "Point ({}, {}) added to curve." .format(x, y_in)

            except:
                return "Point not on curve!"

        else:
            try:
                x = float(x)
                y = float(y)
                lhs = float("{0:.2f}".format(y**2))
                rhs = float("{0:.2f}".format(x**3 + (self.a * x) + self.b))

                if lhs == rhs:
                    y_in = math.sqrt(x**3 + (self.a * x) + self.b).real if y > 0 \
                        else -math.sqrt(x**3 + (self.a * x) + self.b).real
                    point = Point(x, y_in)
                    self.points.append(point)

                    self.res = max(self.res, x, y_in)
                    return "Point ({}, {}) added to curve.".format(x, y_in)

                else:
                    return "Point not on curve!"

            except:
                return "Point not on curve!"

    def delete_points(self, index=-1):
        if index != -1:
            point = self.points[index]

        self.points.clear()

        if index != -1:
            self.points.append(point)
            self.res = max(50, point.x, point.y)
            return "All points except ({}, {}) removed from curve.".format(point.x, point.y)

        return "All points removed from curve!"

    def point_duplication(self, index=-1):
        if len(self.points) == 0:
            return "No points to perform operation!"

        p = self.points[index] if index > -1 else self.points[len(self.points) - 1]

        s = (3 * p.x**2 + self.a) / (2 * p.y)

        x_new = s**2 - 2 * p.x
        y_new = s * (p.x - x_new) - p.y

        return self.add_point(x_new, y_new)

    def point_summation(self, index_1=-1, index_2=-1):
        if len(self.points) == 0:
            return "No points to perform operation!"

        p1 = self.points[index_1] if index_1 > -1 else self.points[0]
        p2 = self.points[index_2] if index_2 > -1 else self.points[len(self.points) - 1]

        if p1.x == p2.x and p1.y == p2.y:
            return self.point_duplication(0)

        s = (p1.y - p2.y) / (p1.x - p2.x)

        x_new = s**2 - (p1.x + p2.x)
        y_new = s * (p1.x - x_new) - p1.y

        return self.add_point(x_new, y_new)

    def point_multiplication(self, index, n):
        if len(self.points) == 0:
            return "No points to perform operation!"

        if index < 0:
            index = 0

        if index > len(self.points) - 1:
            index = len(self.points) - 1

        if n < 1:
            return "Point not added!"

        for i in range(n):
            if i == n-1:
                ret = self.point_summation(index, index+i)
            else:
                self.point_summation(index, index+i)

        return ret


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    print("Elliptic Curve Cryptography Demo")
    print("\tLet's make a curve...")
    a = input("\t\ta = ")
    b = input("\t\tb = ")

    curve = Curve(a, b)
    print("\n\tCurve created! Here is the equation: {}".format(curve.string()))

    opt = -1
    while opt != 0:
        print("\n\tWhat shall we do next?")
        print("\t  1: List points on curve")
        print("\t  2: Add point to curve")
        print("\t  3: Point Duplication")
        print("\t  4: Point Summation")
        print("\t  5: Point Multiplication")
        print("\t  6: Show curve")
        print("\t  7: Delete points")

        print("\t  0: Quit")
        opt = int(input("\tChoice: "))

        if opt == 1:
            print("\n\t\tPoints on curve:")
            for i,p in enumerate(curve.points):
                print("\t\t\t[{}]\t({}, {})".format(i, p.x, p.y))

        if opt == 2:
            x_in = input("\t\tx = ")
            y_in = input("\t\ty = ")
            print("\n\t\t{}".format(curve.add_point(x_in, y_in)))

        if opt == 3:
            p_index = input("\n\t\tDuplicate point: ")
            try:
                idx = int(p_index)
            except:
                idx = -1
            print("\t\t{}".format(curve.point_duplication(idx)))

        if opt == 4:
            p_index_1 = input("\n\t\tAdd point 1: ")
            p_index_2 = input("\t\t to point 2: ")
            try:
                idx_1 = int(p_index_1)
            except:
                idx_1 = -1
            try:
                idx_2 = int(p_index_2)
            except:
                idx_2 = -1
            print("\t\t{}".format(curve.point_summation(idx_1, idx_2)))

        if opt == 5:
            p_index = input("\n\t\tPoint: ")
            n = input("\t\t\tn: ")
            try:
                idx = int(p_index)
            except:
                idx = -1
            try:
                n = int(n)
            except:
                n = -1
            print("\t\t{}".format(curve.point_multiplication(idx, n)))

        if opt == 6:
            curve.display()

        if opt == 7:
            p_index = input("\n\t\tDelete all points (except): ")
            try:
                idx = int(p_index)
            except:
                idx = -1
            print("\t\t{}".format(curve.delete_points(idx)))


main()

