from tkinter import *
import random
import time

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 650

APPLE_WIDTH = 30
APPLE_HEIGHT = 30

SNAKE_WIDTH = 30
SNAKE_HEIGHT = 30
SNAKE_COLOR = 'yellow'

DELAY = 1 / 9


class Game:
    def __init__(self, root, canvas, apple_image, snake_image, trophy_image):
        self.root = root
        self.canvas = canvas

        self.apple_image = apple_image
        self.snake_image = snake_image
        self.trophy_image = trophy_image

        self._set_starting_screen()

    def _set_starting_screen(self):
        self.root.configure(background='black')

        self.canvas.create_image(0 + APPLE_WIDTH / 2, 10, image=self.apple_image, anchor=NW)
        self.canvas.create_image(350, 0, image=self.snake_image, anchor=NW)
        self.canvas.create_image(150, 5, image=self.trophy_image, anchor=NW)

        self.canvas.create_line(0, 50, CANVAS_WIDTH, 50, fill='white')

        x = 0
        y = 0
        row = 20

        s = CANVAS_WIDTH // row

        for i in range(row):
            x += s
            y += s

            self.canvas.create_line(x, 50, x, CANVAS_HEIGHT, fill='white')
            self.canvas.create_line(0, y + 50, CANVAS_WIDTH, y + 50, fill='white')

    def get_score_text(self, score):
        return self.canvas.create_text(0 + APPLE_WIDTH / 2 + 55, 25,
                                       fill='white',
                                       text=':' + str(score),
                                       anchor=CENTER,
                                       font='Courier 25')

    def get_max_score_text(self, max_score):
        return self.canvas.create_text(205, 25,
                                       fill='white',
                                       text=':' + str(max_score),
                                       anchor=CENTER,
                                       font='Courier 25')

    def show_score(self, canvas, score):
        return self.canvas.create_text(0 + APPLE_WIDTH / 2 + 55, 25,
                                       fill='white',
                                       text=':' + str(score),
                                       anchor=CENTER,
                                       font='Courier 25')

    def show_max_score(self, max_score, max_score_text):
        return self.canvas.create_text(0 + APPLE_WIDTH / 2 + 55, 25,
                                       fill='white',
                                       text=':' + str(max_score),
                                       anchor=CENTER,
                                       font='Courier 25')

    def get_scores(self):
        score = 0
        max_score = 0

        return score, max_score

    def get_directions(self, presses, last_pressed):
        if presses[-1] == 'w' and last_pressed != 's':
            last_pressed = 'w'

        if presses[-1] == 'a' and last_pressed != 'd':
            last_pressed = 'a'

        if presses[-1] == 's' and last_pressed != 'w':
            last_pressed = 's'

        if presses[-1] == 'd' and last_pressed != 'a':
            last_pressed = 'd'

        return last_pressed

    def restart_snake_apple(self, snake, snake_list, snake_obj, apple, apple_obj, score_text):
        for i in snake_list:
            self.canvas.delete(i)

        self.canvas.delete(apple)
        self.canvas.delete(snake)

        snake, apple = snake_obj.create_snake(), apple_obj.create_apple()
        snake_list = [snake]

        score = 0
        self.show_score(score, score_text)

        return snake, snake_list, snake_obj, apple, apple_obj, score, score_text

    def respawn_apple(self, apple_obj, apple, snake_list, score, max_score, score_text, max_score_text):
        self.canvas.delete(apple)
        apple = apple_obj.create_apple()

        apple_x, apple_y = apple_obj.get_apple_coordinates(apple)

        for s in snake_list[1:]:
            if apple_x == self.canvas.coords(s)[0] and apple_y == self.canvas.coords(s)[1]:
                self.canvas.delete(apple)
                apple = apple_obj.create_apple()

        score += 1
        if score > max_score:
            max_score = score

        self.show_score(score, score_text)
        self.show_max_score(max_score, max_score_text)

        return apple, score


class Snake:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color

    def create_snake(self):
        snake_x1 = CANVAS_WIDTH / 2
        snake_y1 = CANVAS_HEIGHT / 2 - 5
        snake_x2 = CANVAS_WIDTH / 2 + SNAKE_WIDTH
        snake_y2 = CANVAS_HEIGHT / 2 + SNAKE_HEIGHT - 5

        snake = self.canvas.create_rectangle(snake_x1, snake_y1, snake_x2, snake_y2, fill=self.color)

        return snake

    def snake_hits_wall(self, snake):
        if self.canvas.coords(snake)[1] >= CANVAS_HEIGHT:
            return True

        if self.canvas.coords(snake)[1] < 50:
            return True

        if self.canvas.coords(snake)[0] < 0:
            return True

        if self.canvas.coords(snake)[0] >= CANVAS_WIDTH:
            return True

        return False

    def get_snake_coordinates(self, snake):
        snake_x1 = self.canvas.coords(snake)[0]
        snake_y1 = self.canvas.coords(snake)[1]
        snake_x2 = self.canvas.coords(snake)[2]
        snake_y2 = self.canvas.coords(snake)[3]

        return snake_x1, snake_y1, snake_x2, snake_y2

    def move_snake(self, snake_x1, snake_y1, snake_x2, snake_y2, color, last_pressed):
        if last_pressed == 'w':
            snake = self.canvas.create_rectangle(snake_x1, snake_y1 - 30,
                                                 snake_x2, snake_y2 - 30, fill=color)

        if last_pressed == 'a':
            snake = self.canvas.create_rectangle(snake_x1 - 30, snake_y1,
                                                 snake_x2 - 30, snake_y2, fill=color)

        if last_pressed == 's':
            snake = self.canvas.create_rectangle(snake_x1, snake_y1 + 30,
                                                 snake_x2, snake_y2 + 30, fill=color)

        if last_pressed == 'd':
            snake = self.canvas.create_rectangle(snake_x1 + 30, snake_y1,
                                                 snake_x2 + 30, snake_y2, fill=color)

        return snake

    def if_snake_overlaps(self, snake, snake_list, kill):
        for s in snake_list[1:]:
            if self.canvas.coords(snake)[0] == self.canvas.coords(s)[0] and self.canvas.coords(
                    snake)[1] == self.canvas.coords(s)[1]:
                kill = True
                break

        return kill


class Apple:
    def __init__(self, canvas, apple_image):
        self.canvas = canvas
        self.apple_image = apple_image

    def create_apple(self):
        xs = []
        a = 0

        ys = []
        b = 50

        for x in range(19):
            a += 30
            xs.append(a)

        for y in range(19):
            b += 30
            ys.append(b)

        apple = self.canvas.create_image(random.choice(xs), random.choice(ys),
                                         image=self.apple_image,
                                         anchor=NW)

        return apple

    def snake_eats_apple(self, snake, apple):
        return self.canvas.coords(snake)[0] == self.canvas.coords(apple)[0] and self.canvas.coords(snake)[1] == \
               self.canvas.coords(apple)[1]

    def get_apple_coordinates(self, apple):
        apple_x = self.canvas.coords(apple)[0]
        apple_y = self.canvas.coords(apple)[1]

        return apple_x, apple_y


def main():
    root = Tk()

    root.geometry('600x650')
    root.title('Snake Game')
    root.configure(bg='black')

    canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black')
    canvas.pack()

    apple_image = PhotoImage(file='apple1.png')
    snake_image = PhotoImage(file='snake.png')
    trophy_image = PhotoImage(file='trophy.png')

    game = Game(root=root, canvas=canvas,
                apple_image=apple_image,
                snake_image=snake_image,
                trophy_image=trophy_image)

    snake_obj = Snake(canvas=canvas, color=SNAKE_COLOR)
    snake = snake_obj.create_snake()

    applex_image = PhotoImage(file='applex.png')

    apple_obj = Apple(canvas=canvas, apple_image=applex_image)
    apple = apple_obj.create_apple()

    score, max_score = game.get_scores()
    score_text, max_score_text = game.get_score_text(score), game.get_max_score_text(max_score)

    snake_list = [snake]

    random_options = ['w', 'a', 's', 'd']
    last_pressed = random.choice(random_options)

    global presses
    presses = [last_pressed]

    while True:
        eat = False
        kill = False

        root.bind('<Key>', key_pressed)

        last_pressed = game.get_directions(presses=presses, last_pressed=last_pressed)

        if apple_obj.snake_eats_apple(snake=snake, apple=apple):
            apple, score = game.respawn_apple(apple_obj=apple_obj,
                                              apple=apple,
                                              snake_list=snake_list,
                                              score=score,
                                              max_score=max_score,
                                              score_text=score_text,
                                              max_score_text=max_score_text)
            eat = True

        if snake_obj.snake_hits_wall(snake):
            kill = True
            snake, snake_list, snake_obj, apple, apple_obj, score, score_text = game.restart_snake_apple(snake=snake,
                                                                                                         snake_list=snake_list,
                                                                                                         snake_obj=snake_obj,
                                                                                                         apple=apple,
                                                                                                         apple_obj=apple_obj,
                                                                                                         score_text=score_text)

        snake_x1, snake_y1, snake_x2, snake_y2 = snake_obj.get_snake_coordinates(snake)

        kill = snake_obj.if_snake_overlaps(snake, snake_list, kill)

        if kill:
            snake, snake_list, snake_obj, apple, apple_obj, score, score_text = game.restart_snake_apple(snake=snake,
                                                                                                         snake_list=snake_list,
                                                                                                         snake_obj=snake_obj,
                                                                                                         apple=apple,
                                                                                                         apple_obj=apple_obj,
                                                                                                         score_text=score_text)

        snake = snake_obj.move_snake(snake_x1=snake_x1,
                                     snake_y1=snake_y1,
                                     snake_x2=snake_x2,
                                     snake_y2=snake_y2,
                                     color=SNAKE_COLOR,
                                     last_pressed=last_pressed)

        if not eat:
            canvas.delete(snake_list[-1])
            snake_list.pop()

        # EXTEND THE SNAKE
        snake_list.insert(0, snake)

        canvas.update()
        time.sleep(DELAY)

    root.mainloop()


def key_pressed(event):
    presses.append(event.char)
    return presses


if __name__ == '__main__':
    main()
