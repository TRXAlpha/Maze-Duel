import pygame
import sys
from maze import Maze
from player import Player
from game import Game
from clock import Clock

pygame.init()
pygame.font.init()

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 50)
        self.buttons = {
            "1v1 Local": (450, 300),
            "Multiplayer": (450, 400),
            "Exit the Game": (450, 500)
        }
        self.running = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        for text, pos in self.buttons.items():
            btn = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(btn, pos)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for text, pos in self.buttons.items():
                btn_rect = pygame.Rect(pos, self.font.size(text))
                if btn_rect.collidepoint(mouse_pos):
                    if text == "1v1 Local":
                        return "1v1 Local"
                    elif text == "Multiplayer":
                        return "Multiplayer"
                    elif text == "Exit the Game":
                        pygame.quit()
                        sys.exit()
        return None

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                action = self.handle_event(event)
                if action:
                    return action
            self.draw()

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.FPS = pygame.time.Clock()

    def instructions(self):
        instructions1 = self.font.render('Player 1: Use Arrow Keys to Move', True, self.message_color)
        instructions2 = self.font.render('Player 2: Use WASD Keys to Move', True, self.message_color)
        self.screen.blit(instructions1, (810, 300))
        self.screen.blit(instructions2, (810, 350))

    def _draw(self, maze, tile, players, game, clock):
        maze_area = pygame.Rect(0, 0, 800, 800)
        info_area = pygame.Rect(800, 0, 200, 800)
        
        # Draw maze
        self.screen.fill("gray", maze_area)
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]

        # Draw info area background
        self.screen.fill(pygame.Color("darkslategray"), info_area)

        # Add a goal point to reach
        game.add_goal_point(self.screen)

        # Draw every player movement
        for player in players:
            player.draw(self.screen)
            player.update(tile, maze.grid_cells, maze.thickness)

        # Instructions, clock, winning message
        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.screen.blit(game.message(), (810, 120))
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (825, 200))
        
        pygame.display.flip()

    def main(self, frame_size, tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        maze.generate_maze()
        game = Game(maze.grid_cells[-1], tile)
        player1 = Player(tile // 3, tile // 3)
        player2 = Player(tile // 3, tile // 3)
        player1.controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
        player2.controls = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}
        players = [player1, player2]
        clock = Clock()

        clock.start_timer()
        while self.running:
            self.screen.fill("gray")
            self.screen.fill(pygame.Color("darkslategray"), (803, 0, 197, 797))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for player in players:
                    if event.type == pygame.KEYDOWN:
                        if not self.game_over:
                            if event.key == player.controls['left']:
                                player.left_pressed = True
                            if event.key == player.controls['right']:
                                player.right_pressed = True
                            if event.key == player.controls['up']:
                                player.up_pressed = True
                            if event.key == player.controls['down']:
                                player.down_pressed = True
                            player.check_move(tile, maze.grid_cells, maze.thickness)
        
                    if event.type == pygame.KEYUP:
                        if not self.game_over:
                            if event.key == player.controls['left']:
                                player.left_pressed = False
                            if event.key == player.controls['right']:
                                player.right_pressed = False
                            if event.key == player.controls['up']:
                                player.up_pressed = False
                            if event.key == player.controls['down']:
                                player.down_pressed = False
                            player.check_move(tile, maze.grid_cells, maze.thickness)

            if game.is_game_over(players):
                self.game_over = True
                for player in players:
                    player.left_pressed = False
                    player.right_pressed = False
                    player.up_pressed = False
                    player.down_pressed = False

            self._draw(maze, tile, players, game, clock)
            self.FPS.tick(60)

if __name__ == "__main__":
    window_size = (800, 800)
    screen_size = (1000, 800)  # Wider screen to accommodate the information section
    tile_size = 30
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Maze")

    menu = MainMenu(screen)
    action = menu.main_loop()

    if action == "1v1 Local":
        game = Main(screen)
        game.main(window_size, tile_size)
    elif action == "Multiplayer":
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("impact", 50)
        text = font.render("To be continued", True, (255, 255, 255))
        screen.blit(text, (450, 300))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()
    elif action == "Exit the Game":
        pygame.quit()
        sys.exit()
``
