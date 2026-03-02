from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def drawLines(x, y):
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glEnd()

def drawTriangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()
    
def drawField():
    # glColor3f(0.42, 0.56, 0.14)
    glColor3f(0.6, 0.4, 0.1)
    drawTriangle(0, 300, 0, 0, 500, 0)
    drawTriangle(0, 300, 500, 300, 500, 0)
    
def drawTrees():
    glColor3f(0.13, 0.55, 0.13)
    for x in range(0, 500, 40):
        # left-most -> x
        # right-most -> x+40
        # middle -> x+20
        drawTriangle(x, 240, x + 40, 240, x + 20, 290)

def drawHouse():
    drawField()
    drawTrees()
    # house body
    glColor3f(1.0, 0.98, 0.94)
    drawTriangle(187.5, 255, 187.5, 190, 312.5, 190)
    drawTriangle(312.5, 190, 312.5, 255, 187.5, 255)
    # roof
    glColor3f(0.6, 0.2, 0.8) 
    drawTriangle(170, 255, 330, 255, 250, 310)
    # door
    glColor3f(0.53, 0.81, 0.98)
    drawTriangle(235, 190, 265, 190, 265, 230)
    drawTriangle(235, 190, 235, 230, 265, 230)
    # Window -> left
    drawTriangle(200, 215, 225, 215, 225, 240)
    drawTriangle(200, 215, 200, 240, 225, 240)
    # Window -> right
    drawTriangle(275, 215, 300, 215, 300, 240)
    drawTriangle(275, 215, 275, 240, 300, 240)
    # door lock "."
    glColor3f(0, 0, 0)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(257, 213)
    glEnd()
    # window frames "+"
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(212.5, 215)
    glVertex2f(212.5, 240)
    glVertex2f(200, 227.5)
    glVertex2f(225, 227.5)
    glVertex2f(287.5, 215)
    glVertex2f(287.5, 240)
    glVertex2f(275, 227.5)
    glVertex2f(300, 227.5)
    glEnd()

def setupProjection():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, 0, 1)
    glMatrixMode(GL_MODELVIEW)
  
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupProjection()
    drawHouse()
    
    glutSwapBuffers()
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(450, 200)
    glutCreateWindow(b"A House in Rainfall")
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()