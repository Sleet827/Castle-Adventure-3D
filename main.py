from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from panda3d.core import *
from classes import *
loadPrcFile("config/Config.prc")

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.displayMenu()
    
    def displayMenu(self):
        self.label = DirectLabel(text="Castle Adventure 3D", pos=(400, 0, -250), scale=50, parent=self.pixel2d)
        self.button = DirectButton(text="Start", pos=(400, 0, -350), scale=50, parent=self.pixel2d, command=self.loadGame)
        self.bgImage = OnscreenImage(image="castle.png", scale=1.4)
        
    def loadGame(self):
        self.label.destroy()
        self.button.destroy()
        self.bgImage.destroy()
        
        self.disableMouse()
        
        self.cTrav = CollisionTraverser()
        self.pickerTraverser = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.addInPattern("%fn-into-%in")
        self.pusher.setHorizontal(True)
        self.queue = CollisionHandlerQueue()
        
        self.room = self.loader.loadModel("models/room.bam")
        self.room.setH(270)
        self.room.reparentTo(self.render)
        
        self.player = Player(Point3(0, -20, 2))
        
        self.keyMap = {"w" : False, "a" : False, "s" : False, "d" : False, "arrow_left" : False, "arrow_right" : False}
        
        for key in self.keyMap:
            self.accept(key, self.updateKeyMap, [key, True])
            self.accept(key + "-up", self.updateKeyMap, [key, False])
        
        self.taskMgr.add(self.update, "update")
        
        wallNode = CollisionNode("wall")
        wallSolid = CollisionCapsule(-4, -6, 1, -1, -6, 1, 0.5)
        wallNode.addSolid(wallSolid)
        wallC = render.attachNewNode(wallNode)
        
        wallNode = CollisionNode("wall")
        wallSolid = CollisionPlane(Plane(Vec3(1, 0, 0), Point3(-5, 0, 2)))
        wallNode.addSolid(wallSolid)
        wallC = render.attachNewNode(wallNode)
        
        wallNode = CollisionNode("wall")
        wallSolid = CollisionPlane(Plane(Vec3(0, 1, 0), Point3(6, -15, 2)))
        wallNode.addSolid(wallSolid)
        wallC = render.attachNewNode(wallNode)
        
        wallNode = CollisionNode("wall")
        wallSolid = CollisionPlane(Plane(Vec3(-1, 0, 0), Point3(5, -5, 2)))
        wallNode.addSolid(wallSolid)
        wallC = render.attachNewNode(wallNode)
        
        wallNode = CollisionNode("wall")
        wallSolid = CollisionPlane(Plane(Vec3(0, -1, 0), Point3(-3, 5, 2)))
        wallNode.addSolid(wallSolid)
        wallC = render.attachNewNode(wallNode)
        
        self.monster = BabyMonster(Point3(0.25, 0.25, 0.25))
        
        self.healthText = OnscreenText("Health: " + str(self.player.health), pos=(-1.1, 0.9), scale=0.07, mayChange=True)
        
        self.accept("monster-into-player", self.monsterToPlayer)
        self.taskMgr.add(self.checkGameOver, "Check Game Over")
        
        self.pickerNode = CollisionNode("picker")
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setIntoCollideMask(0)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerTraverser.addCollider(self.pickerNP, self.queue)
        
        self.accept("mouse1", self.click)
        self.taskMgr.add(self.checkmonsterDead, "Check Monster Dead")
        
        #self.accept("p", self.printPos)
        
    """def printPos(self):
        print(self.camera.getPos())"""
    
    def monsterToPlayer(self, collisionEntry):
        self.player.health -= 1
        self.healthText.setText("Health: " + str(self.player.health))
    
    def checkGameOver(self, task):
        if self.player.health <= 0:
            gameOverText = OnscreenText("GAME OVER", pos=(0, 0), scale=0.25)
             
        return Task.cont
    
    def checkmonsterDead(self, task):
        if self.monster.health <= 0:
            self.monster.actor.cleanup()
            self.monster.actor.removeNode()
                   
        return Task.cont 
    
    def click(self):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(self.camNode, mpos.x, mpos.y)
        
        self.pickerTraverser.traverse(self.render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            pickedObj = self.queue.getEntry(1).getIntoNodePath()
            pickedObj = pickedObj.findNetPythonTag("monster")
            if not pickedObj.isEmpty():
                self.monster.health -= 1
    
    def updateKeyMap(self, key, value):
        self.keyMap[key] = value
        
    def update(self, task):
        dt = globalClock.getDt()
        
        self.player.update(self.keyMap, dt)
        if not self.monster.actor.isEmpty(): # This checks if the monster is still alive.
            self.monster.update(self.player, dt)
        
        return Task.cont
        
game = Game()
game.run()