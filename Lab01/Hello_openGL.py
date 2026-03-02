# ===== OpenGL 2D Point Drawing Example =====
# This program displays a single yellow point using PyOpenGL + GLUT.

from OpenGL.GL import *     # Core OpenGL functions (drawing, colors, etc.)
from OpenGL.GLUT import *   # GLUT library (window creation, display, loop)
from OpenGL.GLU import *    # OpenGL Utility Library (projection utilities)

# --- Global coordinates of the point ---
x, y = 250, 250


# ===== Function to draw a single point =====
def draw_points(x, y):
    glPointSize(30)          # Set pixel size of the point (default = 1)
    glBegin(GL_POINTS)      # Start drawing points
    glVertex2f(x, y)  
    glColor3f(0, 1, 1)# Specify the (x, y) coordinate of the point
    glVertex2f(200, 200)
    glEnd()                 # Finish drawing


def draw_lines():
    glBegin(GL_LINES)       # Start drawing lines
    glVertex2f(100, 100)    # First endpoint of the line
    glVertex2f(200, 200)    # Second endpoint of the line
    glColor3f(0, 0, .8)     # Set line color to red
    glVertex2f(255, 255)
    glVertex2f(355, 355)
    glEnd()                 # Finish drawing


# ===== Set up 2D coordinate system =====
def setup_projection():
    # glViewport(x, y, width, height)
    glViewport(0, 0, 500, 500)     # Define the portion of the window to render to (0, 0) is the bottom-left corner, and (500, 500) is the top-right corner; This is the size of the drawing area in pixels.
    glMatrixMode(GL_PROJECTION)    # Switch to the projection matrix
    glLoadIdentity()               # Reset the projection matrix
    # glOrtho(left, right, bottom, top, near, far)
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)  # Define a 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)     # Switch back to the modelview matrix


# ===== Display callback =====
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer
    glLoadIdentity()                                    # Reset transformations
    setup_projection()                                  # Set up coordinate system
    glColor3f(0.0, 0.0, 0.8)                            # Set color (R, G, B) → Blue
    draw_points(x, y)                                   # Global point coordinates, (250, 250)
    glColor3f(0.8, 0.0, 0.0)                            # Set color to red for the second point 
    draw_points(100, 150)  
    # Draw the points
    draw_lines()
    glutSwapBuffers()                                   # Swap buffers (double buffering)


# ===== Main entry point =====
def main():
    glutInit()                               # Initialize GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)           # Set display mode: RGBA color
    glutInitWindowSize(500, 500)             # Set window size (width, height)
    glutInitWindowPosition(0, 0)             # Set window position (top-left corner)
    glutCreateWindow(b"OpenGL 2D Point")     # Create window with a title
    glutDisplayFunc(display)                 # Register display callback
    glutMainLoop()                           # Start the main event-processing loop


# ===== Run the program =====
if __name__ == "__main__":
    main()
