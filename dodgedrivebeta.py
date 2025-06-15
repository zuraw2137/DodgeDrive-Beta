import pgzrun
import random
import time

WIDTH = 600
HEIGHT = 480
TITLE = "DodgeDrive"

FPS = 30
mode = 'menu'
obstacles = []
background = Actor('backgroundgrass')
background_universal = Actor('background')
car = Actor('defult', (300,400))
defult = Actor('defult', (125,240))
pickup = Actor('pickup', (250,240))
sedan = Actor('sedan', (375,240))
sport_car = Actor('sportcar', (500,240))
button_white = Actor('whitebutton', (300,240))
button_green = Actor('greenbutton', (300,160))
button_red = Actor('redbutton', (300,320))
score = 0
car_list = []
boost_active = False
last_boost_time = 10
boost_status = '...'

def reset_obstacles():
    global obstacles
    obstacles = []
    for i in range(3):
        x = random.randint(0, 600)
        y = random.randint(50, 200)
        obstacle = Actor('obstacle', (x, y))
        obstacle.speed = 2
        obstacles.append(obstacle)

def draw():
    global mode
    global boost_status
    global boost_active
    global last_boost_time
    if mode == 'game':
        background.draw()
        car.draw()
        screen.draw.text(f'{score}', center = (50,50), color = 'black', fontsize = 36)
        if time.time() - last_boost_time < 10:
            screen.draw.text(f'{boost_status}', center = (50,75), color = 'black', fontsize = 36)
        elif time.time() - last_boost_time >= 10:
            screen.draw.text(f'{boost_status}', center = (50,75), color = 'black', fontsize = 36)
        elif boost_active == 'True':
            screen.draw.text(f'{boost_status}', center = (50,75), color = 'black', fontsize = 36)
        for i in range(len(obstacles)):
            obstacles[i].draw()
    elif mode == 'menu':
        background_universal.draw()
        button_green.draw()
        screen.draw.text('PLAY', center = (300,160), color = 'black', fontsize = 36)
        button_white.draw()
        screen.draw.text('SKINS', center = (300,240), color = 'black', fontsize = 36)
        button_red.draw()
        screen.draw.text('EXIT', center = (300,320), color = 'black', fontsize = 36)
        screen.draw.text(f'{score}', center = (50,50), color = 'white', fontsize = 36)
    elif mode == 'skins':
        background_universal.draw()
        defult.draw()
        pickup.draw()
        sedan.draw()
        sport_car.draw()
        screen.draw.text('press any car to buy and set it as default', center = (300, 100), color = 'white', fontsize = 36)
        screen.draw.text('press SPACE to exit to the menu', center = (300, 370), color = 'white', fontsize = 36)
        screen.draw.text('0', center = (125,340), color = 'white', fontsize = 36)
        screen.draw.text('50', center = (250,340), color = 'white', fontsize = 36)
        screen.draw.text('100', center = (375,340), color = 'white', fontsize = 36)
        screen.draw.text('150', center = (500,340), color = 'white', fontsize = 36)
        screen.draw.text(f'{score}', center = (50,50), color = 'white', fontsize = 36)
    elif mode == 'end':
        background_universal.draw()
        screen.draw.text('GAME OVER', center = (300,240), color = 'red', fontsize = 36)
        screen.draw.text('press SPACE to exit to the menu', center = (300,300), color = 'white', fontsize = 36)
        screen.draw.text('Your score is:' f'{score}', center = (300, 200), color = 'white', fontsize = 36)

def new_obstacle():
    x = random.randint(81, 512)
    y = 25
    obstacle = Actor('obstacle', (x, y))
    obstacle.speed = 2
    obstacles.append(obstacle)

def obstacle_ship():
    for i in range(len(obstacles)):
        if obstacles[i].y < 440:
            obstacles[i].y = obstacles[i].y + obstacles[i].speed
        else:
            obstacles.pop(i)
            new_obstacle()

def collision():
    global mode
    global boost_active
    if boost_active == False:
        for i in range(len(obstacles)):
            if car.colliderect(obstacles[i]):
                mode = 'end'

def on_mouse_down(button, pos):
    global mode
    global score
    if button == mouse.LEFT and mode == 'menu':
        if button_green.collidepoint(pos):
            reset_obstacles()
            mode = 'game'
        if button_white.collidepoint(pos):
            mode = 'skins'
        if button_red.collidepoint(pos):
            exit()
    elif button == mouse.LEFT and mode == 'skins':
        if defult.collidepoint(pos):
            car.image = 'defult'
        if pickup.collidepoint(pos):
            if 'pickup' not in car_list and score >= 50:
                score -= 50
                car.image = 'pickup'
                car_list.append('pickup')
            if 'pickup' in car_list:
                car.image = 'pickup'
        if sedan.collidepoint(pos):
            if 'sedan' not in car_list and score >= 100:
                score -= 100
                car.image = 'sedan'
                car_list.append('sedan')
            if 'sedan' in car_list:
                car.image = 'sedan'
        if sport_car.collidepoint(pos):
            if 'sportcar' not in car_list and score >= 150:
                score -= 150
                car.image = 'sportcar'
                car_list.append('sportcar')
            if 'sportcar' in car_list:
                car.image = 'sportcar'
def add_score():
    global score
    if mode == 'game':
        score += 1

clock.schedule_interval(add_score, 1)

def boost_on():
    global boost_active
    global last_boost_time
    if time.time() - last_boost_time >= 10:
        boost_active = True
        boost_status = 'Boost activated'
        last_boost_time = time.time()
        clock.schedule_unique(boost_off, 3.0)

def boost_off():
    global boost_active
    boost_status = 'Boost unready'
    boost_active = False

def update(dt):
    global mode
    global score
    global last_boost_time
    def controls():
        if keyboard.right and car.x < 512:
            car.x += 2
        if keyboard.left and car.x > 81:
            car.x -= 2
        if keyboard.up and car.y > 50:
            car.y -= 2
        if keyboard.down and car.y < 440:
            car.y += 2
        if keyboard.e:
            boost_on()
    if keyboard.space and mode == 'game':
        mode = 'menu'
    if mode == 'game':
        controls()
        obstacles = []
        obstacle_ship()
        collision()
    elif mode == 'skins' and keyboard.space:
        mode = 'menu'
    elif mode == 'end' and keyboard.space:
        score = 0
        reset_obstacles()
        car.x = 300
        car.y = 400
        car_list.clear()
        car.image = 'defult'
        boost_active = False
        last_boost_time = 10
        mode = 'menu'

pgzrun.go()
