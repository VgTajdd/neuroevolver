from b2d.actor_b2d import ActorB2D
from b2d.simulation_b2d import SimulationB2D
from Box2D import b2AABB, b2Vec2, b2QueryCallback, b2_dynamicBody, b2Color, b2CircleShape, b2FixtureDef, b2BodyDef, b2PolygonShape, b2Filter
import settings, pygame

class SimulationB2DDIP(SimulationB2D):
    def __init__(self, container, width, height):
        self.m_keyboardInputsEnabled = False
        SimulationB2D.__init__(self, container, width, height)

    #def init(self, genomes, config):
    #    super().init(genomes, config)
    #    self.m_systems = [NNDIPSystem(self, genome, config) for genome in genomes]

    def setupWorld(self):
        DIP(self)

    #def addNNDIPSystemToWorld(self, world):
    #    pass

class NNDIPSystem(object):
    """ Description of the class """
    def __init__(self, simulation, genome, config):
        pass

class DIP(object):
    def __init__(self, simulation):
        self.m_simulation = simulation
        self.box = self.createSimpleBox((400, 550), (40, 20))
        barA = self.createSimpleBox((400, 490), (10, 100))
        barB = self.createSimpleBox((400, 390), (10, 100))

        j1 = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=self.box.m_body,
                                                       bodyB=barA.m_body,
                                                       localAnchorA=(0, 0),
                                                       localAnchorB=(0, -50/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=False,
                                                       lowerAngle=0,
                                                       upperAngle=0)
        j2 = simulation.m_b2dWorld.CreateRevoluteJoint(bodyA=barA.m_body,
                                                       bodyB=barB.m_body,
                                                       localAnchorA=(0, 50/settings.B2D_PPM),
                                                       localAnchorB=(0, -50/settings.B2D_PPM),
                                                       enableMotor=False,
                                                       maxMotorTorque=1000,
                                                       enableLimit=False,
                                                       lowerAngle=0,
                                                       upperAngle=0)
        simulation.m_joints.append(j1)
        simulation.m_joints.append(j2)

    def createSimpleBox(self, screenBoxPosition, screenBoxSize):
        screenBoxWidth = screenBoxSize[0]
        screenBoxHeight = screenBoxSize[1]

        boxWidth = screenBoxWidth/settings.B2D_PPM
        boxHeight = screenBoxHeight/settings.B2D_PPM

        boxPosition = self.m_simulation.convertScreenToWorld(screenBoxPosition)

        shape = b2PolygonShape()
        shape.SetAsBox(boxWidth / 2, boxHeight / 2)

        fixture = b2FixtureDef()
        fixture.density = 1
        fixture.friction = 0.0
        fixture.shape = shape
        fixture.filter = b2Filter(
            groupIndex=0,
            categoryBits=0x0002,    # I am...
            maskBits=0x0001         # I collide with...
            )

        # body definition
        bodyDef = b2BodyDef()
        bodyDef.position.Set(boxPosition[0], boxPosition[1])
        bodyDef.type = b2_dynamicBody
        bodyDef.fixedRotation = False

        return self.m_simulation.addActor(ActorB2D(screenBoxPosition, (screenBoxWidth, screenBoxHeight)), bodyDef = bodyDef, fixture = fixture)

    def onKeyPress(self, event):
        if event == pygame.K_q:
            # apply gradual force upwards
            f = self.box.m_body.GetWorldVector(localVector=(0.0, 2000.0))
            p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 2.0))
            self.box.m_body.ApplyForce(f, p, True)
        #elif event == pygame.K_w:
        #    # apply immediate force upwards
        #    f = self.box.m_body.GetWorldVector(localVector=(0.0, 10.0))
        #    p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 2.0))
        #    self.box.m_body.ApplyLinearImpulse(f, p, True)
        elif event == pygame.K_LEFT:
            f = self.box.m_body.GetWorldVector(localVector=(-10.0, 0.0))
            p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 0.0))
            self.box.m_body.ApplyLinearImpulse(f, p, True)
        elif event == pygame.K_RIGHT:
            f = self.box.m_body.GetWorldVector(localVector=(10.0, 0.0))
            p = self.box.m_body.GetWorldPoint(localPoint=(0.0, 0.0))
            self.box.m_body.ApplyLinearImpulse(f, p, True)