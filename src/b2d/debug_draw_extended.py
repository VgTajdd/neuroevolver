from Box2D import b2DrawExtended
import pygame
import settings

class DebugDrawExtended(b2DrawExtended):
    """
    This debug draw class accepts callbacks from Box2D (which specifies what to
    draw) and handles all of the rendering.

    If you are writing your own game, you likely will not want to use debug
    drawing.  Debug drawing, as its name implies, is for debugging.
    """

    surface = None
    axisScale = 10.0
    PPM = 1.0 #20

    def __init__(self, **kwargs):
        b2DrawExtended.__init__(self, **kwargs)
        self.flipX = False
        self.flipY = True
        self.convertVertices = True

    #def convertScreenToWorld(self, pos):
    #    return pos[0]*self.PPM, pos[1]*self.PPM

    #def to_screen(self, point):
    #    """to_screen(b2DrawExtended self, b2Vec2 point) -> PyObject *"""
    #    #point = self.convertScreenToWorld(point)
    #    return super().to_screen(point)

    def StartDraw(self):
        self.zoom = self.PPM
        self.center = (400, 300)
        self.offset = (0, 0)
        self.screenSize = (800, 600)

    def EndDraw(self):
        pass

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size / self.zoom, color, drawwidth=0)

    def DrawAABB(self, aabb, color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        points = [(aabb.lowerBound.x, aabb.lowerBound.y),
                  (aabb.upperBound.x, aabb.lowerBound.y),
                  (aabb.upperBound.x, aabb.upperBound.y),
                  (aabb.lowerBound.x, aabb.upperBound.y)]

        pygame.draw.aalines(self.surface, color, True, points)

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        pygame.draw.aaline(self.surface, color, p1, p2)

    def DrawTransform(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        p2 = self.to_screen(p1 + self.axisScale * xf.R.x_axis)
        p3 = self.to_screen(p1 + self.axisScale * xf.R.y_axis)
        p1 = self.to_screen(p1)
        pygame.draw.aaline(self.surface, (255, 0, 0), p1, p2)
        pygame.draw.aaline(self.surface, (0, 255, 0), p1, p3)

    def DrawCircle(self, center, radius, color, drawwidth=1):
        """
        Draw a wireframe circle given the center, radius, axis of orientation
        and color.
        """
        radius *= self.zoom
        if radius < 1:
            radius = 1
        else:
            radius = int(radius)

        pygame.draw.circle(self.surface, color,
                           center, radius, drawwidth)

    def DrawSolidCircle(self, center, radius, axis, color):
        """
        Draw a solid circle given the center, radius, axis of orientation and
        color.
        """
        radius *= self.zoom
        if radius < 1:
            radius = 1
        else:
            radius = int(radius)

        pygame.draw.circle(self.surface, (color / 2) + [127],
                           center, radius, 0)
        pygame.draw.circle(self.surface, color, center, radius, 1)
        pygame.draw.aaline(self.surface, (255, 0, 0), center,
                           (center[0] - radius * axis[0],
                            center[1] + radius * axis[1]))

    def DrawPolygon(self, vertices, color):
        """
        Draw a wireframe polygon given the screen vertices with the specified color.
        """
        if not vertices:
            return

        if len(vertices) == 2:
            pygame.draw.aaline(self.surface, color,
                               vertices[0], vertices)
        else:
            pygame.draw.polygon(self.surface, color, vertices, 1)

    def DrawSolidPolygon(self, vertices, color):
        """
        Draw a filled polygon given the screen vertices with the specified color.
        """
        if not vertices:
            return

        if len(vertices) == 2:
            pygame.draw.aaline(self.surface, color,
                               vertices[0], vertices[1])
        else:
            pygame.draw.polygon(
                self.surface, (color / 2) + [127], vertices, 0)
            pygame.draw.polygon(self.surface, color, vertices, 1)