import pygame
import random
import time

class Game:
    def __init__(self, window_width=800, window_height=500):
        pygame.init()
        self.width = window_width
        self.height = window_height
        self.snake_clock = Clock(10)
        self.render_clock = Clock(60)


    def start(self):
        self.screen = Screen(self.width, self.height)
        self.snake = Snake()
        self.background = Surface(self.width, self.height, (255, 0, 0))
        self.running = True
        self.state = 'running'
        self.event_queue = []
        self.food_lst = []


    def run(self):
        self.start()
        while self.running:
            self.get_events(pygame.event.get())
            self.generate_food(2)

            if self.event_queue is False:
                self.running = False

            if self.snake_clock.should_update():
                if self.state == 'running':
                    self.update()

            if self.render_clock.should_update():
                snake_board = self.snake.get_area()
                snake_board.fill(snake_board.get_surface(), (0,0,0))
                snake_board.blit_snake(self.snake.get_width(), self.snake.get_body(), \
                                       (255,255,255))
                snake_board.blit_food(self.snake.get_width(), self.food_lst)
                self.background.blit(snake_board.get_surface(), (10, 10))
                self.screen.blit(self.background.get_surface(), (0,0))
        pygame.quit()


    def update(self):
        if self.event_queue:
            event = self.event_queue[0]
            self.event_queue = self.event_queue[1:]
            self.snake.change_facing(event)
        new_head = self.snake.get_snake_head()
        nutrition = self.check_snake_head(new_head)
        if nutrition:
            for food in self.food_lst:
                food.time_passed()
                if food.is_rotted():
                    self.food_lst.remove(food)
            self.generate_special('poison', 10)
            self.generate_special('vege', 20)
            self.generate_special('super', 5)
        self.snake.update(new_head, nutrition)
        if self.snake.is_dead():
            self.state = 'game over'


    def change_game_state(self):
        if self.state == 'running':
            self.state = 'paused'
            #self.time_paused = time.monotonic()
            self.snake_clock.pause()

        elif self.state == 'paused':
            self.state = 'running'
            #self.time_resumed = time.monotonic()
            #self.total_paused += self.time_resumed - self.time_paused
            self.snake_clock.unpause()

        elif self.state == 'game over' or self.state == 'not started':
            self.state = 'running'
            self.start()



    def get_events(self, events):
        def what_direction(event):
            if event.key == pygame.K_UP:
                return 'up'
            elif event.key == pygame.K_DOWN:
                return 'down'
            elif event.key == pygame.K_LEFT:
                return 'left'
            elif event.key == pygame.K_RIGHT:
                return 'right'

        oppo_direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
        for event in events:
            if event.type == pygame.QUIT:
                self.event_queue = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_queue = False
                elif event.key == pygame.K_SPACE:
                    self.change_game_state()

                if self.state == 'running':
                    direction = what_direction(event)
                    if direction:
                        if self.event_queue == []:
                            self.event_queue.append(direction)

                        elif self.event_queue and len(self.event_queue) <= 3:
                            if self.event_queue[-1] != oppo_direction[direction] and \
                            self.event_queue[-1] != direction:
                                self.event_queue.append(direction)


    def generate_food(self, max_food_num):
        area = self.snake.get_area()
        snake_body = self.snake.get_body()
        food_pos = [food.get_position for food in self.food_lst]
        normal_food_num = len([food for food in self.food_lst \
                               if food.get_type() == 'normal'])
        existing_points = snake_body+food_pos
        if normal_food_num == 0:
            for _ in range(max_food_num):
                point = area.generate_random_point(self.snake.get_width(), existing_points)
                self.food_lst.append(Food(point))
                existing_points += [point]


    def generate_special(self, food_type, probability):
        area = self.snake.get_area()
        snake_body = self.snake.get_body()
        food_pos = [food.get_position() for food in self.food_lst]
        existing_points = snake_body+food_pos

        random_number = random.uniform(0, 1)
        if random_number <= probability/100:
            point = area.generate_random_point(self.snake.get_width(), existing_points)
            if food_type == 'poison':
                self.food_lst.append(Food(point, food_type, 5))
            elif food_type == 'vege':
                self.food_lst.append(Food(point, food_type, 3))
            elif food_type == 'super':
                self.food_lst.append(Food(point, food_type, 1))


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


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))


    def blit(self, board, position):
        self.screen.blit(board, position)
        pygame.display.update()


class Surface:
    def __init__(self, width, height, color=(0,0,0)):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)


    def blit(self, surface, position):
        self.surface.blit(surface, position)

    def fill(self, surface, color):
        self.surface.fill(color)

    def generate_random_point(self, point_width, existing_points):
        max_width = self.width // point_width - 1
        max_height = self.height // point_width - 1
        empty_space = [(a, b) for a in range(max_width)
                              for b in range(max_height)
                              if (a, b) not in existing_points]
        n = random.randint(0, len(empty_space)-1)
        return empty_space[n]

    def blit_snake(self, cell_width, snake, color):
        for (x, y) in snake:
            pygame.draw.rect(self.surface, color,
                            (cell_width*x, cell_width*y,
                            cell_width, cell_width))

    def blit_food(self, cell_width, food_lst):
        for food in food_lst:
            x, y = food.get_position()
            if food.get_type() == 'normal':
                color = (255,255,255)
            elif food.get_type() == 'poison':
                color = (255,0,0)
            elif food.get_type() == 'vege':
                color = (0,255,0)
            elif food.get_type() == 'super':
                color = (0,0,255)
            pygame.draw.rect(self.surface, color,
                            (cell_width*x, cell_width*y,
                            cell_width, cell_width))


    def get_surface(self):
        return self.surface


class Snake:
    def __init__(self, length=1, facing='right', width=20, area=(30,20)):
        self.length = length
        self.width = width
        self.area_x = area[0]
        self.area_y = area[1]
        self.facing = facing
        self.body = [(self.area_x//2, self.area_y//2)]
        self.area = Surface(self.width*self.area_x, self.width*self.area_y)
        self.nutrition = 0


    def change_facing(self, direction):
        oppo_direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
        if direction != oppo_direction[self.facing]:
            self.facing = direction


    def move(self, new_head):
        self.body = [new_head] + self.body[:-1]


    def grow(self, new_head):
        self.body = [new_head] + self.body
        self.nutrition -= 1


    def shrink(self, new_head):
        self.body = [new_head] + self.body[:len(self.body)//2]
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
            self.shrink(snake_head)

    def is_dead(self):
        if len(self.body) != len(set(self.body)):
            return True
        for (x, y) in self.body:
            if x < 0 or x >= self.area_x:
                return True
            if y < 0 or y >= self.area_y:
                return True
        return False

    def get_area(self):
        return self.area


    def get_body(self):
        return self.body


    def get_width(self):
        return self.width


class Food:
    def __init__(self, position, food_type='normal', lasting_time=999):
        self.position = position
        self.type = food_type
        self.lasting_time = lasting_time

    def time_passed(self):
        self.lasting_time -= 1

    def get_position(self):
        return self.position

    def get_type(self):
        return self.type

    def is_rotted(self):
        return self.lasting_time <= 0


if __name__ == '__main__':
    Game().run()
