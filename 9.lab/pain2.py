import pygame 
 
WIDTH, HEIGHT = 1200, 800  # Определяет ширину и высоту окна игры
FPS = 90  # Частота обновления экрана
draw = False  # Указывает, производится ли рисование на экране
radius = 2  # Радиус кисти
color = 'blue'  # Цвет кисти
mode = 'pen'  # Режим (по умолчанию — ручка)
 
pygame.init() 
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Создание окна заданных размеров
pygame.display.set_caption('Paint')  # Название окна
clock = pygame.time.Clock()  # Для управления временем
screen.fill(pygame.Color('white'))  # Заполняет экран белым цветом
font = pygame.font.SysFont('None', 60)  # Создание шрифта для отображения текста
 
def drawLine(screen, start, end, width, color): 
    # Извлечение координат начальной и конечной точек
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    
    # Вычисление абсолютной разницы координат
    dx = abs(x1 - x2) 
    dy = abs(y1 - y2) 
    
    # Коэффициенты уравнения прямой Ax + By + C = 0
    A = y2 - y1  # Вертикаль
    B = x1 - x2  # Горизонталь
    C = x2 * y1 - x1 * y2 
    
    # Если линия более горизонтальна
    if dx > dy: 
        if x1 > x2:  # Убедимся, что x1 левее x2
            x1, x2 = x2, x1 
            y1, y2 = y2, y1 
        for x in range(x1, x2): 
            y = (-C - A * x) / B 
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width) 
    # Если линия более вертикальна
    else: 
        if y1 > y2:  # Убедимся, что y1 выше y2
            x1, x2 = x2, x1 
            y1, y2 = y2, y1 
        for y in range(y1, y2): 
            x = (-C - B * y) / A 
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)

def drawCircle(screen, start, end, width, color): 
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    x = (x1 + x2) / 2  # Центр круга по X
    y = (y1 + y2) / 2  # Центр круга по Y
    radius = abs(x1 - x2) / 2  # Радиус круга
    pygame.draw.circle(screen, pygame.Color(color), (x, y), radius, width)  # Отрисовка круга

def drawRectangle(screen, start, end, width, color): 
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    widthr = abs(x1 - x2)  # Ширина прямоугольника
    height = abs(y1 - y2)  # Высота прямоугольника

    # Отрисовка прямоугольника в зависимости от направления
    if x2 > x1 and y2 > y1: 
        pygame.draw.rect(screen, pygame.Color(color), (x1, y1, widthr, height), width) 
    if y2 > y1 and x1 > x2: 
        pygame.draw.rect(screen, pygame.Color(color), (x2, y1, widthr, height), width) 
    if x1 > x2 and y1 > y2: 
        pygame.draw.rect(screen, pygame.Color(color), (x2, y2, widthr, height), width) 
    if x2 > x1 and y1 > y2: 
        pygame.draw.rect(screen, pygame.Color(color), (x1, y2, widthr, height), width)

def drawSquare(screen, start, end, color): 
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    mn = min(abs(x2 - x1), abs(y2 - y1))  # Сторона квадрата
 
    if x2 > x1 and y2 > y1: 
        pygame.draw.rect(screen, pygame.Color(color), (x1, y1, mn, mn)) 
    if y2 > y1 and x1 > x2: 
        pygame.draw.rect(screen, pygame.Color(color), (x2, y1, mn, mn)) 
    if x1 > x2 and y1 > y2: 
        pygame.draw.rect(screen, pygame.Color(color), (x2, y2, mn, mn)) 
    if x2 > x1 and y1 > y2: 
        pygame.draw.rect(screen, pygame.Color(color), (x1, y2, mn, mn)) 

def drawRightTriangle(screen, start, end, color): 
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    if x2 > x1 and y2 > y1: 
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x1, y2))) 
    if y2 > y1 and x1 > x2: 
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x1, y2))) 
    if x1 > x2 and y1 > y2: 
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x2, y1))) 
    if x2 > x1 and y1 > y2: 
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y2), (x2, y1))) 

def drawEquilateralTriangle(screen, start, end, width, color): 
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    width_b = abs(x2 - x1) 
    height = (3**0.5) * width_b / 2  # Высота равностороннего треугольника

    if y2 > y1: 
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y2), (x2, y2), ((x1 + x2) / 2, y2 - height)), width) 
    else: 
        pygame.draw.polygon(screen, pygame.Color(color), ((x1, y1), (x2, y1), ((x1 + x2) / 2, y1 - height))) 

def drawRhombus(screen, start, end, width, color): 
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    pygame.draw.lines(screen, pygame.Color(color), True, 
        (((x1 + x2) / 2, y1), (x1, (y1 + y2) / 2), ((x1 + x2) / 2, y2), (x2, (y1 + y2) / 2)), width) 

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            exit()  # Выход из программы при закрытии окна
         
        # Обработка событий клавиатуры
        if event.type == pygame.KEYDOWN: 
            # Изменение режима рисования по нажатию клавиши
            if event.key == pygame.K_r: 
                mode = 'rectangle'  # Режим прямоугольника
            if event.key == pygame.K_c: 
                mode = 'circle'  # Режим круга
            if event.key == pygame.K_p: 
                mode = 'pen'  # Режим пера
            if event.key == pygame.K_e: 
                mode = 'erase'  # Режим стирания
            if event.key == pygame.K_s: 
                mode = 'square'  # Режим квадрата
            if event.key == pygame.K_q: 
                screen.fill(pygame.Color('white'))  # Очистка экрана

            # Изменение цвета
            if event.key == pygame.K_1: 
                color = 'black' 
            if event.key == pygame.K_2: 
                color = 'green' 
            if event.key == pygame.K_3: 
                color = 'red' 
            if event.key == pygame.K_4: 
                color = 'blue' 
            if event.key == pygame.K_5: 
                color = 'yellow' 
            if event.key == pygame.K_t: 
                mode = 'right_tri'  # Режим прямоугольного треугольника
            if event.key == pygame.K_u: 
                mode = 'eq_tri'  # Режим равностороннего треугольника
            if event.key == pygame.K_h: 
                mode = 'rhombus'  # Режим ромба

        if event.type == pygame.MOUSEBUTTONDOWN:  
            draw = True  # Включить рисование
            if mode == 'pen': 
                pygame.draw.circle(screen, pygame.Color(color), event.pos, radius)  # Рисование точки
            prevPos = event.pos  # Сохраняем начальную точку

        if event.type == pygame.MOUSEBUTTONUP:  
            # Когда отпускается кнопка мыши
            if mode == 'rectangle': 
                drawRectangle(screen, prevPos, event.pos, radius, color) 
            elif mode == 'circle': 
                drawCircle(screen, prevPos, event.pos, radius, color) 
            elif mode == 'square': 
                drawSquare(screen, prevPos, event.pos, color) 
            elif mode == 'right_tri': 
                drawRightTriangle(screen, prevPos, event.pos, color) 
            elif mode == 'eq_tri': 
                drawEquilateralTriangle(screen, prevPos, event.pos, radius, color) 
            elif mode == 'rhombus': 
                drawRhombus(screen, prevPos, event.pos, radius, color) 
            draw = False  # Выключить рисование

        if event.type == pygame.MOUSEMOTION:  
            # При движении мыши
            if draw and mode == 'pen': 
                drawLine(screen, lastPos, event.pos, radius, color) 
            elif draw and mode == 'erase': 
                drawLine(screen, lastPos, event.pos, radius, 'white') 
            lastPos = event.pos  # Обновление предыдущей позиции

    # Отрисовка прямоугольника с информацией о радиусе
    pygame.draw.rect(screen, pygame.Color('white'), (5, 5, 115, 75)) 
    renderRadius = font.render(str(radius), True, pygame.Color(color)) 
    screen.blit(renderRadius, (5, 5)) 

    pygame.display.flip()  # Обновление дисплея
    clock.tick(FPS)  # Управление частотой кадров