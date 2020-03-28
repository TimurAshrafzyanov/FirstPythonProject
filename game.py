from tkinter import Tk, Label, Radiobutton, IntVar, Button
import pygame
import os
import random


# COLORS
LIGHT_BLUE = (0, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 100, 180)
ORANGE = (255, 100, 10)

# PARAMETERS
WIDTH = 800
HEIGHT = 600
FPS = 60

# GLOBAL VARIABLES
Player_cord = (WIDTH / 2, HEIGHT - 100)
jumping_range = 44


def Game_making():
    class Ghost(pygame.sprite.Sprite):
        count_of_jumps = 0
        player_right_img = ''
        player_left_img = ''

        def __init__(self, player_right_img, player_left_img):
            self.player_right_img = player_right_img
            self.player_left_img = player_left_img

            pygame.sprite.Sprite.__init__(self)
            self.image = player_right_img
            self.image.set_colorkey(BLACK)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = Player_cord

        def update(self):
            if self.rect.left > WIDTH:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = WIDTH
            if self.count_of_jumps != 0:
                self.jump()
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.go_right()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.go_left()

        def jump(self):
            if self.count_of_jumps == 0:
                self.count_of_jumps = jumping_range
            if self.count_of_jumps > (jumping_range + 1) / 2:
                self.move(3)
                self.count_of_jumps -= 1
            if (jumping_range + 1) / 2 >= self.count_of_jumps > 0:
                self.move(2)
                self.count_of_jumps -= 1

        def move(self, direction):
            if direction == 0:
                self.rect.x += 5
                self.image = self.player_right_img
                self.image.set_colorkey(BLACK)
                self.mask = pygame.mask.from_surface(self.image)
            if direction == 1:
                self.rect.x -= 5
                self.image = self.player_left_img
                self.image.set_colorkey(BLACK)
                self.mask = pygame.mask.from_surface(self.image)
            if direction == 2:
                self.rect.y += 6
            if direction == 3:
                self.rect.y -= 6

        def go_right(self):
            self.move(0)

        def go_left(self):
            self.move(1)

    class Pumpkin(pygame.sprite.Sprite):
        pumpkin_img = ''
        falling_speed = 5

        def __init__(self, pumpkin_img):
            self.pumpkin_img = pumpkin_img

            pygame.sprite.Sprite.__init__(self)
            self.image = pumpkin_img
            self.image.set_colorkey(BLACK)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(1, WIDTH), 30)

        def update(self):
            global HEIGHT
            if self.rect.bottom < HEIGHT - 5:
                self.rect.y += Pumpkin.falling_speed
            else:
                self.kill()

    def Start_game(selected):
        # PUTTING SETTINGS TO CREATE WINDOW IN THE CENTRE OF THE SCREEN
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # VARIABLES
        level_mode = 0
        COUNT_OF_LIVES = 3
        CURRENT_SCORE = 0

        def make_harder():
            nonlocal level_mode
            nonlocal MODE_ID
            if level_mode in (0, 2):
                MODE_ID += 1
                level_mode += 1
            elif level_mode in (1, 3):
                Pumpkin.falling_speed += 1
                level_mode += 1
            elif level_mode in (4, 5, 7, 8):
                level_mode += 1
            elif level_mode == 6:
                MODE_ID += 1
                Pumpkin.falling_speed -= 1
                level_mode += 1
            elif level_mode == 9:
                Pumpkin.falling_speed += 1
                level_mode += 1

        # GAME INITIALIZING
        pygame.init()
        starting_time = pygame.time.get_ticks()

        # EVENTS
        EASY_MODE = pygame.USEREVENT
        MEDIUM_MODE = pygame.USEREVENT + 1
        HARD_MODE = pygame.USEREVENT + 2
        SUPER_HARD_MODE = pygame.USEREVENT + 3
        MODE_ID = EASY_MODE
        pygame.time.set_timer(EASY_MODE, 600)
        pygame.time.set_timer(MEDIUM_MODE, 500)
        pygame.time.set_timer(HARD_MODE, 400)
        pygame.time.set_timer(SUPER_HARD_MODE, 300)
        INSTANT_MODE = pygame.USEREVENT + 4
        pygame.time.set_timer(INSTANT_MODE, 1200)
        period = 20000
        MAKING_HARDER_TIME = pygame.USEREVENT + 5
        pygame.time.set_timer(MAKING_HARDER_TIME, period)

        # SCREEN MAKING
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My game")
        clock = pygame.time.Clock()

        # IMAGE INSERTING
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        player_right_img = pygame.image.load(os.path.join(img_folder, 'ghost_r{}.png'.format(selected))).convert()
        player_left_img = pygame.image.load(os.path.join(img_folder, 'ghost_l{}.png'.format(selected))).convert()
        pumpkin_img = pygame.image.load(os.path.join(img_folder, 'pumpkin{}.png'.format(selected))).convert()
        background_img = pygame.image.load(os.path.join(img_folder, 'background{}.png'.format(selected))).convert()

        # SPRITES FORMING
        all_sprites = pygame.sprite.Group()
        player = Ghost(player_right_img, player_left_img)
        all_sprites.add(player)
        pumpkins = pygame.sprite.Group()
        pumpkins.add(Pumpkin(pumpkin_img))
        all_sprites.add(pumpkins)

        # GAME PROCESS
        running = True
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                    if event.key == pygame.K_SPACE:
                        player.jump()
                if event.type == INSTANT_MODE:
                    pumpkins.add(Pumpkin(pumpkin_img))
                    all_sprites.add(pumpkins)
                if event.type == MODE_ID:
                    pumpkins.add(Pumpkin(pumpkin_img))
                    all_sprites.add(pumpkins)
                if event.type == MAKING_HARDER_TIME:
                    make_harder()

            if pygame.sprite.spritecollide(player, pumpkins, True, pygame.sprite.collide_mask):
                COUNT_OF_LIVES -= 1

            all_sprites.update()
            screen.blit(background_img, (0, 0))
            all_sprites.draw(screen)

            # SCORE TABLE ADDING
            CURRENT_SCORE = (pygame.time.get_ticks() - starting_time) // 100
            first_font = pygame.font.Font(None, 50)
            score_table = first_font.render('Score : {}'.format(CURRENT_SCORE), 1, BLACK, ORANGE)
            screen.blit(score_table, (200, 30))

            # LIVES TABLE ADDING
            second_font = pygame.font.Font(None, 50)
            lives_table = second_font.render('Lives : {}'.format(COUNT_OF_LIVES), 1, BLACK, PINK)
            screen.blit(lives_table, (20, 30))

            pygame.display.flip()

            if COUNT_OF_LIVES == 0:
                running = False
        pygame.quit()
        return CURRENT_SCORE

    return Start_game


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def start_button_clicked():
    global selected_mode
    current_score = Game_making()(selected_mode)
    last_score_lbl.configure(text='Your last score : {}'.format(current_score))
    global max_score
    if current_score > max_score:
        max_score = current_score
        record_lbl.configure(text='Your record : {}'.format(max_score))
    global money
    money += current_score // 10


def choose_mod_button_clicked():
    def which_mode_selected():
        global selected_mode
        selected_mode = modes_array[var.get() - 1][1]

    global selected_mode
    global modes_array

    # MAKING CHOOSE MODE SCREEN
    choose_mod_window = Tk()
    choose_mod_window.title("Choose mode")
    choose_mod_window.geometry('{}x{}+0+0'.format(window_width, window_height))
    center(choose_mod_window)

    var = IntVar(choose_mod_window)
    i = 1
    for mode in modes_array:
        button = Radiobutton(choose_mod_window, font=(None, 20), text=mode[0], value=i, variable=var)
        button.config(command=which_mode_selected)
        button.pack()
        i += 1

    # ADD GO BACK BUTTON
    QuitButton('Go back', choose_mod_window)

    choose_mod_window.mainloop()


def add_bought_table(shop_window, x_cord, y_cord):
    bought_lbl = Label(shop_window, text='Bought', bg='green', font=(None, 15, 'bold'))
    bought_lbl.place(relx=x_cord, rely=y_cord, anchor='center')


def add_buy_button(shop_window, cost, x_cord, y_cord, name):
    def buy_button_clicked():
        nonlocal cost
        global money
        if money < cost:
            pass
        else:
            money -= cost
            new_btn.destroy()
            add_bought_table(shop_window, x_cord, y_cord + 0.15)
            global modes_array
            modes_array.append(name)
    new_btn = Button(shop_window, text='Buy', bg='pink', fg='black', height=3, width=15, command=buy_button_clicked)
    new_btn.place(relx=x_cord, rely=y_cord + 0.15, anchor='center')


def add_mode(shop_window, name, cost, x_cord, y_cord):
    new_lbl = Label(shop_window, text='{} \n Cost : {} coins'.format(name[0], cost), font=(None, 20))
    new_lbl.place(relx=x_cord, rely=y_cord, anchor='center')
    add_buy_button(shop_window, cost, x_cord, y_cord, name)


def add_bought_mode(shop_window, name, x_cord, y_cord):
    default_lbl = Label(shop_window, text='{} \n Cost : -'.format(name[0]), font=(None, 20))
    default_lbl.place(relx=x_cord, rely=y_cord, anchor='center')
    add_bought_table(shop_window, x_cord=x_cord, y_cord=y_cord + 0.15)


def shop_button_clicked():
    # CREATE SHOP WINDOW
    shop_window = Tk()
    shop_window.title("Shop")
    shop_window.geometry('{}x{}+0+0'.format(window_width, window_height))
    center(shop_window)
    global money
    money_lbl = Label(shop_window, text='You have {} coins'.format(money), font=(None, 20, 'bold'))
    money_lbl.place(relx=0.5, rely=0.1, anchor='center')

    # ADD ALL BUTTONS
    number = 0
    for mode in all_modes_array:
        if mode in modes_array:
            add_bought_mode(shop_window, name=mode, x_cord=cords[number][0], y_cord=cords[number][1])
        else:
            add_mode(shop_window, name=mode, cost=costs[number], x_cord=cords[number][0], y_cord=cords[number][1])
        number += 1

    # ADD GO BACK BUTTON
    QuitButton('Go back', shop_window)

    shop_window.mainloop()


class QuitButton(Button):
    def __init__(self, name, parent):
        Button.__init__(self, parent)
        self['text'] = name
        self['command'] = parent.destroy
        self['height'] = 3
        self['width'] = 15
        self['bg'] = 'red'
        self['fg'] = 'black'
        self.place(relx=0.1, rely=0.9, anchor='center')


# MAKING START WINDOW
window = Tk()
window.title("Main menu")
window_height = 450
window_width = 600
window.geometry('{}x{}+0+0'.format(window_width, window_height))
center(window)

max_score = 0
last_score = 0
money = 0
selected_mode = 1
record_lbl = Label(text='Your record : {}'.format(max_score), font=(None, 20, 'bold'))
record_lbl.pack()
last_score_lbl = Label(text='Your last score : {}'.format(last_score), font=(None, 20, 'bold'))
last_score_lbl.pack()


# MAKING START BUTTON
start_btn = Button(window, text='Start game', bg='pink', fg='black', height=7, width=30, command=start_button_clicked)
start_btn.place(relx=0.5, rely=0.5, anchor='center')

# MAKING SHOP BUTTON
shop_btn = Button(window, text='Shop', bg='pink', fg='black', height=3, width=15, command=shop_button_clicked)
shop_btn.place(relx=0.9, rely=0.9, anchor='center')

# MAKING CHOOSE MOD BUTTON
modes_array = [('1.Halloween', 1)]
all_modes_array = [('1.Halloween', 1), ('2.Dark Halloween', 2), ('3.Wild West', 3)]
cords = [(0.17, 0.3), (0.5, 0.3), (0.83, 0.3)]
costs = [0, 300, 750]
choose_mod_btn = Button(window, text='Choose \n mode', bg='pink', fg='black', height=3, width=15)
choose_mod_btn.config(command=choose_mod_button_clicked)
choose_mod_btn.place(relx=0.9, rely=0.75, anchor='center')

# MAKING EXIT BUTTON
QuitButton('Exit', window)

window.mainloop()
