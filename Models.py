from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image


class Object:
    def __init__(self, x, z, size, height=3.0):
        self.height = height
        self.falling = True

        self.velocity = -0.0005
        self.g_force = 1 + self.height / 8
        self.x = x
        self.z = z
        self.size = size

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
        glTranslatef(self.x, self.height, self.z)

    def draw_end(self):
        glPopMatrix()


class Ball(Object):
    def __init__(self, x, z, size, height=3.0, quality=25):
        super().__init__(x, z, size, height)
        self.quality = quality

    def update(self):
        super().update()

    def draw(self):
        super().draw_start()
        #glEnable(GL_TEXTURE_2D)
        glutSolidSphere(self.size, self.quality, 25)
        #glDisable(GL_TEXTURE_2D)
        super().draw_end()


class Cube(Object):
    def __init__(self, x, z, size, height=3.0):
        super().__init__(x, z, size, height)

    def update(self):
        super().update()

    def draw(self):
        super().draw_start()
        glutSolidCube(self.size)
        super().draw_end()


class Teapot(Object):
    def __init__(self, x, z, size, height=3.0, texture=True):
        super().__init__(x, z, size, height)
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
