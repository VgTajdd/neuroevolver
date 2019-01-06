from core.simulation_base import SimulationBase
from steering.actor_steering import ActorSteering
from core.simulation_base import SimulationActor
from enums import NPCType
from enums import SteeringBehaviourType
import core.colors as colors
import random

class SimulationFPGA(SimulationBase):
    def __init__(self, container, width, height):
        SimulationBase.__init__(self, container, width, height)
        self.m_foodActors = []
        self.m_poisonActors = []
        self.m_fpVehicles = []
        self.m_totalFood = 20
        self.m_totalPoison = 20
        self.m_initialNumVehicles = 10
        self.init()

    def init(self):
        self.createFood(self.m_totalFood)
        self.createPoison(self.m_totalPoison)
        self.createVehicles(self.m_initialNumVehicles)

    def updateTime(self, dt):
        super().updateTime(dt)

        self.m_debugContainer.clear()
        # Code for adding debug shapes...
        # this can be passed to actors to see connections between player and food or poison.

        # Removing dead actors.
        for actor in self.m_foodActors:
            if actor.m_isAwaitingToDelete:
                self.m_foodActors.remove(actor)
        for actor in self.m_poisonActors:
            if actor.m_isAwaitingToDelete:
                self.m_poisonActors.remove(actor)

        for actor in self.m_fpVehicles:
            if actor.m_isAwaitingToDelete:
                self.m_fpVehicles.remove(actor)
                continue

            # Keeping alive actors inside screen bounds.
            if actor.m_position[0] < 0 and actor.m_velocity.x < 0:
                actor.m_velocity.x *= -1
            if actor.m_position[0] > self.m_width and actor.m_velocity.x > 0:
                actor.m_velocity.x *= -1
            if actor.m_position[1] < 0 and actor.m_velocity.y < 0:
                actor.m_velocity.y *= -1
            if actor.m_position[1] > self.m_height and actor.m_velocity.y > 0:
                actor.m_velocity.y *= -1

            for fActor in self.m_foodActors:
                if actor.hasCircleCollisionWith(fActor):
                    actor.addHealth(fActor.m_healthBonus)
                    fActor.setAwaitingToDelete(True)

            for pActor in self.m_poisonActors:
                if actor.hasCircleCollisionWith(pActor):
                    actor.addHealth(pActor.m_healthBonus)
                    pActor.setAwaitingToDelete(True)

        # Creating new actors.
        self.createVehicles(self.m_initialNumVehicles - len(self.m_fpVehicles))
        self.createFood(self.m_totalFood - len(self.m_foodActors))
        self.createPoison(self.m_totalPoison - len(self.m_poisonActors))

    def createFood(self, total):
        for i in range(0, total):
            randomX = random.randint(10, self.m_width - 10)
            randomY = random.randint(10, self.m_height - 10)
            foodActor = NPC((randomX, randomY), npcType = NPCType.FOOD)
            self.addActor(foodActor)
            self.m_foodActors.append(foodActor)

            for fpVehicle in self.m_fpVehicles:
                component = fpVehicle.addSteeringComponent(SteeringBehaviourType.SEEK, foodActor)
                if component:
                    component.m_steeringConstant = fpVehicle.m_steeringConstantFood
                    component.m_steeringRadius = fpVehicle.m_steeringRadiusFood

    def createPoison(self, total):
        for i in range(0, total):
            randomX = random.randint(10, self.m_width - 10)
            randomY = random.randint(10, self.m_height - 10)
            poisonActor = NPC((randomX, randomY), npcType = NPCType.POISON)
            self.addActor(poisonActor)
            self.m_poisonActors.append(poisonActor)

            for fpVehicle in self.m_fpVehicles:
                component = fpVehicle.addSteeringComponent(SteeringBehaviourType.FLEE, poisonActor)
                if component:
                    component.m_steeringConstant = fpVehicle.m_steeringConstantPoison
                    component.m_steeringRadius = fpVehicle.m_steeringRadiusPoison

    def createVehicles(self, total):
        chooseParent = False
        possibleParents = []
        if len(self.m_fpVehicles) != 0:
            chooseParent = True
            possibleParents = self.m_fpVehicles.copy()

        for i in range(0, total):
            randomX = random.randint(10, self.m_width - 10)
            randomY = random.randint(10, self.m_height - 10)
            fpVehicle = FPVehicle((randomX, randomY), (10, 20), imagePath = 'assets/actor0.png')
            self.addActor(fpVehicle)
            self.m_fpVehicles.append(fpVehicle)

            if chooseParent:
                parent = self.getBestVehicle(possibleParents)

                # Copying from vehicle chosen as parent.
                fpVehicle.m_steeringConstantFood = parent.m_steeringConstantFood
                fpVehicle.m_steeringConstantPoison = parent.m_steeringConstantPoison
                fpVehicle.m_steeringRadiusFood = parent.m_steeringRadiusFood
                fpVehicle.m_steeringRadiusPoison = parent.m_steeringRadiusPoison

                # Adding little mutation.
                fpVehicle.m_steeringConstantFood += random.uniform(-0.001, 0.001)
                fpVehicle.m_steeringConstantPoison += random.uniform(-0.001, 0.001)
                fpVehicle.m_steeringRadiusFood += random.uniform(-5, 5)
                fpVehicle.m_steeringRadiusPoison += random.uniform(-5, 5)
            
            # Add existent poison component.
            for pActor in self.m_poisonActors:
                component = fpVehicle.addSteeringComponent(SteeringBehaviourType.FLEE, pActor)
                if component:
                    component.m_steeringConstant = fpVehicle.m_steeringConstantPoison
                    component.m_steeringRadius = fpVehicle.m_steeringRadiusPoison

            # Add existent food component.
            for fActor in self.m_foodActors:
                component = fpVehicle.addSteeringComponent(SteeringBehaviourType.SEEK, fActor)
                if component:
                    component.m_steeringConstant = fpVehicle.m_steeringConstantFood
                    component.m_steeringRadius = fpVehicle.m_steeringRadiusFood

    def getBestVehicle(self, possibleParents):
        best = None
        sumOfFitness = 0
        cum = 0

        for pparent in possibleParents:
            sumOfFitness += pparent.m_timeAlive

        f = random.randint(0, sumOfFitness)

        for pparent in possibleParents:
            cum += pparent.m_timeAlive
            if cum > f:
                best = pparent
                break

        return best

    def free(self):
        for actor in self.m_foodActors:
            actor.free()
            actor = None
        self.m_foodActors.clear()
        self.m_foodActors = None

        for actor in self.m_poisonActors:
            actor.free()
            actor = None
        self.m_poisonActors.clear()
        self.m_poisonActors = None

        for actor in self.m_fpVehicles:
            actor.free()
            actor = None
        self.m_fpVehicles.clear()
        self.m_fpVehicles = None

class NPC(SimulationActor):
    def __init__(self, pos, imagePath = '', npcType = NPCType.NONE):
        SimulationActor.__init__(self, pos, (15, 15), imagePath = imagePath)
        self.m_healthBonus = 0
        self.m_type = npcType
        self.init()

    def init(self):
        if self.m_type == NPCType.FOOD:
            self.setImage('assets/food.png')
            self.m_healthBonus = 10
        elif self.m_type == NPCType.POISON:
            self.setImage('assets/poison.png')
            self.m_healthBonus = -50

class FPVehicle(ActorSteering):
    ''' This only will seek 1 food and flee 1 poison, even if all of them are added.
    Also m_timeAlive will be used as fitness to produce new vehicles in the evolutive 
    process. '''
    def __init__(self, pos, size, color = colors.WHITE, imagePath = '', alpha = 255, layer = 1):
        ActorSteering.__init__(self, pos, size, color, imagePath, alpha, layer)
        self.m_health = 100
        self.m_totalHealth = self.m_health
        self.m_wasteHealthSpeed = 0.01 #hp/ms -> 10 hp/s
        self.m_behaviour.m_useOneActorPerCompType = True
        self.m_timeAlive = 0

        # Parameters to evolve.
        self.m_steeringConstantFood = random.uniform(-0.01, 0.01)
        self.m_steeringConstantPoison = random.uniform(-0.01, 0.01)
        self.m_steeringRadiusFood = random.uniform(50, 100)
        self.m_steeringRadiusPoison = random.uniform(50, 100)

    def update(self, dt):
        super().update(dt)
        self.m_health -= self.m_wasteHealthSpeed * dt
        self.m_timeAlive += dt

        ##
        self.m_alpha = 255 * (self.m_health / self.m_totalHealth)
        if self.m_alpha > 255:
            self.m_alpha = 255
        if self.m_alpha < 0:
            self.m_alpha = 0
        self.repaint()
        ##

        if self.m_health <= 0:
            self.m_isAwaitingToDelete = True