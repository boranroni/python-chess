import pygame
none = 0
king = 1
pawn = 2
knight = 3
bishop = 4
rook = 5
queen = 6

white = 8
black = 16

pd = {
    1: "king",
    2: "pawn",
    3: "knight",
    4: "bishop",
    5: "rook",
    6: "queen"
}
p_dict = {
    "r": rook,
    "n": knight,
    "b": bishop,
    "q": queen,
    "k": king,
    "p": pawn
}
# TODO: load all images first then dict to


class Piece(pygame.sprite.Sprite):
    def __init__(self, num: int, x: int, y: int, color: bool, SIZE):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load((f"img\\{pd[num]}" + (".png" if color else "1.png"))), (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def reimport_image(self, new_size: int, name: str):
        self.image = pygame.transform.scale(
            pygame.image.load(f"img\\{name}.png"), (new_size, new_size))
