from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

class Player(DirectObject):
    def __init__(self, pos):
        self.player = base.camera
        self.player.setPos(pos)
        
        self.health = 10
            
        playerCenter = self.player.getBounds().getCenter()
        playerRad = 2
        cNode = CollisionNode("player")
        cNode.addSolid(CollisionSphere(playerCenter, playerRad))
        playerC = self.player.attachNewNode(cNode)
        
        base.cTrav.addCollider(playerC, base.pusher)
        base.pusher.addCollider(playerC, self.player)
    
    def update(self, keys, dt):
        if keys.get("w"):
            self.player.setY(self.player, dt * 10)
        elif keys.get("a"):
            self.player.setX(self.player, dt * -5)
        elif keys.get("s"):
            self.player.setY(self.player, dt * -10)
        elif keys.get("d"):
            self.player.setX(self.player, dt * 5)
        elif keys.get("arrow_left"):
            self.player.setH(self.player, dt * 100)
        elif keys.get("arrow_right"):
            self.player.setH(self.player, dt * -100)

class BabyMonster(DirectObject):
    def __init__(self, scale):
        self.actor = Actor("models/monster1.egg", {"attack" : "models/monster1-pincer-attack-both.egg", "explode" : "./models/monster1-explode.egg"})
        self.actor.setScale(0.25, 0.25, 0.25)
        self.actor.reparentTo(base.render)
        self.actor.setPythonTag("monster", '1')
        self.actor.loop("attack")
        
        self.health = 10	
        
        monsterCenter = self.actor.getBounds().getCenter()
        monsterRad = 2
        monsterNode = CollisionNode("monster")
        monsterNode.addSolid(CollisionSphere(monsterCenter, monsterRad))
        monsterC = self.actor.attachNewNode(monsterNode)
        
        base.cTrav.addCollider(monsterC, base.pusher)
        base.pusher.addCollider(monsterC, self.actor)
        
    def update(self, player, dt):
        self.actor.lookAt(player.player)
        self.actor.setY(self.actor, dt * 10)