import PixelPerfect

class CollisionManager:

    def __init__(self,game):

        self.game = game

    def check(self):

        self.game.check_collisions()

    def check_powerups(self):

        collisions = PixelPerfect.spritecollide_pp(
            self.game.player,
            self.game.powerup_sprites,
            0
        )

        for powerup in collisions:

            if not powerup.fading:

                if not self.game.player.dying:

                    self.game.health.add()
                    powerup.pickup()

    def check_mines(self):

        collisions = PixelPerfect.spritecollide_pp(
            self.game.player,
            self.game.mine_sprites,
            0
        )

        for mine in collisions:

            if not mine.exploding:

                if not self.game.player.dying:

                    self.game.damage_player()
                    mine.explode()

    def check_sharks(self):

        collisions = PixelPerfect.spritecollide_pp(
            self.game.player,
            self.game.shark_sprites,
            0
        )

        for shark in collisions:

            if not shark.dying:

                if not self.game.player.dying:

                    self.game.damage_player()
                    shark.die()