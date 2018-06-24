from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image

import math


class Object:
    def __init__(self, x, z, RGB, size, height=3.0, quality=50):
        self.height = height
        self.falling = True

        self.velocity = -0.0005
        self.g_force = 1 + self.height / 8
        self.x = x
        self.z = z
        self.RGB = RGB
        self.size = size
        self.quality = quality

        self.size /= 100

    def update(self):
        if self.g_force <= 0 and self.velocity <= 0 and self.height <= -2:
            return

        self.height += self.velocity
        #print(self.height, " - ", self.velocity, self.g_force)

        self.velocity -= 0.0000001

        if self.height <= -2 and self.velocity < 0:
            self.velocity = 0.001 * self.g_force
            self.g_force -= 0.1
            self.falling = False

    def draw_start(self):
        glPushMatrix()
        glTranslatef(self.x, self.height,
                     self.z)  # translates the planet from the sun/planet by the distance it has from the sun/planet
        glColor3f(self.RGB[0], self.RGB[1], self.RGB[2])  # gives the planet a color

    def draw_end(self):
        glPopMatrix()


class Ball(Object):
    def __init__(self, x, z, RGB, size, height=3.0, quality=50):
        super().__init__(x, z, RGB, size, height, quality)

    def update(self):
        super().update()

    def draw(self):
        super().draw_start()
        glColor3f(1, 1, 1)  # gives the planet a color
        glutSolidSphere(0.5, 25, 25)
        #glutSolidTeapot(0.5)

        super().draw_end()


class Cube(Object):
    def __init__(self, x, z, RGB, size, height=3.0, quality=50):
        super().__init__(x, z, RGB, size, height, quality)

    def update(self):
        super().update()

    def draw(self):
        super().draw_start()
        glutSolidCube(self.size)
        super().draw_end()


class Teapot(Object):
    def __init__(self, x, z, RGB, size, height=3.0, quality=50, texture=True):
        super().__init__(x, z, RGB, size, height, quality)
        if texture:
            img = Image.open("hart.png")  # laad plaatje
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)  # voor plaatjes met oneven aantal pixels
            texture = glGenTextures(1)  # maak een ID voor 1 textuur
            glBindTexture(GL_TEXTURE_2D, texture)  # gebruik de ID
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes())

    def update(self):
        super().update()

    def draw(self):
        super().draw_start()
        glEnable(GL_TEXTURE_2D)
        glutSolidTeapot(self.size)
        glDisable(GL_TEXTURE_2D)
        super().draw_end()

class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point(x, self.y, z)

    def transform(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point(x, y, 1)


class WireCube:
    def __init__(self):
        self.points = [
            Point(-1, -1, -1),
            Point(1, -1, -1),
            Point(1, 1, -1),
            Point(-1, 1, -1),
            Point(-1, -1, 1),
            Point(1, -1, 1),
            Point(1, 1, 1),
            Point(-1, 1, 1)
        ]

        self.faces = [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6), (4, 0, 3, 7), (0, 4, 5, 1), (3, 2, 6, 7)]

        # Will hold transformed vertices.
        t = []