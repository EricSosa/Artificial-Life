import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
import pygame
import random
import time
import numpy as np

random.seed(7)
WIDTH = 800
HEIGHT = 400
FPS = 80

class Ant(pygame.sprite.Sprite):
    def __init__(self,color,speed,carry):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,WIDTH), random.randint(0,HEIGHT))
        self.randx = 0
        self.randy = 0
        self.chain = False
        self.following = self
        self.speed = speed
        self.carry = carry
        self.carrylist = [self]

    def update(self, iteration, all_sprites, swarm):
        
        #change course at random times
        if iteration == random.randint(10,30):
            self.randx = random.uniform(-1,1)*self.speed
            self.randy = random.uniform(-1,1)*self.speed

        #follow chained ant
        if self.chain == True:
            self.randx = self.following.randx
            self.randy = self.following.randy
            #remove corpse
            if (self.randx == 0) & (self.randy == 0):
                all_sprites.remove(self)
                swarm.remove(self)               
        
        #move on x axis
        self.rect.centerx += self.randx
        #wrap around screen
        if self.rect.centerx >= WIDTH:
            self.rect.centerx = 1
        if self.rect.centerx <= 0:
            self.rect.centerx = WIDTH-1
        
        #move on y axis
        self.rect.centery += self.randy
        #wrap around screen
        if self.rect.centery >= HEIGHT:
            self.rect.centery = 1
        if self.rect.centery <= 0:
            self.rect.centery = HEIGHT-1

    def die(self,insect,all_sprites,swarm,start):
        if self.carry == 0:
            for i in self.carrylist:
                for ant in i.carrylist:
                    if ant != self:
                        ant.randx = 0
                        ant.randy = 0
                        all_sprites.remove(ant)
                        swarm.remove(ant)
                    insect.carry += 1
            #kill self at the end
            self.randx = 0
            self.randy = 0
            all_sprites.remove(self)
            swarm.remove(self)

class RedAnt(Ant):
    def __init__(self):
        #color, speed, strength
        Ant.__init__(self,'red',1,7)

class BlackAnt(Ant):
    def __init__(self):
        #color, speed, strength
        Ant.__init__(self,'black',2,5)

class BlueAnt(Ant):
    def __init__(self):
        #color, speed, strength
        Ant.__init__(self,'blue',3,3)

class Insect(Ant):
    def __init__(self):
        #color, speed, strength
        Ant.__init__(self,'green',2,999)
        self.image = pygame.Surface((10, 10))
        self.image.fill((20,180,20))


def main():
    times = [] 
    antcolor = ['Red', 'Blue','Black','Combined']
    #antammount = [150,180,210,240,270,300]
    antammount = [300]
    for thiscolor in antcolor:
        timescolor = []
        for ammount in antammount:
            timesammount = []
            for loop in range(1):
                life = 200
                pygame.init()
                pygame.mixer.init()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Weaver Ants")
                clock = pygame.time.Clock()
                bigfont = pygame.font.Font(None, 80)
                smallfont = pygame.font.Font(None, 45)


                all_sprites = pygame.sprite.Group()
                ants = pygame.sprite.Group()
                swarm = pygame.sprite.Group()

                #Add insect to kill
                insect = Insect()
                all_sprites.add(insect)
                swarm.add(insect)

                #Add ants
                if thiscolor == 'Red':
                    for i in range(ammount):
                        r = RedAnt()
                        all_sprites.add(r)
                        ants.add(r)

                if thiscolor == 'Blue':
                    for i in range(ammount):
                        r = BlueAnt()
                        all_sprites.add(r)
                        ants.add(r)
                
                if thiscolor == 'Black':
                    for i in range(ammount):
                        r = BlackAnt()
                        all_sprites.add(r)
                        ants.add(r)

                if thiscolor == 'Combined':
                    for i in range(int(ammount/3)):
                        r = RedAnt()
                        all_sprites.add(r)
                        ants.add(r)

                    for i in range(int(ammount/3)):
                        r = BlueAnt()
                        all_sprites.add(r)
                        ants.add(r)
                
                    for i in range(int(ammount/3)):
                        r = BlackAnt()
                        all_sprites.add(r)
                        ants.add(r)

                # Game loop
                running = True
                start = time.time()
                while running:
                    #pygame update screen
                    screen.fill(pygame.Color('white'))
                    all_sprites.draw(screen)
                    pygame.display.flip()

                    # keep loop running at the right speed
                    clock.tick(FPS)
                    # Process input (events)
                    for event in pygame.event.get():
                        # check for closing window
                        if event.type == pygame.QUIT:
                            running = False

                    # Update each frame
                    #count 20 frames for random movement
                    if i < 30:
                        i += 1
                    else:
                        i = 0
                    pygame.event.get()
                    all_sprites.update(i,all_sprites,swarm)
                    #check collisions between roaming ants and swarm
                    hits = pygame.sprite.groupcollide(ants, swarm, False, False)
                    if hits:
                        for ant in hits:
                            for chained in hits[ant]:
                                #follow the chained ant it collided with
                                ant.chain = True
                                ant.following = chained
                                #now its part of the army swarm
                                ants.remove(ant)
                                swarm.add(ant)
                                #another ant to carry
                                chained.carry -= 1
                                chained.carrylist.append(ant)
                                #check if someone died
                                chained.die(insect,all_sprites,swarm,start)
                                #lower enemy life
                                life -= 1
                                insect.carrylist.append(ant)
                    if life <= 0:
                        end = time.time()
                        timesammount.append(int(end - start))
                        pygame.display.quit()
                        all_sprites = None
                        ants = None
                        swarm = None
                        insect = None
                        running = False
            timescolor.append(timesammount)
        times.append(timescolor)
    #np.savez('times75.npz', times=times)
    pygame.quit() 

if __name__ == '__main__':
    main()