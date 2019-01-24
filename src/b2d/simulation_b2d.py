from core.simulation_base import SimulationBase
from core.debug_drawing import DebugDrawing
from b2d.debug_draw_extended import DebugDrawExtended
from b2d.actor_b2d import ActorB2D
import Box2D
from Box2D import b2AABB, b2Vec2, b2QueryCallback, b2_dynamicBody, b2Color
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody
import settings
import core.colors as colors

class SimulationB2D(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)

        # --- pybox2d world setup ---
        # Create the world
        self.m_b2dWorld = world(gravity=(0, -10), doSleep=True)
        self.m_debugDraw = DebugDrawExtended(surface=settings.OBJ_SURFACE)
        self.m_groundBody = None
        ## And a static body to hold the ground shape
        ##self.ground_body = self.m_b2dWorld.CreateStaticBody(position=(20, 2),shapes=polygonShape(box=(20, 1)))
        #self.ground_body = self.m_b2dWorld.CreateStaticBody(position=(20, 2))
        #box = self.ground_body.CreatePolygonFixture(box=(20, 1), density=1, friction=0.3)
        ## Create a dynamic body
        #self.dynamic_body = self.m_b2dWorld.CreateDynamicBody(position=(10, 15), angle=15)
        ## And add a box fixture onto it (with a nonzero density, so it will move)
        #box = self.dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

        self.PPM = 1.0 #20.0 # pixels per meter
        self.mouseJoint = None

        self.init()

    def addActor(self, actor, static = True):
        actor = super().addActor(actor)
        if static:
            actor.m_body = self.m_b2dWorld.CreateStaticBody(position=(actor.m_position[0]/self.PPM, actor.m_position[1]/self.PPM),
                                                            shapes=polygonShape(box=(actor.m_size[0]*0.5/self.PPM, actor.m_size[1]*0.5/self.PPM)))
            #actor.body = self.m_b2dWorld.CreateStaticBody(position=actor.m_position,shapes=polygonShape(box=(20, 1)))
        else:
            actor.m_body = self.m_b2dWorld.CreateDynamicBody(position=(actor.m_position[0]/self.PPM, actor.m_position[1]/self.PPM),
                                                             angle=actor.m_angle)
            fixture = actor.m_body.CreatePolygonFixture(box=(actor.m_size[0]*0.5/self.PPM, actor.m_size[1]*0.5/self.PPM),
                                                        density=1, friction=0.3)
        return actor

    def init(self):
        actorGround = self.addActor(ActorB2D((400, 40), (400, 20)))
        self.addActor(ActorB2D((200, 300), (40, 20)), False)
        self.m_groundBody = actorGround.m_body

    def update(self, dt):
        super().update(dt)
        self.m_b2dWorld.Step(dt/1000, 10, 10)
        self.m_b2dWorld.ClearForces()

    def debugDraw(self, screen):
        for actor in self.m_actorManager.m_actors:
            for fixture in actor.m_body.fixtures:
                # The fixture holds information like density and friction,
                # and also the shape.
                shape = fixture.shape

                # Naively assume that this is a polygon shape. (not good normally!)
                # We take the body's transform and multiply it with each
                # vertex, and then convert from meters to pixels with the scale
                # factor.
                vertices = [(actor.m_body.transform * v) * self.PPM for v in shape.vertices]

                # But wait! It's upside-down! Pygame and Box2D orient their
                # axes in different ways. Box2D is just like how you learned
                # in high school, with positive x and y directions going
                # right and up. Pygame, on the other hand, increases in the
                # right and downward directions. This means we must flip
                # the y components.
                vertices = [(v[0], settings.APP_HEIGHT - v[1]) for v in vertices]

                self.m_debugContainer.append(DebugDrawing.polygon(colors.GRAY, vertices, 0))
                self.m_debugContainer.append(DebugDrawing.polygon(colors.WHITE, vertices))

        self.m_debugDraw.StartDraw()
        if self.mouseJoint:
            p1 = self.m_debugDraw.to_screen(self.mouseJoint.anchorB)
            p2 = self.m_debugDraw.to_screen(self.mouseJoint.target)
            self.m_debugDraw.DrawPoint(p1, 5, b2Color(colors.RED))
            self.m_debugDraw.DrawPoint(p2, 5, b2Color(colors.RED))
            self.m_debugDraw.DrawSegment(p1, p2, b2Color(colors.GREY_BLUE))
        self.m_debugDraw.EndDraw()

    def onKeyPress(self, event):
        pass

    def onKeyRelease(self, event):
        pass

    def onMouseMove(self, event):
        p = self.convertScreenToWorld(event.pos)

        self.mouseWorld = p
        if self.mouseJoint:
            self.mouseJoint.target = p

    def onMouseDown(self, event):
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
                bodyA=self.m_groundBody,
                bodyB=body,
                target=p,
                maxForce=1000.0 * body.mass)
            body.awake = True

    def onMouseRelease(self, event):
        if self.mouseJoint:
            self.m_b2dWorld.DestroyJoint(self.mouseJoint)
            self.mouseJoint = None

    def convertScreenToWorld(self, pos):
        return pos[0]/self.PPM, (settings.APP_HEIGHT - pos[1])/self.PPM

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
