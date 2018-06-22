from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Object:
    def __init__(self, x, z, RGB, size, height=3.0, quality=50):
        self.height = height
        self.falling = True

        self.velocity = -0.0005
        self.g_force = 1
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
        glutSolidSphere(0.5, 25, 25)
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


class Game:
    def __init__(self):
        self.balls = (
            Ball(0, 0, [1, 0, 0], 5, 2),
            Ball(2, 0, [1, 1, 0], 1, 5),
            Ball(1, 3, [1, 1, 1], 25, 0),
            Cube(-3, -1, [0, 1, 1], 50, 3)
        )

        self.pressed = []

        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutCreateWindow("Bouncy Ball".encode("ascii"))
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glFrustum(-1.333, 1.333, -1, 1, 5, 20)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(10, 4, 10,
                  0, 0, 0,
                  0, 1, 0)

        glEnable(GL_LIGHTING)  # belichting
        glEnable(GL_RESCALE_NORMAL)  # zorgt voor correcte belichting van geschaalde objecten

        glEnable(GL_LIGHT0)  # een lichtbron
        glLight(GL_LIGHT0, GL_POSITION, [-3, 3, 3])  # positie lichtbron
        glLight(GL_LIGHT0, GL_DIFFUSE, [1, 0, 1])  # kleur lichtbron (paars)
        glLight(GL_LIGHT0, GL_AMBIENT, [1, 0, 1])  # kleur ambient licht (paars)

        glEnable(GL_LIGHT1) # nog een lichtbron
        glLight(GL_LIGHT1, GL_POSITION, [3, 3, 3]) # positie lichtbron
        glLight(GL_LIGHT1, GL_DIFFUSE, [1, 1, 0]) # kleur lichtbron (geel)
        glLight(GL_LIGHT1, GL_AMBIENT, [1, 1, 0]) # kleur ambient licht (geel)
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.end)
        glutIdleFunc(glutPostRedisplay)
        glutMainLoop()

    def end(self, key, x, y):
        global eyeX, eyeY, eyeZ

        key = key.decode("utf-8")
        print(key)

        if key in self.pressed:
            self.pressed.remove(key)
        else:
            self.pressed.append(key)

    def handle_rotate(self):
        speed = 0.005
        if len(self.pressed) is 0:
            return

        if "a" in self.pressed:
            glRotatef(speed, 0, 1.0, 0)

        if "d" in self.pressed:
            glRotatef(-speed, 0, 1.0, 0)
        glutPostRedisplay()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.handle_rotate()

        for b in self.balls:
            b.update()

        for b in self.balls:
            b.draw()
        glutSwapBuffers()


Game()
