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


import matplotlib.pyplot as plt


class Curve(object):

    def __init__(self, a, b, p):
        self.a = int(a)
        self.b = int(b)
        self.p = int(p)
        self.points = []

    def string(self):
        return "y^2 = x^3 + ({})x + ({}) % {}".format(self.a, self.b, self.p)

    def display(self):
        plt.xlim([0, self.p])
        plt.ylim([0, self.p])
        plt.grid()
        #lbl = plt.figure().add_subplot(111)

        xs = []
        ys = []
        for i, p in enumerate(self.points):
            xs.append(p.x)
            ys.append(p.y)
            plt.annotate(" {}: {}, {}".format(i, p.x, p.y), xy=(p.x, p.y), textcoords='data')

        plt.plot(xs, ys, 'or')
        plt.show()


    def add_point(self, x, y):
        try:
            x = int(x) % self.p
            y = int(y) % self.p

            point = Point(x, y)
            self.points.append(point)

            return "Point ({}, {}) added to curve.".format(x, y)

        except:
            return "Point not added!"

    def delete_points(self, index=-1):
        if index != -1:
            point = self.points[index]

        self.points.clear()

        if index != -1:
            self.points.append(point)
            return "All points except ({}, {}) removed from curve.".format(point.x, point.y)

        return "All points removed from curve!"

    def point_duplication(self, index=-1):
        if len(self.points) == 0:
            return "No points to perform operation!"

        p0 = self.points[index] if index > -1 else self.points[len(self.points) - 1]
        x0, y0 = p0.x, p0.y

        s = ((3 * x0**2 + self.a) * multi_inv(2 * y0, self.p)) % self.p

        x_new = (s**2 - 2 * x0) % self.p
        y_new = (s * (x0 - x_new) - y0) % self.p

        return self.add_point(x_new, y_new)

    def point_summation(self, index_1=-1, index_2=-1):
        if len(self.points) == 0:
            return "No points to perform operation!"

        p0 = self.points[index_1] if index_1 > -1 else self.points[0]
        p1 = self.points[index_2] if index_2 > -1 else self.points[len(self.points) - 1]
        x0, y0 = p0.x, p0.y
        x1, y1 = p1.x, p1.y


        if x0 == x1 and y0 == y1:
            return self.point_duplication(0)

        s = ((y0 - y1) * multi_inv(x0 - x1, self.p)) % self.p

        x_new = (s**2 - (x0 + x1)) % self.p
        y_new = (s * (x0 - x_new) - y0) % self.p

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


def extended_euclidean(a, b):
    s, _s = 0, 1
    t, _t = 1, 0
    r, _r = b, a

    while r != 0:
        q = _r // r
        _r, r = r, _r - q * r
        _s, s = s, _s - q * s
        _t, t = t, _t - q * t

    return _r, _s, _t


def multi_inv(n, p):
    gcd, x, y = extended_euclidean(n, p)
    #assert (n * x + p * y) % p == gcd

    if gcd == 1:
        return x % p

    return -1


def main():
    print("Elliptic Curve Cryptography Demo")
    print("\tLet's make a curve...")
    a = input("\t\ta = ")
    b = input("\t\tb = ")

    print("\n\tNow let's give the curve a modulus...")
    p = input("\t\tp = ")

    curve = Curve(a, b, p)
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
