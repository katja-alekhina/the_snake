from random import choice, randint
from exceptions import EndGameError
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
left_positions = [(x, y) for x in range(GRID_WIDTH)
                  for y in range(GRID_HEIGHT)]

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (255, 199, 226)

# Цвет границы ячейки
BORDER_COLOR = (255, 199, 226)

# Цвет яблока
APPLE_COLOR = (75, 0, 130)

# Цвет змейки
SNAKE_COLOR = (255, 0, 255)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются игровые объекты."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=None) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Базовый метод отрисовки объекта, переопределяющийся далее."""
        raise NotImplementedError('Определите  draw в'
                                  f'{self.__class__.__name__}')


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, taken_positions=[]) -> None:
        super().__init__(body_color=APPLE_COLOR,
                         position=self.randomize_position(taken_positions))

    def randomize_position(self, taken_positions):
        """Метод, рандомно определяющий позицию яблока."""
        random_position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                           randint(0, GRID_HEIGHT) * GRID_SIZE)
        if len(taken_positions) < GRID_HEIGHT * GRID_HEIGHT:
            while random_position in taken_positions:
                random_position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                                   randint(0, GRID_HEIGHT) * GRID_SIZE)
        else:
            raise EndGameError
        return random_position

    def draw(self):   # Это прекод, он мне изначально дан.
        """Метод, отрисовывающий яблоко на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и ее поведение."""

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):   # Это прекод, он мне дан.
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, определяющий движение змейки."""
        head_position = self.get_head_position()
        x, y = head_position
        # Не понимаю, как можно без них обойтись(
        x_direction, y_direction = self.direction
        x += GRID_SIZE * x_direction
        y += GRID_SIZE * y_direction
        x %= SCREEN_WIDTH
        y %= SCREEN_HEIGHT
        new_head_position = (x, y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод, отрисовывающий змейку."""
        for position in self.positions:   # Это прекод, он мне дан.
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Метод, возвращающий координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, заново отрисовывающий змейку."""
        self.direction = choice([LEFT, UP, RIGHT, DOWN])
        self.__init__()


def handle_keys(game_object):
    """Метод, обрабатывающий нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция для основного хода игры."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
