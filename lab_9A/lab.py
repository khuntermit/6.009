# -*- coding: utf-8 -*-
## 6.009 -- Spring 2017 -- Lab 9
#  Time spent on the lab: 15 hours
#    Week 1: …
#    Week 2: …

class Textures:
    """A collection of object textures.

    Each constant in this class describes one texture, and
    single-letter texture names are also used in level maps.
    For example, the letter "e" in a game level map indicates
    that there is a bee at that position in the game.

    To add support for a new blob type, or to add a new texture
    for an existing blob, you'll probably want to update this
    list and the TEXTURE_MAP list in ``Constants``.
    """
    Bee = "e"
    Boat = "b"
    Building = "B"
    Castle = "C"
    Cloud = "c"
    Fire = "f"
    Fireball = "F"
    Floor = "="
    Helicopter = "h"
    Mushroom = "m"
    Player = "p"
    PlayerBored = "bored"
    PlayerFlying = "h"
    PlayerLost = "defeat"
    PlayerWon = "victory"
    Rain = "r"
    Storm = "s"
    Sun = "o"
    Tree = "t"
    Water = "w"

class Constants:
    """A collection of game-world constants.

    You can experiment with tweaking these constants, but
    remember to revert the changes when running the test suite!
    """
    TILE_SIZE = 128
    GRAVITY = -9
    MAX_DOWNWARDS_SPEED = 48

    PLAYER_DRAG = 6
    PLAYER_MAX_HORIZONTAL_SPEED = 48
    PLAYER_HORIZONTAL_ACCELERATION = 16
    PLAYER_JUMP_SPEED = 62
    PLAYER_JUMP_DURATION = 3
    PLAYER_BORED_THRESHOLD = 60

    STORM_LIGHTNING_ROUNDS = 5
    STORM_RAIN_ROUNDS = 10

    BEE_SPEED = 40
    MUSHROOM_SPEED = 16
    FIREBALL_SPEED = 60

    SUN_POWER = 5

    TEXTURE_MAP = {Textures.Bee: '1f41d',          # 🐝
                   Textures.Boat: '26f5',          # ⛵
                   Textures.Building: '1f3e2',     # 🏢
                   Textures.Castle: '1f3f0',       # 🏰
                   Textures.Cloud: '2601',         # ☁
                   Textures.Fire: '1f525',         # 🔥
                   Textures.Fireball: '1f525',     # 🔥
                   Textures.Floor: '2b1b',         # ⬛
                   Textures.Helicopter: '1f681',   # 🚁
                   Textures.Mushroom: '1f344',     # 🍄
                   Textures.Player: '1f60a',       # 😊
                   Textures.PlayerBored: '1f634',  # 😴
                   Textures.PlayerFlying: '1f681', # 🚁
                   Textures.PlayerLost: '1f61e',   # 😞
                   Textures.PlayerWon: '1f60e',    # 😎
                   Textures.Rain: '1f327',         # 🌧
                   Textures.Storm: '26c8',         # ⛈
                   Textures.Sun: '2600',           # ☀
                   Textures.Tree: '1f333',         # 🌳
                   Textures.Water: '1f30a'}        # 🌊


class HardBlob:
    """Contains behaviors for Hard Blob objects"""
    def __init__(self, identifier, pos, texture):
        self.x = pos[0]
        self.y = pos[1]
        self.identifier = identifier
        self.texture = texture
        self.player = False
        self.rect = Rectangle(self.x, self.y, Constants.TILE_SIZE, Constants.TILE_SIZE)

    def timestep(self, keys):
        pass

    def get_render_info(self):
        return {
                "identifier": self.identifier,
                "texture": self.texture,
                "pos": (self.x, self.y),
                "player": self.player
                }


class Castle(HardBlob):
    """Contains behavior for Castle objects"""
    def __init__(self, identifier, pos, texture):
        super().__init__(identifier, pos, texture)


class SoftBlob(HardBlob):
    """Contains behavior for Soft Blob objects.
    - Have speed
    - Can be affected by gravity
    """
    def __init__(self, identifier, pos, texture):
        super().__init__(identifier, pos, texture)
        self.y_speed = 0
        self.x_speed = 0

    def gravity(self):
        if self.y_speed > -Constants.MAX_DOWNWARDS_SPEED:
            self.y_speed += Constants.GRAVITY
            if self.y_speed < -Constants.MAX_DOWNWARDS_SPEED:
                self.y_speed = -Constants.MAX_DOWNWARDS_SPEED

    def timestep(self, keys):
        """
        SoftBlob-specific timestep function
        Handles:
        - Gravity
        """
        # gravity
        self.gravity()

        # move
        self.move(self.x_speed, self.y_speed)

    def move(self, x, y):
        self.x += x
        self.y += y

        self.rect.x = self.x
        self.rect.y = self.y

    def y_collide(self, v, h):
        if (self.y_speed > 0 and v[1] < 0) or (self.y_speed < 0 and v[1] > 0):
            self.y_speed = 0

    def x_collide(self, v, h):
        if (self.x_speed > 0 and v[0] < 0) or (self.x_speed < 0 and v[0] > 0):
            self.x_speed = 0

class Player(SoftBlob):
    def __init__(self, identifier, pos, texture):
        super().__init__(identifier, pos, texture)
        self.boredom = 0
        self.player = True

    def isbored(self, keys):
        """
        If frames passed without keys exceeds the Player's bored threshold, changes texture of character.
        """
        # no keys passed
        if len(keys) == 0:
            self.boredom += 1
        # keys passed - boredom resets
        else:
            self.boredom = 0
        # changes texture to bored
        if self.boredom > Constants.PLAYER_BORED_THRESHOLD:
            self.texture = Constants.TEXTURE_MAP[Textures.PlayerBored]
        # changes texture back to active
        else:
            self.texture = Constants.TEXTURE_MAP[Textures.Player]

    def is_defeated(self):
        """
        Returns True and changes texture to defeated texture if player is defeated
        Otherwise if not defeated, returns False
        """
        if self.y < -Constants.TILE_SIZE:
            self.texture = Constants.TEXTURE_MAP[Textures.PlayerLost]
            return True
        return False

    def x_collide(self, v, h):
        super().x_collide(v, h)

    def y_collide(self, v, h):
        super().y_collide(v, h)

    def timestep(self, keys):
        """
        Player-specific timestep function
        Handles:
        - Boredom
        - Gravity
        - Keys
        - Drag
        """
        # boredom
        self.isbored(keys)

        # gravity
        self.gravity()

        # keys
        if "left" in keys:
            self.x_speed -= Constants.PLAYER_HORIZONTAL_ACCELERATION

        if "right" in keys:
            self.x_speed += Constants.PLAYER_HORIZONTAL_ACCELERATION

        if "up" in keys:
            self.y_speed = Constants.PLAYER_JUMP_SPEED

        # drag
        if self.x_speed > 0:
            # speed is less than drag
            if self.x_speed < Constants.PLAYER_DRAG:
                self.x_speed = 0
            # speed is greater than or equal to drag
            else:
                self.x_speed -= Constants.PLAYER_DRAG
            # caps speed
            if self.x_speed > Constants.PLAYER_MAX_HORIZONTAL_SPEED:
                self.x_speed = Constants.PLAYER_MAX_HORIZONTAL_SPEED

        elif self.x_speed < 0:
            # speed is greater than drag
            if self.x_speed > -Constants.PLAYER_DRAG:
                self.x_speed = 0
            # speed is less than or equal to drag
            else:
                self.x_speed += Constants.PLAYER_DRAG
            # caps speed
            if self.x_speed < -Constants.PLAYER_MAX_HORIZONTAL_SPEED:
                self.x_speed = -Constants.PLAYER_MAX_HORIZONTAL_SPEED

        self.move(self.x_speed, self.y_speed)


class Rectangle:
    """A rectangle object to help with collision detection and resolution."""

    def __init__(self, x, y, w, h):
        """Initialize a new rectangle.

        `x` and `y` are the coordinates of the bottom-left corner. `w`
        and `h` are the dimensions of the rectangle.
        """
        self.x, self.y = x, y
        self.w, self.h = w, h

    def intersects(self, other):
        """Check whether `self` and `other` overlap.

        Rectangles are open on the top and right sides, and closed on
        the bottom and left sides; concretely, this means that the
        rectangle [0, 0, 1, 1] does not intersect either of [0, 1, 1, 1]
        or [1, 0, 1, 1].
        """
        # rectangles intersect when both x and y ranges somewhat overlap

        # checks if x's lie outside of r1 x-range
        outside_x = (self.x >= (other.x + other.w)) or ((self.x + self.w) <= other.x)
        # checks if y's lie outside of r1 y-range
        outside_y = (self.y >= (other.y + other.h)) or ((self.y + self.h) <= other.y)
        # returns true if both are not outside of r1
        return not outside_x and not outside_y

    @staticmethod
    def translationvector(r1, r2):
        """Compute how much `r2` needs to move to stop intersecting `r1`.

        If `r2` does not intersect `r1`, return ``None``.  Otherwise,
        return a minimal pair ``(x, y)`` such that translating `r2` by
        ``(x, y)`` would suppress the overlap. ``(x, y)`` is minimal in
        the sense of the "L1" distance; in other words, the sum of
        ``abs(x)`` and ``abs(y)`` should be as small as possible.

        When two pairs ``(x, y)`` and ``(y, x)`` are tied, return the
        one with the smallest element first.
        """

        if r1.intersects(r2):

            # calculates how far we need to move in all directions to exit r1
            left = (r1.x - r2.x) - r2.w
            right = (r1.x - r2.x) + r1.w
            down = -(r2.y - r1.y) - r2.h
            up = -(r2.y - r1.y) + r1.h

            # chooses between left and right
            if abs(left) > abs(right):
                x = right
            else:
                x = left

            # chooses between up and down
            if abs(down) > abs(up):
                y = up
            else:
                y = down

            # compares x and y movement
            if abs(y) <= abs(x):
                return 0, y
            else:
                return x, 0

        else:

            # does not intersect
            return None


class Game:
    def __init__(self, levelmap):
        """Initialize a new game, populated with objects from `levelmap`.

        `levelmap` is a 2D array of 1-character strings; all possible
        strings (and some others) are listed in the ``Textures`` class.
        Each character in `levelmap` corresponds to a blob of size
        ``TILE_SIZE * TILE_SIZE``.

        This function is free to store `levelmap`'s data however it
        wants.  For example, it may choose to just keep a copy of
        `levelmap`; or it could choose to read through `levelmap` and
        extract the position of each blob listed in `levelmap`.

        Any choice is acceptable, as long as it plays well with the
        implementation of ``timestep`` and ``render`` below.
        """

        def create(blob, blob_identifier, pos):
            """
            Creates blob object depending on the symbol in levelmap
            """
            textures = Constants.TEXTURE_MAP

            if blob == '=':
                texture = textures[Textures.Floor]
                return HardBlob(blob_identifier, pos, texture)

            if blob == 'c':
                texture = textures[Textures.Cloud]
                return HardBlob(blob_identifier, pos, texture)

            if blob == 'C':
                texture = textures[Textures.Castle]
                return Castle(blob_identifier, pos, texture)

            if blob == 't':
                texture = textures[Textures.Tree]
                return HardBlob(blob_identifier, pos, texture)

            if blob == 'B':
                texture = textures[Textures.Building]
                return HardBlob(blob_identifier, pos, texture)

            if blob == 'p':
                texture = textures[Textures.Player]
                return Player(blob_identifier, pos, texture)

        soft_blobs = []
        hard_blobs = []
        col = -1
        blob_identifier = 1

        # starts at the bottom of the 2D array
        for c in reversed(range(len(levelmap))):
            col += 1

            # works through the rows left to right
            for row in range(len(levelmap[c])):

                # FOR LATER: if char in blob_types:

                blob = levelmap[c][row]
                pos = (row * Constants.TILE_SIZE, col * Constants.TILE_SIZE)

                if blob == 'p' or blob == "=" or blob == 'c' or blob == 't' or blob == 'B' or blob == 'C':
                    item = create(blob, blob_identifier, pos)

                    # sorts items into categories within Game class
                    if isinstance(item, Player):
                        self.player = item
                    elif isinstance(item, SoftBlob):
                        soft_blobs.append(item)
                    elif isinstance(item, HardBlob) or isinstance(item, Castle):
                        hard_blobs.append(item)

                blob_identifier += 1

        self.soft_blobs = soft_blobs
        self.hard_blobs = hard_blobs
        self.status = 'ongoing'

    def timestep(self, keys):
        """Simulate the evolution of the game state over one time step.
        `keys` is a list of currently pressed keys."""
        # player timestep
        self.player.timestep(keys)

        # checks player defeat
        if self.player.is_defeated():
            self.status = "defeat"

        soft = self.soft_blobs + [self.player]

        # y translation for all soft blobs
        for s in soft:
            for h in self.hard_blobs:
                if s.rect.intersects(h.rect):

                    # do not add to player collide -
                    if isinstance(s, Player) and isinstance(h, Castle):
                        self.status = "victory"
                        self.player.texture = Constants.TEXTURE_MAP[Textures.PlayerWon]

                    v = Rectangle.translationvector(h.rect, s.rect)

                    s.y_collide(v, h)

                    s.move(0, v[1])

        # x translation for soft blobs
        for s in soft:
            for h in self.hard_blobs:
                if s.rect.intersects(h.rect):
                    v = Rectangle.translationvector(h.rect, s.rect)

                    s.x_collide(v, h)

                    s.move(v[0], 0)

    def render(self, w, h):
        """Report status and list of blob dictionaries for blobs
        with a horizontal distance of w//2 from player.  See writeup
        for details."""
        visible_blobs = []
        blobs = [self.player] + self.soft_blobs + self.hard_blobs
        px = self.player.x
        frame = Rectangle(px - w // 2, 0, w, h)

        for b in blobs:
            if frame.intersects(b.rect):
                visible_blobs.append(b.get_render_info())

        return self.status, visible_blobs
