import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
FPS = 20

BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)


class GameObject:
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self, screen):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
            randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        )

    def draw(self, screen):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0]) % SCREEN_WIDTH,
            (head[1] + self.direction[1]) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                snake.next_direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                snake.next_direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                snake.next_direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                snake.next_direction = (GRID_SIZE, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()

    