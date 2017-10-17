import pew


class Mob:
    color = 3

    def __init__(self, x, y, dx=0, dy=0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.dead = False

    def act(self, mobs):
        self.x += self.dx
        self.y += self.dy

    def clear(self, screen):
        screen.pixel(self.x, self.y, 0)

    def draw(self, screen):
        screen.pixel(self.x, self.y, self.color)


class Bullet(Mob):
    color = 3

    def act(self, mobs):
        if not 0 <= self.x <= 8 or not 0 <= self.y <= 8:
            self.dead = True
        self.x += self.dx
        self.y += self.dy


class Hero(Mob):
    color = 2

    def act(self, mobs):
        keys = pew.keys()
        kx, ky = 0, 0
        if keys & pew.K_UP:
            ky = -1
        elif keys & pew.K_DOWN:
            ky = 1
        if keys & pew.K_LEFT:
            kx = -1
        elif keys & pew.K_RIGHT:
            kx = 1
        if keys & pew.K_O:
            mobs.append(Bullet(self.x, self.y, self.dx, self.dy))
        if kx == self.dx and ky == self.dy:
            self.x += kx
            self.y += ky
        elif kx or ky:
            self.dx = kx
            self.dy = ky


pew.init()
screen = pew.Pix()
hero = Hero(4, 4)
mobs = [hero]

while True:
    for mob in mobs:
        mob.clear(screen)
    for mob in mobs:
        mob.act(mobs)
    for mob in mobs:
        mob.draw(screen)
    mobs = [mob for mob in mobs if not mob.dead]
    pew.show(screen)
    pew.tick(1/6)

