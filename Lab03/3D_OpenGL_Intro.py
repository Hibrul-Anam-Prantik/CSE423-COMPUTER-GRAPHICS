from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

# camera-related variables
camera_pos = (0, 600, 500)

fovY = 120 # field of view in the y direction
GRID_LENGTH = 600 # length of the grid lines
rand_var = 423

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1) # white color
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # set up an orthographic projection that matches the window coordinates
    gluOrtho2D(0, 1000, 0, 800) # left, right, bottom, top
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # draw text at (x, y) in window coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
        
    # restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_shapes():
    glPushMatrix() # save the current matrix state
    glColor3f(1, 0, 0) # red color
    glTranslatef(0, 0 , 0) # move to the center of the scene
    glutSolidCube(60) # take cube size as the parameter
    glTranslatef(0, 0, 100) # move up in the z direction
    glColor3f(0, 1, 0) # green color
    glutSolidCube(60)
    
    glColor3f(1, 1, 0) # yellow color
    glScalef(2, 2, 2) # scale the cube to make it bigger
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10) # parameters are: quadric, base radius, top radius, height, slices, stacks
 
def setupCamera():
    """
     configures the camera's projection and view settings.
     uses a perspective projection and the gluLookAt function to position the camera and set its orientation to look at the target.
    """   
    glMatrixMode(GL_PROJECTION) # switch to projection matrix mode
    glLoadIdentity() # reset the projection matrix
    # set up a perspective projection with the specified field of view, aspect ratio, and near/far clipping planes
    gluPerspective(fovY, 1.25, 0.1, 1500) # fovY, aspect ratio, near plane, far plane
    glMatrixMode(GL_MODELVIEW) # switch back to modelview matrix mode
    glLoadIdentity() # reset the modelview matrix
    
    # extract camera position and look-at target from the camera_pos variable
    x, y, z = camera_pos
    # set the camera position and orientation using gluLookAt, where the camera is positioned at (x, y, z), looking at the origin (0, 0, 0), and with an up vector of (0, 1, 0)
    gluLookAt(x, y, z,     # camera position
               0, 0, 0,     # look at the target (the origin
               0, 1, 0)     # up vector (z-axis is up)

def idle():
    """
        idle func that runs when the application is idle. It updates the random variable and requests a redraw of the screen to create an animation effect.
        - triggers a redraw of the screen by calling glutPostRedisplay(), which will call the display function to update the screen with any changes.
    """
    # global camera_pos
    # x, y, z = camera_pos
    # y += 0.5
    # camera_pos = (x, y, z)
    # glutPostRedisplay() # request a redraw of the screen
    
def showScreen():
    """
    Display function to render the game screen:
    - Clear the screen and sets up the camera.
    - Draw everything of the screen (grid, shapes, text)."""
    # clear the screen (color) and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() # reset the modelview matrix
    glViewport(0, 0, 1000, 800) # set the viewport to cover the whole window
    
    setupCamera() # config camera position and perspective
    
    # drawe a random point
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # draw the grid - game background
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1) # white color
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)

    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex(-GRID_LENGTH, 0, 0)
    glVertex(0, 0, 0)
    glVertex(0, -GRID_LENGTH, 0)
    
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()
    
    # display game info text at a specific screen position
    draw_text(10, 680, f"A Random Fixed Position Text")
    draw_text(10, 640, f"See how the posotion and variable change?: {rand_var}")
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) # enable double buffering, RGB color mode, and depth testing
    glutInitWindowSize(1000, 800) # set the window size
    glutInitWindowPosition(0, 0); # set the window position
    wind = glutCreateWindow(b"3D Shapes with OpenGL") # create the window with a title

    glutDisplayFunc(showScreen) # register the display callback function
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)  
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle) # register the idle func to move the bullet automatically
    
    glutMainLoop() # start the main loop

if __name__ == "__main__":
    main()