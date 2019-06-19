import pygame
import random
import time

BG = pygame.image.load('background.png')
BG_x, BG_y = BG.get_rect().size


PALLETE = {
    'fg': (255, 255, 255),
    'bg': (0, 0, 0),
    'dark':(153, 196, 96),
    'light':(188, 214, 100),
    'poison': (255, 0, 0),
    'vege': (0, 255, 0),
    'super': (0, 0, 255)
}


class Game:
    def __init__(self, window_width=800, window_height=500):
        pygame.init()
        self.width = window_width
        self.height = window_height
        self.snake_clock = Clock(10)
        self.render_clock = Clock(60)
        self.cell_width = 30
        self.col = 20
        self.row = 15
        self.bg = pygame.transform.scale(BG, (window_width, window_height))


    def start(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.playground = pygame.Surface((self.cell_width*self.col, self.cell_width*self.row))
        self.playground_bg = pygame.Surface((self.cell_width*self.col, self.cell_width*self.row))
        self.blit_playground_bg()
        self.snake_board = Playground(self.col, self.row)
        self.snake = Snake(initial_position=(self.col//2, self.row//2))
        self.running = True
        self.state = 'running'
        self.event_queue = []
        self.food_lst = []
        self.get_snake_pic()
        self.body_tile = self.find_body_tile( \
            self.snake.get_body(), self.snake.get_facing())


    def get_snake_pic(self):
        snake_color_lst = ['orange', 'blue', 'pink', 'white', 'purple', 'yellow', 'red']
        snake_color = snake_color_lst[random.randint(0,len(snake_color_lst)-1)]
        self.head_r = pygame.transform.scale( \
            pygame.image.load('snake_pic/'+snake_color+'/head.png'), (self.cell_width, self.cell_width))
        self.tail_r = pygame.transform.scale( \
            pygame.image.load('snake_pic/'+snake_color+'/tail.png'), (self.cell_width, self.cell_width))
        self.body_h = pygame.transform.scale( \
            pygame.image.load('snake_pic/'+snake_color+'/body.png'), (self.cell_width, self.cell_width))
        self.corner_dl = pygame.transform.scale( \
            pygame.image.load('snake_pic/'+snake_color+'/corner.png'), (self.cell_width, self.cell_width))
        self.dead_head_r = pygame.transform.scale( \
            pygame.image.load('snake_pic/'+snake_color+'/dead.png'), (self.cell_width, self.cell_width))

    def run(self):
        self.start()
        border = (self.height - self.cell_width * self.row) // 2
        while self.running:
            self.process_events(pygame.event.get())
            self.generate_food(2)

            if self.event_queue is False:
                self.running = False

            if self.snake_clock.should_update():
                if self.state == 'running':
                    self.update()
                    self.body_tile = self.find_body_tile( \
                        self.snake.get_body(), self.snake.get_facing())
                elif self.state == 'dying':
                    self.state = 'game over'
                    self.body_tile = self.find_body_tile( \
                        self.snake.get_body(), self.snake.get_facing())

            if self.render_clock.should_update():
                if self.state == 'running' or self.state == 'dying':
                    self.blit_snake()
                elif self.state == 'game over':
                    self.blit_dead_snake()
                self.blit_food()
                self.background.blit(self.bg, (0,0))
                self.background.blit(self.playground, (border,border))
                self.screen.blit(self.background, (0,0))
                pygame.display.update()
        pygame.quit()


    def update(self):
        if self.event_queue:
            event = self.event_queue[0]
            self.event_queue = self.event_queue[1:]
            self.snake.change_facing(event)
        next_head = self.snake.get_snake_head()

        if self.snake.will_hit_wall(next_head, self.col, self.row) or \
            self.snake.will_eat_self(next_head):
            self.state = 'dying'
            self.previous_snake_body = self.snake.get_body()
            self.previous_body_tile = self.body_tile

        nutrition = self.check_snake_head(next_head)
        if nutrition:
            for food in self.food_lst:
                food.time_passed()
                if food.is_rotted():
                    self.food_lst.remove(food)
            self.generate_special_food('poison', PALLETE['poison'], 10)
            self.generate_special_food('vege', PALLETE['vege'], 20)
            self.generate_special_food('super', PALLETE['super'], 5)
        self.snake.update(next_head, nutrition)



    def toggle_game_state(self):
        if self.state == 'running' or self.state == 'dying':
            self.previous_state = self.state
            self.state = 'paused'
            #self.time_paused = time.monotonic()
            self.snake_clock.pause()

        elif self.state == 'paused':
            self.state = self.previous_state
            #self.time_resumed = time.monotonic()
            #self.total_paused += self.time_resumed - self.time_paused
            self.snake_clock.unpause()

        elif self.state == 'game over' or self.state == 'not started':
            self.state = 'running'
            self.start()



    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                elif event.key == pygame.K_SPACE:
                    self.toggle_game_state()

                if self.state != 'running':
                    continue

                if event.key == pygame.K_UP:
                    self.append_movement_event('up')
                elif event.key == pygame.K_DOWN:
                    self.append_movement_event('down')
                elif event.key == pygame.K_LEFT:
                    self.append_movement_event('left')
                elif event.key == pygame.K_RIGHT:
                    self.append_movement_event('right')


    def quit_game(self):
        self.event_queue = False

    def append_movement_event(self, dir):
        opposite_direction = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }

        if self.event_queue is False:
            return
        if len(self.event_queue) > 3:
            return
        if self.event_queue == []:
            self.event_queue.append(dir)

        if self.event_queue[-1] not in [dir, opposite_direction[dir]]:
            self.event_queue.append(dir)


    def generate_food(self, max_food_num):
        snake_body = self.snake.get_body()
        food_pos = [food.get_position for food in self.food_lst]
        normal_food_num = len([food for food in self.food_lst \
                               if food.get_type() == 'normal'])
        masked_area = snake_body + food_pos
        if normal_food_num != 0:
            return

        for _ in range(max_food_num):
            point = self.snake_board.generate_random_point(self.cell_width, forbidden=masked_area)
            self.food_lst.append(Food(point))
            masked_area += [point]


    def generate_special_food(self, food_type, food_color, probability):
        snake_body = self.snake.get_body()
        food_pos = [food.get_position() for food in self.food_lst]
        masked_area = snake_body + food_pos

        random_number = random.uniform(0, 1)
        if random_number <= probability/100:
            point = self.snake_board.generate_random_point(self.cell_width, forbidden=masked_area)
            if food_type == 'poison':
                self.food_lst.append(Food(point, food_type, food_color, 5))
            elif food_type == 'vege':
                self.food_lst.append(Food(point, food_type, food_color, 3))
            elif food_type == 'super':
                self.food_lst.append(Food(point, food_type, food_color, 1))


    def check_snake_head(self, snake_head):
        for food in self.food_lst:
            if food.get_position() == snake_head:
                food_type = food.get_type()
                self.food_lst.remove(food)
                if food_type == 'normal':
                    return 1
                elif food_type == 'vege':
                    return 3
                elif food_type == 'super':
                    return 10
                elif food_type == 'poison':
                    return -999
        return 0

    def blit_playground_bg(self):
        color = {0:PALLETE['dark'], 1:PALLETE['light']}
        for col in range(self.col):
            color_index = col % 2
            for row in range(self.row):
                pygame.draw.rect(self.playground_bg, color[color_index],
                            (self.cell_width*col, self.cell_width*row,
                            self.cell_width, self.cell_width))
                color_index = (color_index + 1) % 2


    def find_body_tile(self, snake_body, facing):
        def detect_corner_degree(point, previous_point, next_point):
            x1, y1 = previous_point
            x2, y2 = point
            x3, y3 = next_point
            if x1 == x2 and x2 == x3:
                return False
            if y1 == y2 and y2 == y3:
                return False
            if all([y1<y2, x2>x3]) or all([x1<x2, y2>y3]):
                return 270 # upleft
            if all([y1<y2, x2<x3]) or all([x1>x2, y2>y3]):
                return 180 # upright
            if all([y1>y2, x2<x3]) or all([x1>x2, y2<y3]):
                return 90 # downright
            if all([y1>y2, x2>x3]) or all([x1<x2, y2<y3]):
                return 0 # downleft

        def detect_tail_degree(tail, before_tail):
            x1, y1 = before_tail
            x2, y2 = tail

            if x1 == x2 and y1 > y2:
                return 270 #'down'
            if x1 < x2 and y1 == y2:
                return 180 #'left'
            if x1 == x2 and y1 < y2:
                return 90 #'up'
            if x1 > x2 and y1 == y2:
                return 0 #'right'

        def detect_body_degree(facing):
            if facing == 'up' or facing == 'down':
                return 90 #'vertical'
            elif facing == 'left' or facing == 'right':
                return 0 #'horizontal'

        def switch_body_degree(body_facing):
            if body_facing == 0:
                return 90
            return 0

        def facing_to_degree(facing):
            if facing == 'right':
                return 0
            if facing == 'up':
                return 90
            if facing == 'left':
                return 180
            if facing == 'down':
                return 270

        length = len(snake_body)
        body_degree = detect_body_degree(facing)
        lst = []
        for i in range(length):
            if i == 0:
                lst.append(('head', facing_to_degree(facing)))
                continue
            elif i == length-1:
                tail_degree = detect_tail_degree(snake_body[i], snake_body[i-1])
                lst.append(('tail', tail_degree))
                continue
            corner_degree = detect_corner_degree(snake_body[i], snake_body[i-1], snake_body[i+1])
            if type(corner_degree) is int:
                lst.append(('corner', corner_degree))
                body_degree = switch_body_degree(body_degree)
            else:
                lst.append(('body', body_degree))
        return lst


    def blit_snake(self):
        tile_dic = {
            'head': self.head_r,
            'tail': self.tail_r,
            'body': self.body_h,
            'corner':self.corner_dl,
        }
        self.playground.blit(self.playground_bg, (0, 0))
        for (x, y), (tile, degree) in list(zip(self.snake.get_body(), self.body_tile))[::-1]:
            self.playground.blit(pygame.transform.rotate(tile_dic[tile], degree), \
                (self.cell_width*x, self.cell_width*y))

    def blit_dead_snake(self):
        tile_dic = {
            'head': self.dead_head_r,
            'tail': self.tail_r,
            'body': self.body_h,
            'corner':self.corner_dl,
        }
        self.playground.blit(self.playground_bg, (0, 0))
        for (x, y), (tile, degree) in zip(self.previous_snake_body, self.previous_body_tile):
            self.playground.blit(pygame.transform.rotate(tile_dic[tile], degree), \
                (self.cell_width*x, self.cell_width*y))



    def blit_food(self):
        for food in self.food_lst:
            x, y = food.get_position()
            color = food.get_color()
            pygame.draw.rect(self.playground, color,
                            (self.cell_width*x, self.cell_width*y,
                            self.cell_width, self.cell_width))


class Clock:
    def __init__(self, ups):
        self.ups = ups
        self.prev_time = time.monotonic()
        self.paused = False

    def should_update(self):
        if self.paused:
            return False
        now = time.monotonic()
        if now - self.prev_time >= 1 / self.ups:
            self.prev_time = now
            return True
        return False

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def set_ups(self, new_ups):
        self.ups = new_ups


class Playground:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def generate_random_point(self, point_width, forbidden=[]):
        empty_space = [(a, b) for a in range(self.col)
                              for b in range(self.row)
                              if (a, b) not in forbidden]
        n = random.randint(0, len(empty_space)-1)
        return empty_space[n]


class Snake:
    def __init__(self, length=1, initial_position=(15,10)):
        self.length = length
        self.facing = 'right'
        x, y = initial_position
        self.body = [(x, y), (x-1, y), (x-2, y)]
        self.nutrition = 0


    def change_facing(self, direction):
        opposite_direction = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }
        if direction != opposite_direction[self.facing]:
            self.facing = direction


    def move(self, next_head):
        self.body = [next_head] + self.body[:-1]


    def grow(self, next_head):
        self.body = [next_head] + self.body
        self.nutrition -= 1


    def halve(self, next_head): # minimum length = 3
        length = len(self.body)
        half = length // 2
        if half <= 3:
            self.body = [next_head] + self.body[0:2]
        else:
            self.body = [next_head] + self.body[:len(self.body)//2]
        self.nutrition = 0


    def get_snake_head(self):
        x, y = self.body[0]
        if self.facing == 'up':
            new_head = (x, y-1)
        elif self.facing == 'down':
            new_head = (x, y+1)
        elif self.facing == 'left':
            new_head = (x-1, y)
        elif self.facing == 'right':
            new_head = (x+1, y)
        return new_head


    def update(self, snake_head, nutrition):
        self.nutrition += nutrition
        if self.nutrition > 0:
            self.grow(snake_head)
        elif self.nutrition == 0:
            self.move(snake_head)
        else:
            self.halve(snake_head)

    def will_eat_self(self, next_head):
        return next_head in self.body

    def will_hit_wall(self, next_head, col, width):
        x, y = next_head
        if x < 0 or x >= col:
            return True
        if y < 0 or y >= width:
            return True
        return False

    def get_body(self):
        return self.body

    def get_facing(self):
        return self.facing

class Food:
    def __init__(self, position, food_type='normal', color=(255,255,255), \
                lasting_time=999):
        self.position = position
        self.type = food_type
        self.lasting_time = lasting_time
        self.color = color

    def time_passed(self):
        self.lasting_time -= 1

    def get_position(self):
        return self.position

    def get_type(self):
        return self.type

    def get_color(self):
        return self.color

    def is_rotted(self):
        return self.lasting_time <= 0


if __name__ == '__main__':
    Game().run()
