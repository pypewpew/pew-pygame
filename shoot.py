import pew


class Bullet:
    __slots__ = 'x', 'y', 'dx', 'dy', 'dead'
    colors = 3, 3

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dead = False
        self.dx = dx
        self.dy = dy

    def act(self, level):
        self.x += self.dx
        self.y += self.dy
        if level.tile(self.x, self.y).block:
            self.dead = True
        for mob in level.mobs:
            if mob.x == self.x and mob.y == self.y and mob is not self:
                self.dead = True
                mob.dead = True


class Monster:
    __slots__ = 'x', 'y', 'dead', 'step'
    colors = 2, 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dead = False
        self.step = 0

    def act(self, level):
        self.step = max(self.step - 1, 0)
        if self.step:
            return
        self.step = 4
        hero = level.mobs[0]
        if hero.x == self.x and hero.y == self.y:
            self.dead = True
        dx, dy = 0, 0
        if hero.x > self.x:
            dx = 1
        elif hero.x < self.x:
            dx = -1
        if hero.y > self.y:
            dy = 1
        elif hero.y < self.y:
            dy = -1

        def blocked(x, y):
            if level.tile(x, y).block:
                return True
            for mob in level.mobs:
                if mob.x == x and mob.y == y:
                    return True
            return False

        if not blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        elif not blocked(self.x, self.y + dy):
            self.y += dy
        elif not blocked(self.x + dx, self.y):
            self.x += dx


class Hero:
    __slots__ = 'x', 'y', 'dx', 'dy', 'dead', 'step', 'cooldown'
    colors = 1, 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dead = False
        self.cooldown = 0
        self.step = 0
        self.dx = 0
        self.dy = -1

    def act(self, level):
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
        if keys & pew.K_O and self.cooldown == 0:
            level.mobs.append(Bullet(self.x, self.y, self.dx, self.dy))
            self.cooldown += 1
        else:
            self.cooldown = max(self.cooldown - 1, 0)
        if kx == self.dx and ky == self.dy and self.step == 0:
            tile = level.tile(self.x + kx, self.y + ky)
            if not tile.block:
                self.x += kx
                self.y += ky
                self.step = 2
        else:
            self.step = max(self.step - 1, 0)
            if kx or ky:
                self.dx = kx
                self.dy = ky


class Tile:
    __slots__ = 'colors', 'block', 'spawn'

    def __init__(self, colors, block=False, spawn=None):
        self.colors = colors
        self.block = block
        self.spawn = spawn


class Level:
    __slots__ = 'ground', 'mobs'

    LEGEND = {'X': 0, '.': 1, '+': 2, '@': 3, 'M': 4}

    # color 1, color 2, block, spawn
    TILES = (
        Tile((2, 2), True),
        Tile((0, 0)),
        Tile((3, 3)),
        Tile((0, 0), False, Hero),
        Tile((0, 0), False, Monster),
    )

    def __init__(self, filename):
        self.ground = []
        with open(filename, 'r') as f:
            for line in f:
                self.ground.append(bytes(self.LEGEND[c] for c in line.strip()))
        self.mobs = []

    def tile(self, x, y):
        if not 0 <= y < len(self.ground):
            return self.TILES[0]
        row = self.ground[y]
        if not 0 <= x < len(row):
            return self.TILES[0]
        return self.TILES[row[x]]

    def spawn(self):
        for y, row in enumerate(self.ground):
            for x, col in enumerate(row):
                tile = self.tile(x, y)
                if tile.spawn:
                    level.mobs.append(tile.spawn(x, y))


class Display:
    __slots__ = 'x', 'y', 'screens'

    def __init__(self):
        self.screens = pew.Pix(), pew.Pix()
        self.x = 1
        self.y = 1

    def draw_level(self, level):
        for y in range(8):
            for x in range(8):
                tile = level.tile(x + self.x, y + self.y)
                self.screens[0].pixel(x, y, tile.colors[0])
                self.screens[1].pixel(x, y, tile.colors[1])

    def draw_mobs(self, level):
        for mob in level.mobs:
            self.screens[0].pixel(mob.x - self.x, mob.y - self.y,
                                  mob.colors[0])
            self.screens[1].pixel(mob.x - self.x, mob.y - self.y,
                                  mob.colors[1])

    def clear_mobs(self, level):
        for mob in level.mobs:
            tile = level.tile(mob.x, mob.y)
            self.screens[0].pixel(mob.x - self.x, mob.y - self.y,
                                  tile.colors[0])
            self.screens[1].pixel(mob.x - self.x, mob.y - self.y,
                                  tile.colors[1])

    def recenter(self, x, y):
        redraw = False
        if x > 4 + self.x:
            self.x += 1
            redraw = True
        elif x < 3 + self.x:
            self.x -= 1
            redraw = True
        if y > 4 + self.y:
            self.y += 1
            redraw = True
        elif y < 3 + self.y:
            self.y -= 1
            redraw = True
        if redraw:
            display.draw_level(level)


pew.init()
display = Display()
level = Level('level0.lvl')
display.draw_level(level)
level.spawn()
hero = level.mobs[0]

while True:
    for screen in display.screens:
        display.clear_mobs(level)
        for mob in level.mobs:
            mob.act(level)
        level.mobs = [mob for mob in level.mobs if not mob.dead]
        display.recenter(hero.x, hero.y)
        display.draw_mobs(level)
        pew.show(screen)
        pew.tick(1/12)

