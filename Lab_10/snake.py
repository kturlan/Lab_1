import pygame, sys, random, time
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="snake",
    port="7050",
    user="postgres",
    password="Tkso0507."
)
cur = conn.cursor()

# Создание таблицы пользователей
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        score INTEGER NOT NULL,
        level INTEGER NOT NULL
    );
""")
conn.commit()

username = input("Enter your username: ")

def get_or_create_user(username):
    """Получение пользователя или создание нового"""
    cur.execute("SELECT id, score, level FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        print(f"Welcome back, {username}! Level: {user[2]}, Score: {user[1]}")
        return user[0], user[1], user[2]
    else:
        cur.execute("INSERT INTO users (username, score, level) VALUES (%s, %s, %s) RETURNING id",
                    (username, 0, 0))
        conn.commit()
        print(f"New user created: {username}")
        return cur.fetchone()[0], 0, 0

LEVEL, SCORE = 0, 0
user_id, SCORE, LEVEL = get_or_create_user(username)

pygame.init()
BLUE = (0, 0, 200)
GRAY = (169, 169, 169)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)
GREEN = (0, 200, 0)
WIDTH, HEIGHT, CELL = 600, 600, 30
FPS = 60
INITIAL_SNAKE_SPEED = 0.2  # Начальная скорость змейки
SPEED_INCREMENT = 0.03  # Уменьшение интервала (увеличение скорости) с каждым уровнем

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

class Point:
    def __init__(self, x, y): self.x, self.y = x, y
    def __eq__(self, other): return self.x == other.x and self.y == other.y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx, self.dy = 0, 0
        self.last_move_time = time.time()
        self.speed = INITIAL_SNAKE_SPEED  # Текущая скорость змейки

    def update_speed(self, level):
        """Обновляет скорость змейки на основе уровня"""
        self.speed = max(0.05, INITIAL_SNAKE_SPEED - level * SPEED_INCREMENT)

    def move(self):
        current_time = time.time()
        if current_time - self.last_move_time >= self.speed and (self.dx != 0 or self.dy != 0):
            new_head = Point(self.body[0].x + self.dx, self.body[0].y + self.dy)
            # Проверка столкновений: со змейкой, стенами и границами
            if new_head in self.body or not (0 <= new_head.x < WIDTH // CELL and 0 <= new_head.y < HEIGHT // CELL) or new_head in wall.body:
                pygame.quit()
                sys.exit()
            self.body.insert(0, new_head)
            if new_head == food.pos:
                global SCORE
                SCORE += food.weight
                food.spawn(self.body + wall.body)
            else:
                self.body.pop()
            self.last_move_time = current_time

    def draw(self):
        for segment in self.body[0:]:
            pygame.draw.rect(screen, BLUE, (segment.x * CELL, segment.y * CELL, CELL, CELL))

class Food:
    def __init__(self):
        self.pos = Point(0, 0)
        self.weight = 1
        self.timer = 0
        self.spawn([])

    def spawn(self, forbidden):
        """Генерация еды, не попадая на тело змейки или стены"""
        while True:
            self.pos = Point(random.randint(0, WIDTH // CELL - 1), random.randint(0, HEIGHT // CELL - 1))
            if self.pos not in forbidden:
                break
        self.weight = random.choice([1, 2, 3])
        self.timer = 500

    def draw(self):
        pygame.draw.rect(screen, RED, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

class Wall:
    def __init__(self, level):
        self.body = []
        self.load_level(level)

    def load_level(self, level):
        """Загрузка стен по текущему уровню"""
        self.body.clear()
        if level == 1:
            self.body = [Point(x, 10) for x in range(5, 15)]
        elif level == 2:
            self.body = [Point(7, y) for y in range(5, 15)] + [Point(12, y) for y in range(5, 15)]
        elif level == 3:
            self.body = [Point(x, x) for x in range(5, 15)] + [Point(x, 20 - x) for x in range(5, 15)]

    def draw(self):
        for block in self.body:
            pygame.draw.rect(screen, YELLOW, (block.x * CELL, block.y * CELL, CELL, CELL))

def draw_grid():
    """Отрисовка игрового поля"""
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(screen, GREEN, (i * CELL, j * CELL, CELL, CELL))

snake, food = Snake(), Food()
wall = Wall(LEVEL)  # Инициализация стены
running = True
game_started = False

while running:
    screen.fill(GRAY)
    draw_grid()
    wall.draw()

    old_level = LEVEL
    LEVEL = min(SCORE // 10, 3)  # Максимум уровень 3
    if LEVEL > old_level:
        snake.update_speed(LEVEL)
        wall.load_level(LEVEL)  # Загрузка новой стены при повышении уровня

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if not game_started:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    snake.dx, snake.dy = 1, 0
            else:
                if event.key == pygame.K_RIGHT and snake.dx == 0:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx == 0:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_DOWN and snake.dy == 0:
                    snake.dx, snake.dy = 0, 1
                elif event.key == pygame.K_UP and snake.dy == 0:
                    snake.dx, snake.dy = 0, -1
                elif event.key == pygame.K_p:
                    # Сохранение текущего счета и уровня при паузе
                    cur.execute(
                        "UPDATE users SET score = %s, level = %s WHERE username = %s",
                        (SCORE, LEVEL, username)
                    )
                    conn.commit()
                    print(f"Game paused. Score and level saved for {username}.")
                    running = False

    if game_started:
        food.timer -= 1
        if food.timer <= 0:
            food.spawn(snake.body + wall.body)
        snake.move()

    snake.draw()
    food.draw()
    screen.blit(font.render(f"Score: {SCORE}", True, RED), (10, 10))
    screen.blit(font.render(f"Level: {LEVEL}", True, RED), (500, 10))

    if not game_started:
        text = font.render("Press SPACE to Start", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()