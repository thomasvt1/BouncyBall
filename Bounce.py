from random import uniform
from random import random
from random import randint

from OpenGL.GLU import *
from OpenGL.GLUT import *

from Models import *


class Game:
    def __init__(self):
        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)
        glutInitWindowSize(720, 480)
        glutCreateWindow("Bouncy Ball".encode("ascii"))
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_DEPTH_TEST)

        self.balls = []

        ballarray = (
            Teapot(0, 0, 80, 2),
            Ball(2, 0, 50, 5),
            Ball(1, 3, 50, 8),
            Cube(-3, -1, 70, 1)
        )

        for b in ballarray:
            self.balls.append(b)


        self.pressed = []
        self.zoom = 5

        glMatrixMode(GL_PROJECTION)
        glFrustum(-2.333, 2.333, -2, 2, self.zoom, 25)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(10, 3, 10,
                  0, 0, 0,
                  0, 1, 0)

        glEnable(GL_LIGHTING)  # belichting
        glEnable(GL_RESCALE_NORMAL)  # zorgt voor correcte belichting van geschaalde objecten

        glEnable(GL_LIGHT0)  # een lichtbron
        glLight(GL_LIGHT0, GL_POSITION, [0, 3, -2])  # positie lichtbron
        glLight(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1])  # kleur lichtbron (paars)
        glLight(GL_LIGHT0, GL_AMBIENT, [1, 1, 1])  # kleur ambient licht (paars)

        glEnable(GL_LIGHT1) # nog een lichtbron
        glLight(GL_LIGHT1, GL_POSITION, [0, 3, 3]) # positie lichtbron
        glLight(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1]) # kleur lichtbron (geel)
        glLight(GL_LIGHT1, GL_AMBIENT, [1, 1, 1]) # kleur ambient licht (geel)

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.end)
        glutIdleFunc(glutPostRedisplay)
        glutMainLoop()

    def end(self, key, x, y):
        global eyeX, eyeY, eyeZ

        key = key.decode("utf-8")
        print(key)

        if "o" is key:
            glDisable(GL_LIGHT0)
        elif "p" is key:
            glEnable(GL_LIGHT0)

        elif "k" is key:
            glDisable(GL_LIGHT1)
        elif "l" is key:
            glEnable(GL_LIGHT1)

        elif "r"is key:
            self.balls = (
                Teapot(0, 0, 80, 2),
                Ball(2, 0, 1, 5),
                Ball(1, 3, 25, 8),
                Cube(-3, -1, 80, 1)
            )

        elif "x"is key:
            self.balls = []
            for i in range(0,5):
                self.balls.append(Ball(uniform(-3, 3), uniform(-3, 3), uniform(60, 80), uniform(3, 10)))

        elif "z"is key:
            for i in range(0, 5):
                self.balls.append(Ball(uniform(-3, 3), uniform(-3, 3), uniform(60, 80), uniform(3, 10)))

        elif "c"is key:
            self.balls = []
            for i in range(0, 5):
                self.balls.append(Ball(uniform(-3, 3), uniform(-3, 3), uniform(60, 80), uniform(3, 10), randint(3, 15)))

        elif "i" is key or "j" is key:
            array = [random(), random(), random()]
            light = GL_LIGHT0 # Default to Light0 - 'I' press
            if "j" is key:
                light = GL_LIGHT1
            glLight(light, GL_DIFFUSE, array)
            glLight(light, GL_AMBIENT, array)

        elif "u" is key or "h" is key:
            light = GL_LIGHT0  # Default to Light0 - 'U' press
            if "h" is key:
                light = GL_LIGHT1
            glLight(light, GL_DIFFUSE, [1, 1, 1])
            glLight(light, GL_AMBIENT, [1, 1, 1])

        elif "t" is key:
            self.zoom = 5
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glFrustum(-2.333, 2.333, -1, 3, self.zoom, 25)
            glMatrixMode(GL_MODELVIEW)

        elif "w" is key or "s" is key:
            if "w" is key:
                self.zoom += 0.1
            else:
                self.zoom -= 0.1

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glFrustum(-2.333, 2.333, -2, 2, self.zoom, 25)
            glMatrixMode(GL_MODELVIEW)

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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(0, -3, 0)
        #glColor3f(1, 0, 0)  # gives the planet a color
        glutSolidSphere(5, 2, 25)
        glPopMatrix()



        for b in self.balls:
            b.update()

        for b in self.balls:
            b.draw()

        glFlush()
        glutSwapBuffers()


Game()
