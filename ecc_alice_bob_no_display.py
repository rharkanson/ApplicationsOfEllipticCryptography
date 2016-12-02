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
import random


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
    print("Elliptic Curve Cryptography Demo - Alice and Bob Mode")
    print("\tFirst, Alice and Bob agree upon a curve...")
    a = input("\t\ta = ")
    b = input("\t\tb = ")
    p = input("\t\tp = ")

    alice = Curve(a, b, p)
    bob = Curve(a, b, p)
    print("\n\tCurves created! Here is the equation: {}".format(alice.string()))

    print("\n\tNow, Alice and Bob agree upon a generator point...")
    x = int(input("\t\tx = "))
    y = int(input("\t\ty = "))

    if x < 0:
        x = random.randrange(0, int(p))

    if y < 0:
        y = random.randrange(0, int(p))


    print("\tAlice's curve: {}".format(alice.add_point(x, y)))
    print("\tBob's curve: {}".format(bob.add_point(x, y)))

    alice_private = int(input("\n\tNext, Alice chooses a random integer (her private key) to multiply the generator point by: "))
    alice.point_multiplication(0, alice_private)
    a_point = alice.points.pop()
    a_x, a_y = a_point.x, a_point.y
    alice.delete_points(0)
    alice.add_point(a_x, a_y)
    print("\t\tAlice's public key: ({}, {})".format(a_x, a_y))

    bob_private = int(input("\n\tAt the same time, Bob chooses his random integer: "))
    bob.point_multiplication(0, bob_private)
    b_point = bob.points.pop()
    b_x, b_y = b_point.x, b_point.y
    bob.delete_points(0)
    bob.add_point(b_x, b_y)
    print("\t\tBob's public key: ({}, {})".format(b_x, b_y))

    print("\n\tAlice sends Bob her public key ({}, {}).".format(a_x, a_y))
    input("\tBob sends Alice his public key ({}, {}).".format(b_x, b_y))
    input("\n\tEve scratches her head....")

    input("\n\tAlice take Bob's public key and adds the generator point n number of times, where n is her private key.")
    alice.delete_points(0)
    alice.add_point(b_x, b_y)
    for i in range(alice_private):
        alice.point_summation(0, len(alice.points) - 1)
    a_ss = alice.points.pop()
    a_ss_x, a_ss_y = a_ss.x, a_ss.y
    alice.delete_points(0)
    alice.add_point(a_x, a_y)
    alice.add_point(b_x, b_y)
    alice.add_point(a_ss_x, a_ss_y)
    input("\tAlice finds the shared secret to be: ({}, {})".format(a_ss_x, a_ss_y))

    input("\n\tBob take Alice's public key and adds the generator point m number of times, where m is his private key.")
    bob.delete_points(0)
    bob.add_point(a_x, a_y)
    for j in range(bob_private):
        bob.point_summation(0, len(bob.points) - 1)
    b_ss = bob.points.pop()
    b_ss_x, b_ss_y = b_ss.x, b_ss.y
    bob.delete_points(0)
    bob.add_point(b_x, b_y)
    bob.add_point(a_x, a_y)
    bob.add_point(b_ss_x, b_ss_y)
    input("\tBob finds the shared secret to be: ({}, {})".format(b_ss_x, b_ss_y))

main()
