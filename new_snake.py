import pygame
import random

class Game:
    def __init__(self, window_width=800, window_height=500):
        pygame.init()
        self.width = window_width
        self.height = window_height


    def start(self):
        self.screen = Screen(self.width, self.height)
        #self.snake = Snake()
        self.background = Surface(self.width, self.height, (255, 0, 0))
        self.running = True
        self.event_queue = []
        self.food_lst = []


    def run(self):
        self.start()
        while self.running:
            self.get_events(pygame.event.get())
            self.generate_food(2)
            self.update()
            self.screen.blit(self.background.get_surface(), (0,0))
        pygame.quit()


    def update(self):
        if self.event_queue is False:
            self.running = False
        if self.event_queue:
            for event in self.event_queue:
                #self.snake.update(event)
                pass


    def get_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.event_queue = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_queue = False

    def generate_food(self, max_food_num):
        area = self.snake.get_area()
        snake_body = self.snake.get_body()
        food_pos = [food.get_position for food in self.food_lst]
        normal_food_num = len([food for food in self.food_lst \
                               if food.get_type == 'normal'])
        existing_points = snake_body+food_pos
        if normal_food_num == 0:
            for _ in range(max_food_num):
                point = area.generate_random_point(snake.get_width, existing_points)
                self.food_lst.append(Food(point))
                existing_points += [point]


    def generate_special(self, food_type, probability):
        area = self.snake.get_area()
        snake_body = self.snake.get_body()
        food_pos = [food.get_position for food in self.food_lst]

        random_number = random.uniform(0, 1)
        if random_number <= probability/100:
            point = area.generate_random_point(snake.get_width, existing_points)
            if food_type == 'poison'
                self.food_lst.append(Food(point, food_type, 5))
            elif food_type == 'vege':
                self.food_lst.append(Food(point, food_type, 3))
            elif food_type = 'super':
                self.food_lst.append(Food(point, food_type, 1))


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


    def generate_random_point(self, point_width, existing_points):
        max_width = self.width // point_width - 1
        max_height = self.height // point_width - 1
        empty_space = [(a, b) for a in range(max_width)
                              for b in range(max_height)
                              if (a, b) not in existing_points]
        n = random.randint(0, len(empty_space)-1)
        return empty_space[n]


    def get_surface(self):
        return self.surface


class Snake:
    def __init__(self, length=1, facing='right', width=20, area=(30,20)):
        self.length = length
        self.width = width
        self.area_x = area[0]
        self.area_y = area[1]
        self.facing = facing
        self.body = [(col//2, row//2)]
        self.area = Surface((self.width*self.area_x, self.width*self.area_y))
        self.nutrition = 0


    def change_facing(self, direction):
        oppo_direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
        if direction != oppo_direction(self.facing):
            self.facing = direction


    def get_new_head(self):
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


    def move(self, new_head):
        self.body = [new_head] + self.body[:-1]


    def grow(self, new_head):
        self.body = [new_head] + self.body
        self.nutrition -= 1


    def shrink(self, new_head):
        self.body = [new_head] + self.body[:len(self.body)//2]
        self.nutrition = 0


    def check_food(self, new_head, food_lst, food_type):
        if new_head in food_lst:
            if food_type == 'normal':
                self.nutrition += 1
            elif food_type == 'vege':
                self.nutrition += 3
            elif food_type == 'super':
                self.nutrition += 10
            elif food_type == 'poison':
                self.nutrition = -1

            i = food_lst.index(new_head)
            return food_lst[:i] + food_lst[i+1:]

        else:
            return food_lst


    def update(self, event):
        self.change_facing(event)
        new_head = self.get_new_head
        food_lst = check_food(new_head, food_lst)
        if nutrition > 0:
            self.grow(new_head)
        elif nutrition == 0:
            self.move(new_head)
        else:
            self.shrink(new_head)

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
        self.lasting_time = 999
        self.rotted = False

    def check_rotted(self):
        if self.lasting_time <= 0:
            self.rotted = True

    def get_position(self);
        return self.position

    def get_type(self):
        return self.type

    def is_rotted(self):
        return self.rotted


if __name__ == '__main__':
    Game().run()
