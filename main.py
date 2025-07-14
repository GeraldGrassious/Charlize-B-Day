import pygame, time, os, sys, random, asyncio, gc

import pygame.freetype

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def resourcepath(relativepath):
    if hasattr(sys, '_MEIPASS'):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.abspath(".")
    return os.path.join(basepath, relativepath)

async def loadlvl(lvl):
    print(lvl)
    for plat in platgroup:
        plat.kill()
        del plat
        gc.collect()
    if lvl == 0:
        Platform((1350, 100), 400)
        Platform((1200, 330))
        Platform((1050, 550))
        Platform((1250, 720))
        Platform((1100, 920))
    elif lvl == 1:
        #Platform((400, 420), 50, 600)
        #Platform((250, 380), 50, 500)
        Platform((700, 100))
    elif lvl == 2:
        pass
    elif lvl == 3:
        pass
    print(len(platgroup))
    await asyncio.sleep(0)


async def fade():
    global fadeframe, faderev, level, addfade
    leveltext = f"Level {level}"
    levelfont = pygame.freetype.Font("assets/cournew.ttf", 100)
    levelrect = levelfont.get_rect(leveltext)
    levelrect.center = screen.get_rect().center
    levelfont.render_to(screen, levelrect, leveltext, (0, 0, 0, fadeframe))
    #deathrect = deathtext.get_rect(center=(width / 2, height / 2))
    #screen.blit(leveltext, (960, 540))
    '''
    if fadeframe == 0:
        loadlvl(level)'''
    if fadeframe < 254 and not faderev:
        fadeframe += 2
    elif fadeframe == 254:
        faderev = True
        await loadlvl(level)
    if fadeframe >= 2 and faderev:
        fadeframe -= 2
    elif fadeframe == 0 and faderev:
        faderev = False
        fadeframe = 0
        addfade = False
    await asyncio.sleep(0)
        
    

    
    

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((45, 45)).convert()
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.velx, self.vely = 0, 0
        self.pos = (50, 935)

    def move(self):
        jump = False
        self.rect.topleft = self.pos

        key = pygame.key.get_pressed()

        if key[pygame.K_a] and self.rect.bottomleft[0] > 0:
            self.velx -= 10
        if key[pygame.K_d] and self.rect.bottomright[0] < 1920:
            self.velx += 10

        #jumping
        if key[pygame.K_SPACE] or key[pygame.K_w]:
            jump = True

        if self.pos[1] < 935:
            coll = 0
            for plat in platgroup:
                if self.rect.colliderect(plat.rectb):
                    self.vely = 0
                    self.pos = (self.pos[0], plat.pos[1] + plat.yl)
                    coll = 0
                elif self.rect.colliderect(plat.rectt):
                    coll += 1
                    self.vely = 0
                    self.pos = (self.pos[0], plat.pos[1] - (plat.yl - 6))
            if coll == 0:
                jump = False
                self.vely += 1

        for plat in platgroup:
            if self.rect.colliderect(plat.rectt) and jump:
                self.vely = -23

            if self.rect.colliderect(plat.rectr):
                self.velx = 0
                #self.pos = (plat.pos[0] + 99, self.pos[1])
            if self.rect.colliderect(plat.rectl):
                self.velx = 0
                #self.pos = (plat.pos[0] - 44, self.pos[1])

            if self.rect.colliderect(plat.rectr) and self.rect.colliderect(plat.rectt):
                self.pos = (self.pos[0], plat.pos[1] - (plat.yl - 6))
            if self.rect.colliderect(plat.rectl) and self.rect.colliderect(plat.rectt):
                self.pos = (self.pos[0], plat.pos[1] - (plat.yl - 6))

            if self.rect.colliderect(plat.rectr) and key[pygame.K_d]:
                self.velx += 10
            if self.rect.colliderect(plat.rectl) and key[pygame.K_a]:
                self.velx -= 10


        if self.pos[1] >= 935 and jump:
            self.vely = -23
        elif self.pos[1] >= 935 and not jump:
            self.vely = 0
            self.pos = (self.pos[0], 935)


        self.pos = (self.pos[0] + self.velx, self.pos[1] + self.vely)
        #print(self.velx, self.vely)
        self.velx = 0

class Platform(pygame.sprite.Sprite):

    def __init__(self, pos, x=100, y=50):
        super().__init__()
        self.xl, self.yl = x, y
        self.vissurf = pygame.Surface((x, y)).convert()
        self.vissurf.fill((255, 255, 255))
        self.surft, self.surfb, self.surfr, self.surfl = pygame.Surface((x - 2, 2)).convert(), pygame.Surface((x - 2, 2)).convert(), pygame.Surface((2, y - 6)).convert(), pygame.Surface((2, y - 6)).convert()
        '''self.surft.fill((255, 0, 0))
        self.surfb.fill((255, 0, 0))
        self.surfr.fill((255, 0, 0))
        self.surfl.fill((255, 0, 0))'''
        self.rectt, self.rectb, self.rectr, self.rectl = self.surft.get_rect(), self.surfb.get_rect(), self.surfr.get_rect(), self.surfl.get_rect()
        self.pos = (pos[0], pos[1])
        self.rectt.topleft = (self.pos[0] + 2, self.pos[1])
        self.rectb.topleft = (self.pos[0] + 2, self.pos[1] + self.yl - 2)
        self.rectr.topleft = (self.pos[0] + self.xl - 2, self.pos[1] + 3) 
        self.rectl.topleft = (self.pos[0], self.pos[1] + 3)
        platgroup.add(self)

class Spawnbeacon(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((45, 980), pygame.SRCALPHA)
        self.surf.fill((230, 0, 0, 255))
        self.trans = 255

    def upd(self):
        self.trans -= 4.25
        if self.trans > 0:
            self.surf.fill((230, 0, 0, self.trans))
        else:
            self.trans = 0
            self.kill()
            del self


pygame.init()

player = Player()
spawn = Spawnbeacon()
platgroup = pygame.sprite.Group()

clock = pygame.time.Clock()
level = 0

#vars for functions
fadeframe = 0
faderev = False
addfade = False

#run before game start
start = True

async def main():
    global addfade, level, player, screen, platgroup, spawn, start
    if start:
        await loadlvl(level)
        start = False

    run = True
    while run:

        pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                raise SystemExit
            
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            raise SystemExit
        
        clock.tick(60)
        screen.fill(((152, 191, 239)))

        #next level check
        if player.pos[1] < 0:
            player.pos = (50, -100)
            addfade = True
            spawn = Spawnbeacon()
        if player.vely < 105 and addfade:
            spawn.upd()
            print(spawn.trans)
        if player.vely == 100:
            level += 1
        #ground
        ground = pygame.Surface((3000, 100))
        ground.fill((27, 209, 99))

        #sprite actions/functions
        player.move()

        #add to screen
        screen.blit(player.surf, player.pos)
        #platform
        for platform in platgroup:
            screen.blit(platform.vissurf, platform.pos)
            #screen.blit(platform.surft, (platform.pos[0] + 2, platform.pos[1]))
            
            #screen.blit(platform.surfb, (platform.pos[0] + 2, platform.pos[1] + platform.yl - 2))
            
            #screen.blit(platform.surfr, (platform.pos[0] + platform.xl - 2, platform.pos[1] + 3))
            
            #screen.blit(platform.surfl, (platform.pos[0], platform.pos[1] + 3))
        screen.blit(ground, (0, 980))
        if addfade:
            if spawn and spawn.trans > 0:
                screen.blit(spawn.surf, (player.pos[0], 0))
            await fade()

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())