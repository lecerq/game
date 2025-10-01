import pgzrun
import random

# Игровое окно
cell = Actor('border1')
cell1 = Actor('floor2')
cell2 = Actor("crack2")
cell3 = Actor("bones2")
size_w = 9 # Ширина поля в клетках
size_h = 10 # Высота поля в клетках
WIDTH = 800
HEIGHT = 500

# Важные переменные
win = 0
mode = "game"
colli = 0
coins = 0
price1 = 10
price2 = 10
level = 1

TITLE = "Game" # Заголовок окна игры
FPS = 60 # Количество кадров в секунду

# Карта
my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 1, 2, 1, 3, 1, 1, 0], 
          [0, 1, 1, 1, 2, 1, 1, 1, 0], 
          [0, 1, 3, 2, 1, 1, 3, 1, 0], 
          [0, 1, 1, 1, 1, 3, 1, 1, 0], 
          [0, 1, 1, 3, 1, 1, 2, 1, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]] 

# Главный герой
char = Actor('char')
char.top = cell.height
char.left = cell.width
char.health = 100
char.attack = 5

# Кнопки
butto = Actor('baton3',(630,100))
butto1 = Actor('baton3',(630,200))

# Генерация врагов
enemies = []

def new_enemy():
    global level
    for i in range(5):
        x = random.randint(1, 7) * cell.width
        y = random.randint(1, 7) * cell.height
        if level == 1:
            enemy = Actor("slime", topleft=(x, y))
        else:
            enemy = Actor("slime1", topleft=(x, y))
        enemy.health = random.randint(10, 20)
        enemy.attack = random.randint(5, 10)
        enemy.bonus = random.randint(0, 2)
        enemies.append(enemy)

new_enemy()

# Бонусы
hearts = []
swords = []   

# Отрисовка карты
def map_draw():
    if mode == 'game':
        for i in range(len(my_map)):
            for j in range(len(my_map[0])):
                if my_map[i][j] == 0:
                    cell.left = cell.width*j
                    cell.top = cell.height*i
                    cell.draw()
                elif my_map[i][j] == 1:
                    cell1.left = cell.width*j
                    cell1.top = cell.height*i
                    cell1.draw()
                elif my_map[i][j] == 2:
                    cell2.left = cell.width*j
                    cell2.top = cell.height*i
                    cell2.draw()  
                elif my_map[i][j] == 3:
                    cell3.left = cell.width*j
                    cell3.top = cell.height*i
                    cell3.draw()

# Отрисовка
def draw():
    global game, game1, price1, price2, coins, level
    if mode == 'game':
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        butto.draw()
        butto1.draw()

        screen.draw.text('Купить HP +20', center=(630,90), color='white', fontsize=20)
        screen.draw.text(str(price1), center=(630,110), color='white', fontsize=20)
        screen.draw.text('Купить AP +10', center=(630,190), color='white', fontsize=20)
        screen.draw.text(str(price2), center=(630,210), color='white', fontsize=20)
        screen.draw.text("HP:", center=(25, 475), color='white', fontsize=20)
        screen.draw.text(str(char.health), center=(75, 475), color='white', fontsize=20)
        screen.draw.text("AP:", center=(375, 475), color='white', fontsize=20)
        screen.draw.text(str(char.attack), center=(425, 475), color='white', fontsize=20)
        screen.draw.text("Coins:", center=(625, 475), color='white', fontsize=20)
        screen.draw.text(str(coins), center=(675, 475), color='white', fontsize=20)

        for enemy in enemies:
            enemy.draw()
            screen.draw.text("HP: " + str(enemy.health), center=(enemy.x, enemy.y - 37), color='white', fontsize=14)
            screen.draw.text("AP: " + str(enemy.attack), center=(enemy.x, enemy.y - 26), color='white', fontsize=14)

        for heart in hearts:
            heart.draw()
        for sword in swords:
            sword.draw()

    elif mode == "pause":
        screen.fill("#2f3542")
        screen.draw.text("Победа!", center=(350, 100), color='white', fontsize=42)
        screen.draw.text("Переход на уровень:", center=(350, 150), color='white', fontsize=24)
        screen.draw.text(str(level), center=(350, 180), color='white', fontsize=36)
        screen.draw.text("Нажми на пробел", center=(350, 220), color='black', fontsize=24)
    
    elif mode == "end":
        screen.fill("#2f3542")
        if win == 1:
            screen.draw.text("Победа!", center=(WIDTH/2, HEIGHT/2), color='white', fontsize=46)
        else:
            screen.draw.text("Поражение!", center=(WIDTH/2, HEIGHT/2), color='white', fontsize=46)

# Управление
def on_key_down(key):
    global colli, coins, level
    old_x = char.x
    old_y = char.y
    if keyboard.right and char.x + cell.width < WIDTH - cell.width:
        char.x += cell.width
        char.image = 'char'
    elif keyboard.left and char.x - cell.width > cell.width:
        char.x -= cell.width
        char.image = 'char_left1'
    elif keyboard.down and char.y + cell.height < HEIGHT - cell.height*2:
        char.y += cell.height
    elif keyboard.up and char.y - cell.height > cell.height:
        char.y -= cell.height
    
    # Столкновение с врагами
    enemy_index = char.collidelist(enemies)
    if enemy_index != -1:
        char.x = old_x
        char.y = old_y
        colli = 1
        enemy = enemies[enemy_index]
        enemy.health -= char.attack
        char.health -= enemy.attack
        if enemy.health <= 0:
            coins += 5
            if enemy.bonus == 1:
                heart = Actor('heart', pos=enemy.pos)
                hearts.append(heart)
            elif enemy.bonus == 2:
                sword = Actor('sword', pos=enemy.pos)
                swords.append(sword)
            enemies.pop(enemy_index)

# Нажатие на кнопки мышки
def on_mouse_down(button , pos):
    global price1, price2, coins
    if button == mouse.LEFT:
        if butto.collidepoint(pos):
            if coins >= price1:
                coins -= price1
                price1 += 10
                char.health += 20
        if butto1.collidepoint(pos):
            if coins >= price2:
                coins -= price2
                price2 += 10
                char.attack += 10

# Логика победы или поражения
def victory():
    global mode, win
    if enemies == [] and char.health > 0:
        mode = "pause"
        win = 1
    elif char.health <= 0:
        mode = "end"
        win = -1

# Логика бонусов и уровней
def update(dt):
    global mode, level
    victory()

    for i in range(len(hearts)):
        if char.colliderect(hearts[i]):
            char.health += 5
            hearts.pop(i)
            break
        
    for i in range(len(swords)):
        if char.colliderect(swords[i]):
            char.attack += 5
            swords.pop(i)
            break
    
    # Смена уровня    
    if mode == "pause" and keyboard.space:
        level += 1
        if level <= 2:
            new_enemy()
            mode = "game"
        else:
            mode = "end"

pgzrun.go()
