from core.simulation_base import SimulationBase
from core.actor import DraggableActor
from core.debug_drawing import DebugDrawing
from steering.actor_steering import ActorSteering
from physics.simple_pendulum import SimplePendulum
from physics.inverted_pendulum import InvertedPendulum
from neat_dycicle.dycicle import Dycicle
from enums import SteeringBehaviourType
import core.colors as colors

from b2d.debug_draw_extended import DebugDrawExtended
import Box2D
from Box2D import b2AABB, b2Vec2, b2QueryCallback, b2_dynamicBody, b2Color
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody
import settings

class SimulationSteering(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.m_invertedPendulum = None
        self.m_target = None
        self.m_vehicle = None

        # --- pybox2d world setup ---
        # Create the world
        self.m_b2dWorld = world(gravity=(0, -10), doSleep=True)

        self.debugDraw = DebugDrawExtended(surface=settings.OBJ_SURFACE)
        #self.m_b2dWorld.SetDebugDraw(self.debugDraw)
        # And a static body to hold the ground shape
        self.ground_body = self.m_b2dWorld.CreateStaticBody(position=(0, 1),shapes=polygonShape(box=(50, 5)))
        # Create a dynamic body
        self.dynamic_body = self.m_b2dWorld.CreateDynamicBody(position=(10, 15), angle=15)
        # And add a box fixture onto it (with a nonzero density, so it will move)
        box = self.dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

        self.PPM = 20.0 # pixels per meter
        self.mouseJoint = None

        self.colours = {
            'mouse_point': b2Color(0, 1, 0),
            'bomb_center': b2Color(0, 0, 1.0),
            'bomb_line': b2Color(0, 1.0, 1.0),
            'joint_line': b2Color(0.8, 0.8, 0.8),
            'contact_add': b2Color(0.3, 0.95, 0.3),
            'contact_persist': b2Color(0.3, 0.3, 0.95),
            'contact_normal': b2Color(0.4, 0.9, 0.4),
        }

        self.init()

    def init(self):
        self.m_target = DraggableActor((400, 300), (20, 20), color = colors.BLUE)
        self.addActor(self.m_target)

        actor = ActorSteering((750, 500), (10, 20), imagePath = "assets/actor0.png", layer = 2)
        actor.addSteeringComponent(SteeringBehaviourType.SEEK, self.m_target)
        self.addActor(actor)

        actor2 = ActorSteering((100, 100), (10, 20), imagePath = "assets/actor1.png", layer = 2)
        actor2.addSteeringComponent(SteeringBehaviourType.SEEK, self.m_target)
        self.addActor(actor2)

        # Added simple pendulum.
        self.addActor(SimplePendulum((100, 100), (10, 100), rc = (5, 0)))

        # Added inverted pendulum.
        self.m_invertedPendulum = InvertedPendulum((500, 100), (10, 100), rc = (5, 100), layer = 2)
        self.m_invertedPendulum.addToSimulation(self)

        self.m_vehicle = Dycicle((400, 500), (20, 20), imagePath = "assets/actor0.png", layer = 2)
        self.addActor(self.m_vehicle)

    def onKeyPress(self, event):
        self.m_invertedPendulum.onKeyPress(event)

    def onKeyRelease(self, event):
        self.m_invertedPendulum.onKeyRelease(event)

    def onMouseMove(self, event):
        if self.m_target:
            self.m_target.onMouseMove(event)

        p = self.convertScreenToWorld(event.pos)

        self.mouseWorld = p
        if self.mouseJoint:
            self.mouseJoint.target = p

    def onMouseDown(self, event):
        if self.m_target:
            self.m_target.onMouseDown(event)

        p = self.convertScreenToWorld(event.pos)

        if self.mouseJoint is not None:
            return

        # Create a mouse joint on the selected body (assuming it's dynamic)
        # Make a small box.
        aabb = b2AABB(lowerBound=b2Vec2(p) - (0.001, 0.001),
                      upperBound=b2Vec2(p) + (0.001, 0.001))

        # Query the world for overlapping shapes.
        query = fwQueryCallback(p)
        self.m_b2dWorld.QueryAABB(query, aabb)

        if query.fixture:
            body = query.fixture.body
            # A body was selected, create the mouse joint
            self.mouseJoint = self.m_b2dWorld.CreateMouseJoint(
                bodyA=self.ground_body,
                bodyB=body,
                target=p,
                maxForce=1000.0 * body.mass)
            body.awake = True

    def onMouseRelease(self, event):
        if self.m_target:
            self.m_target.onMouseRelease(event)

        if self.mouseJoint:
            self.m_b2dWorld.DestroyJoint(self.mouseJoint)
            self.mouseJoint = None

    def convertScreenToWorld(self, pos):
        return pos[0]/self.PPM, (settings.APP_HEIGHT - pos[1])/self.PPM

    def update(self, dt):
        super().update(dt)
        for body in (self.ground_body, self.dynamic_body):  # or: world.bodies
        # The body gives us the position and angle of its shapes
            for fixture in body.fixtures:
                # The fixture holds information like density and friction,
                # and also the shape.
                shape = fixture.shape

                # Naively assume that this is a polygon shape. (not good normally!)
                # We take the body's transform and multiply it with each
                # vertex, and then convert from meters to pixels with the scale
                # factor.
                vertices = [(body.transform * v) * self.PPM for v in shape.vertices]

                # But wait! It's upside-down! Pygame and Box2D orient their
                # axes in different ways. Box2D is just like how you learned
                # in high school, with positive x and y directions going
                # right and up. Pygame, on the other hand, increases in the
                # right and downward directions. This means we must flip
                # the y components.
                vertices = [(v[0], settings.APP_HEIGHT - v[1]) for v in vertices]

                self.m_debugContainer.append(DebugDrawing.polygon(colors.ORANGE, vertices))

        self.m_b2dWorld.Step(dt/1000, 10, 10)
        self.m_b2dWorld.ClearForces()
        self.m_b2dWorld.DrawDebugData()

        self.debugDraw .StartDraw()

        if self.mouseJoint:
            p1 = self.debugDraw.to_screen(self.mouseJoint.anchorB)
            p2 = self.debugDraw.to_screen(self.mouseJoint.target)

            self.debugDraw.DrawPoint(p1, 5,
                                   self.colours['mouse_point'])
            self.debugDraw.DrawPoint(p2, 5,
                                   self.colours['mouse_point'])
            self.debugDraw.DrawSegment(p1, p2, self.colours['joint_line'])

        self.debugDraw .EndDraw()

        self.m_debugContainer += self.m_vehicle.m_debugShapes


class fwQueryCallback(b2QueryCallback):

    def __init__(self, p):
        super(fwQueryCallback, self).__init__()
        self.point = p
        self.fixture = None

    def ReportFixture(self, fixture):
        body = fixture.body
        if body.type == b2_dynamicBody:
            inside = fixture.TestPoint(self.point)
            if inside:
                self.fixture = fixture
                # We found the object, so stop the query
                return False
        # Continue the query
        return True
