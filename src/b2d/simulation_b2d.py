from core.simulation_base import SimulationBase
from core.debug_drawing import DebugDrawing
from b2d.debug_draw_extended import DebugDrawExtended
from b2d.actor_b2d import ActorB2D
import Box2D
from Box2D import b2AABB, b2Vec2, b2QueryCallback, b2_dynamicBody, b2Color, b2CircleShape, b2FixtureDef, b2BodyDef
from Box2D.b2 import world, polygonShape
import settings
import core.colors as colors

class SimulationB2D(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)

        # --- pybox2d world setup ---
        # Create the world
        self.m_b2dWorld = world(gravity=(0, -10), doSleep=True)
        self.m_debugDraw = DebugDrawExtended(surface=settings.OBJ_SURFACE)
        self.m_b2dWorld.renderer = self.m_debugDraw

        self.m_b2dWorld.warmStarting = True
        self.m_b2dWorld.continuousPhysics = True
        self.m_b2dWorld.subStepping = False

        self.m_groundBody = None

        self.mouseJoint = None

        self.colours = {
            'mouse_point': b2Color(0, 1, 0),
            'joint_line': b2Color(0.8, 0.8, 0.8)
        }

        self.m_joints = []

        self.init()
        self.setupWorld()

    def addActor(self, actor, static = True, bodyDef = None, fixture = None):
        actor = super().addActor(actor)
        if bodyDef and fixture:
            actor.m_body = self.m_b2dWorld.CreateBody(bodyDef)
            actor.m_body.CreateFixture(fixture)
        else:
            if static:
                # box is defined by a vector from it's center to a corner, this way,
                # we use actor.m_size[0] * 0.5
                actor.m_body = self.m_b2dWorld.CreateStaticBody(position=self.convertScreenToWorld(actor.m_position),
                                                                shapes=polygonShape(box=(actor.m_size[0]*0.5/settings.B2D_PPM, actor.m_size[1]*0.5/settings.B2D_PPM)))
            else:
                actor.m_body = self.m_b2dWorld.CreateDynamicBody(position=self.convertScreenToWorld(actor.m_position),
                                                                 angle=actor.m_angle)
                fixture = actor.m_body.CreatePolygonFixture(box=(actor.m_size[0]*0.5/settings.B2D_PPM, actor.m_size[1]*0.5/settings.B2D_PPM),
                                                            density=1, friction=0.3)
        return actor

    def init(self):
        actorGround = self.addActor(ActorB2D((400, 580), (800, 40)))
        self.m_groundBody = actorGround.m_body

    def setupWorld(self):
        # circle shape
        shape = b2CircleShape(radius=50/settings.B2D_PPM)

        # fixture
        fixture = b2FixtureDef()
        fixture.density = 1
        fixture.friction = 0.3
        fixture.shape = shape
        #fixture.userData = new UserDataInfo(name, bRadius * 2, bRadius * 2)

        # body definition
        bodyDef = b2BodyDef()
        bodyDef.position.Set((300)/settings.B2D_PPM, (300)/settings.B2D_PPM)
        bodyDef.type = b2_dynamicBody
        bodyDef.fixedRotation = False

        circle = self.addActor(ActorB2D((300, 300), (50, 50)), bodyDef = bodyDef, fixture = fixture)

        box = self.addActor(ActorB2D((100, 400), (40, 20)), False)

        #j = self.m_b2dWorld.CreateRevoluteJoint(bodyA=box.m_body,
        #                                        bodyB=circle.m_body,
        #                                        localAnchorA=(0, 5),
        #                                        localAnchorB=(0, 0),
        #                                        enableMotor=False,
        #                                        maxMotorTorque=1000,
        #                                        enableLimit=True,
        #                                        lowerAngle=0,
        #                                        upperAngle=1)

        j = self.m_b2dWorld.CreateRevoluteJoint(bodyA=box.m_body,
                                                bodyB=circle.m_body,
                                                localAnchorA=(0, 5),
                                                localAnchorB=(0, 0),
                                                enableMotor=True,
                                                maxMotorTorque=1000,
                                                motorSpeed=1, #rad/s
                                                enableLimit=False,
                                                lowerAngle=0,
                                                upperAngle=1)

        self.m_joints.append(j)

    def update(self, dt):
        self.m_b2dWorld.Step(dt/1000, 10, 10)
        self.m_b2dWorld.ClearForces()
        super().update(dt)

    def debugDraw(self, screen):
        #for actor in self.m_actorManager.m_actors:
        #    for fixture in actor.m_body.fixtures:
        #        # The fixture holds information like density and friction,
        #        # and also the shape.
        #        shape = fixture.shape

        #        # Naively assume that this is a polygon shape. (not good normally!)
        #        # We take the body's transform and multiply it with each
        #        # vertex, and then convert from meters to pixels with the scale
        #        # factor.
        #        vertices = [(actor.m_body.transform * v) * settings.B2D_PPM for v in shape.vertices]

        #        # But wait! It's upside-down! Pygame and Box2D orient their
        #        # axes in different ways. Box2D is just like how you learned
        #        # in high school, with positive x and y directions going
        #        # right and up. Pygame, on the other hand, increases in the
        #        # right and downward directions. This means we must flip
        #        # the y components.
        #        vertices = [(v[0], settings.APP_HEIGHT - v[1]) for v in vertices]

        #        self.m_debugDraw.DrawSolidPolygon(vertices, b2Color(colors.GREEN))

                #vertices = [self.m_debugDraw.to_screen(actor.m_body.transform * v) for v in shape.vertices]
                #self.m_debugDraw.DrawSolidPolygon(vertices, b2Color(colors.GREEN))

        self.m_debugDraw.StartDraw()
        self.m_b2dWorld.DrawDebugData()
        if self.mouseJoint:
            p1 = self.m_debugDraw.to_screen(self.mouseJoint.anchorB)
            p2 = self.m_debugDraw.to_screen(self.mouseJoint.target)
            self.m_debugDraw.DrawPoint(p1, 2.5, self.colours['mouse_point'])
            self.m_debugDraw.DrawPoint(p2, 2.5, self.colours['mouse_point'])
            self.m_debugDraw.DrawSegment(p1, p2, self.colours['joint_line'])
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
        return pos[0]/settings.B2D_PPM, (settings.APP_HEIGHT - pos[1])/settings.B2D_PPM

    def free(self):
        [self.m_b2dWorld.DestroyJoint(joint) for joint in self.m_joints]
        [self.m_b2dWorld.DestroyBody(actor.m_body) for actor in self.m_actorManager.m_actors]
        self.m_b2dWorld = None
        self.m_debugDraw = None
        return super().free()

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