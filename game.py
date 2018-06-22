import keyboard

#from pyglet import window
#from pyglet.gl import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from time import sleep


class Ball:
    def __init__(self, x, z, RGB, size, height=100, quality=50):
        self.height = height
        self.falling = True

        self.velocity = -0.5
        self.g_force = 100
        self.x = x
        self.z = z
        self.RGB = RGB
        self.size = size
        self.quality = quality

        self.size /= 100

    def update(self):
        if self.g_force is 0:
            return

        self.height += self.velocity
        #print(self.height, " - ", self.velocity)

        if self.falling is False:
            self.velocity -= 0.01

        if self.height <= 0:
            self.velocity = self.g_force / 100
            self.g_force -= 5
            if self.g_force < 0:
                self.g_force = 0
            self.falling = False

    def draw(self):
        #glRotatef(0, 0, 0, 0)  # rotates the matrix so the planet actually has an orbit
        glTranslatef(self.x, self.height, self.z)  # translates the planet from the sun/planet by the distance it has from the sun/planet
        #glColor3f(self.RGB[0], self.RGB[1], self.RGB[2])  # gives the planet a color
        #gluSphere(q, self.size, self.quality, self.quality)  # creates the planet with the corrisponding size
        glutSolidSphere(5, 50, 50)


class Game:
    def __inits__(self):
        #glClearColor(0.0, 0.0, 0.0, 0.0)  # sets background color to black

        global q  # creates global variable q
        q = gluNewQuadric()  # creates a ref to which all objects must be bound
        #gluQuadricNormals(q, GLU_SMOOTH);
        glEnable(GL_DEPTH_TEST)  # enables depth comparison and updates the depth buffer
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # activates gl polygon mode
        glutInit()

        self.balls = (
            Ball(0, 0, [1, 0, 0], 50, 90),
            Ball(10, 0, [1, 1, 0], 50, 150),
            Ball(0, 10, [1, 1, 1], 50, 60),
            Ball(10, 10, [0, 1, 1], 50)
        )

    def __init__(self):

        global eyeX
        eyeX = 15.0
        global eyeY
        eyeY = -3.0
        global eyeZ
        eyeZ = -19.0

        global q  # creates global variable q
        q = gluNewQuadric()  # creates a ref to which all objects must be bound

        self.balls = (
            Ball(0, 0, [1, 0, 0], 50, 90),
            Ball(10, 0, [1, 1, 0], 50, 150),
            Ball(0, 10, [1, 1, 1], 50, 60),
            Ball(10, 10, [0, 1, 1], 50)
        )

        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutCreateWindow("Perspective view".encode("ascii"))
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)  # lichtbronnen moeten niet geprojecteerd worden, dus om onderscheid te kunnen maken moet de projectiematrix in een andere "matrix modus"
        glFrustum(-1.333, 1.333, -1, 1, 5, 20)
        glMatrixMode(GL_MODELVIEW)  # schakel terug naar de "model/view transformatiematrix modus"
        gluLookAt(3, 4, 5, 0, 0, 0, 0, 1, 0)
        glEnable(GL_LIGHTING)  # belichting
        glEnable(GL_RESCALE_NORMAL)  # zorgt voor correcte belichting van geschaalde objecten
        glEnable(GL_LIGHT0)  # een lichtbron
        glLight(GL_LIGHT0, GL_POSITION, [-3, 4, 5])  # positie lichtbron
        glLight(GL_LIGHT0, GL_DIFFUSE, [1, 0, 1])  # kleur lichtbron (paars)
        glLight(GL_LIGHT0, GL_AMBIENT, [1, 0, 1])  # kleur ambient licht (paars)
        # glEnable(GL_LIGHT1) # nog een lichtbron
        # glLight(GL_LIGHT1, GL_POSITION, [3, 4, 5]) # positie lichtbron
        # glLight(GL_LIGHT1, GL_DIFFUSE, [1, 1, 0]) # kleur lichtbron (geel)
        # glLight(GL_LIGHT1, GL_AMBIENT, [1, 1, 0]) # kleur ambient licht (geel)
        glutDisplayFunc(self.mydisplay)
        #glutKeyboardFunc(end)
        glutIdleFunc(glutPostRedisplay)
        glutMainLoop()

    def resize(self, width, height):                                    #makes sure you are able to see the planets
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)                                 #specifies projection as the current matrix
        glLoadIdentity()                                        #replaces current matrix with the identity matrix
        gluPerspective(zoom, 1 * width / height, 0.1, 100.0)    #the perspective from which you start watching
        glMatrixMode(GL_MODELVIEW)                                #specify modelviuw is the current matrix

    def mydisplay(self):
        print("Update")
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutSolidSphere(1, 50, 50)
        glLoadIdentity()
        gluLookAt(eyeX, eyeY, eyeZ,         # eye
                0.0, 1.0, 0.0,           # center
                0.0, 1, 0.0)            # up

        for b in self.balls:
            b.update()



        for b in self.balls:
            glPushMatrix()
            b.draw()
            glPopMatrix()

        glutSwapBuffers()

    def keyHandle(self, eyeX, eyeY, eyeZ):
        #print(eyeX, eyeY, eyeZ)
        if keyboard.is_pressed('a'):
            if eyeZ >= 0 and eyeX >= 0:
                eyeX += 0.1
                eyeZ -= 0.1
            elif eyeZ >= 0 and eyeX < 0:
                eyeX += 0.1
                eyeZ += 0.1
            elif eyeZ < 0 and eyeX >= 0:
                eyeZ -= 0.1
                eyeX -= 0.1
            elif eyeZ < 0 and eyeX < 0:
                    eyeZ += 0.1
                    eyeX -= 0.1
        if keyboard.is_pressed('d'):
            if eyeZ >= 0 and eyeX >= 0:
                eyeX -= 0.1
                eyeZ += 0.1
            elif eyeZ >= 0 and eyeX < 0:
                eyeX -= 0.1
                eyeZ -= 0.1
            elif eyeZ < 0 and eyeX >= 0:
                eyeZ += 0.1
                eyeX += 0.1
            elif eyeZ < 0 and eyeX < 0:
                eyeZ -= 0.1
                eyeX += 0.1
        if keyboard.is_pressed('w'):
            eyeY += 0.1
        if keyboard.is_pressed('s'):
            eyeY -= 0.1
        if keyboard.is_pressed('q'):
            if eyeZ < 0:
                eyeZ += 0.1
            else:
                eyeZ -= 0.1
            if eyeX < 0:
                eyeX += 0.1
            else:
                eyeX -= 0.1
            if eyeY < 0:
                eyeY += 0.1
            else:
                eyeY -= 0.1
            print (eyeX,eyeZ)
        if keyboard.is_pressed('e'):
            if eyeZ >= 0 and eyeX >= 0:
                eyeX += 0.1
                eyeZ += 0.1
            elif eyeZ >= 0 and eyeX < 0:
                eyeX -= 0.1
                eyeZ += 0.1
            elif eyeZ < 0 and eyeX >= 0:
                eyeZ -= 0.1
                eyeX += 0.1
            elif eyeZ < 0 and eyeX < 0:
                eyeZ -= 0.1
                eyeX -= 0.1
        return eyeX,eyeY,eyeZ

    def main(self):
        #win = window.Window()
        global zoom
        zoom = 135
        #win.on_resize = self.resize

        global eyeX
        eyeX = 15.0
        global eyeY
        eyeY = -3.0
        global eyeZ
        eyeZ = -19.0

        while not win.has_exit:
            eyeX, eyeY, eyeZ = self.keyHandle(eyeX, eyeY, eyeZ)
            win.on_resize = self.resize
            win.dispatch_events()
            self.mydisplay()
            win.flip()
            sleep(0.01)


if __name__ == "__main__":
    Game()
