from typing import List, Generator
import pygame
import time
import math
import os
import random

os.system('')

_unique_id = 0

def error(text):
    print(f'\033[91m[Error] {text}\033[0m')

def warning(text):
    print(f'\033[93m[Warning] {text}\033[0m')

def info(text):
    print(f'\033[94m[Info] {text}\033[0m')

def success(text):
    print(f'\033[92m[Success] {text}\033[0m')

def sleep(second):
    timer = second
    while timer > 0:
        timer -= yield

def randint(a, b):
    return random.randint(a, b)

class Keys:
    Q = pygame.K_q
    W = pygame.K_w
    E = pygame.K_e
    R = pygame.K_r
    T = pygame.K_t
    Y = pygame.K_y
    U = pygame.K_u
    I = pygame.K_i
    O = pygame.K_o
    P = pygame.K_p
    A = pygame.K_a
    S = pygame.K_s
    D = pygame.K_d
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    Z = pygame.K_z
    X = pygame.K_x
    C = pygame.K_c
    V = pygame.K_v
    B = pygame.K_b
    C = pygame.K_c
    N = pygame.K_n
    M = pygame.K_m

    K1 = pygame.K_1
    K2 = pygame.K_2
    K3 = pygame.K_3
    K4 = pygame.K_4
    K5 = pygame.K_5
    K6 = pygame.K_6
    K7 = pygame.K_7
    K8 = pygame.K_8
    K9 = pygame.K_9
    K0 = pygame.K_0

    F1 = pygame.K_F1
    F2 = pygame.K_F2
    F3 = pygame.K_F3
    F4 = pygame.K_F4
    F5 = pygame.K_F5
    F6 = pygame.K_F6
    F7 = pygame.K_F7
    F8 = pygame.K_F8
    F9 = pygame.K_F9
    F10 = pygame.K_F10
    F11 = pygame.K_F11
    F12 = pygame.K_F12

    MINUS = pygame.K_MINUS                  # -
    EQUALS = pygame.K_EQUALS                # =
    BACKSLASH = pygame.K_BACKSLASH          # \
    LEFTBRACKET = pygame.K_LEFTBRACKET      # [
    RIGHTBRACKET = pygame.K_RIGHTBRACKET    # ]

 
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    
    SPACE = pygame.K_SPACE
    ENTER = pygame.K_RETURN
    ESC = pygame.K_ESCAPE
    TAB = pygame.K_TAB
    LSHIFT = pygame.K_LSHIFT
    LCTRL = pygame.K_LCTRL
    LALT = pygame.K_LALT
    RSHIFT = pygame.K_RSHIFT
    RCTRL = pygame.K_RCTRL
    RALT = pygame.K_RALT
    BACKSPACE = pygame.K_BACKSPACE
    DELETE = pygame.K_DELETE
    PAGEUP = pygame.K_PAGEUP
    PAGEDOWN = pygame.K_PAGEDOWN

class KeyVector:

    @classmethod
    def WASD(cls):
        vector = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            vector.y += 1
        if keys[pygame.K_s]:
            vector.y -= 1
        if keys[pygame.K_a]:
            vector.x -= 1
        if keys[pygame.K_d]:
            vector.x += 1
        if vector.length() > 0:
            vector = vector.normalize()
        return vector.angle_to((0, 1)), vector.length()
    
    @classmethod
    def arrow(cls):
        vector = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            vector.y += 1
        if keys[pygame.K_DOWN]:
            vector.y -= 1
        if keys[pygame.K_LEFT]:
            vector.x -= 1
        if keys[pygame.K_RIGHT]:
            vector.x += 1
        if vector.length() > 0:
            vector = vector.normalize()
        return vector.angle_to((0, 1)), vector.length()
    
class MouseVector:

    @classmethod
    def get(cls):
        x, y = pygame.mouse.get_pos()
        return x, y

class Lines:
    def __init__(self):
        self._lines = []
        self._line_lengths = []

    def add(self, x1, y1, x2, y2):
        self._lines.append((x1, y1, x2, y2))
        self._line_lengths.append(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

    def random_point(self):
        if len(self._lines) == 0:
            raise Exception("No lines added")
        line = random.choices(self._lines, self._line_lengths)[0]
        x1, y1, x2, y2 = line
        r = random.uniform(0, 1)
        return (
            x1 + r * (x2 - x1),
            y1 + r * (y2 - y1)
        )

class Stage:
    def __init__(self, width, height):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Scratch")
        self._w = width
        self._h = height
        self._screen = pygame.display.set_mode((width, height))
        self._backgrounds = [] #背景列表
        self._background_index = 0 #当前背景的索引
        self._sprites:List[Sprite] = [] #角色的展示顺序
        self._scripts:List[Generator] = [] #角色脚本的展示顺序
        self.running = True
        self.fps = 30
        self._freeze_time = 0
        self._keydown_scripts = []
    
    def title(self, title):
        pygame.display.set_caption(title)

    def icon(self, icon):
        pygame.display.set_icon(icon)

    def add_script(self, script:Generator):
        next(script) # 执行一次脚本
        self._scripts.append(script)

    def add_keydown_script(self, script):
        self._keydown_scripts.append(script)

    def add_background(self, image):
        image = pygame.transform.scale(image, (self._w, self._h))
        self._backgrounds.append(image)

    def add_background_load(self, path):
        self.add_background(pygame.image.load(path))

    def get_screen_line(self):
        line = Lines()
        line.add(0,0,self._w, 0)
        line.add(self._w, 0, self._w, self._h)
        line.add(self._w, self._h, 0, self._h)
        line.add(0, self._h, 0, 0)
        return line
    
    def freeze(self, time = 0):
        self._freeze_time = time

    def exit(self):
        self.running = False
    
    def button(self, type, button, pos):
        if button >= 4:
            return
        for i in range(len(self._sprites)-1, -1, -1):
            character = self._sprites[i] # 从后往前遍历
            if character.is_hide:
                continue
            rect =  character._rect
            if rect is None:
                continue
            if rect.collidepoint(pos):
                f = character._button_scripts[type][button-1]
                if f is not None:
                    script, args = f
                    self.add_script(script(*args))

    def mainloop(self):
        last_time = time.time()
        while self.running:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self._freeze_time > 0:
                self._freeze_time -= delta_time
                if delta_time < 1 / self.fps:
                    time.sleep((1 / self.fps - delta_time))
                continue

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button(0, event.button, event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.button(1, event.button, event.pos)
                elif event.type == pygame.KEYDOWN:
                    for script in self._keydown_scripts:
                        self.add_script(script(event.key))

            self._screen.fill((255, 255, 255))
            if len(self._backgrounds) > 0:
                self._screen.blit(self._backgrounds[self._background_index], (0, 0))

            for generator in self._scripts[:]:
                try:
                    generator.send(delta_time)
                except StopIteration:
                    self._scripts.remove(generator)

            for character in self._sprites:
                character.show()

            pygame.display.flip()

            if delta_time < 1 / self.fps:
                time.sleep((1 / self.fps - delta_time))
            elif 1 / delta_time < self.fps - 5:
                warning(f'current fps: {1 / delta_time:.2f}')

        pygame.quit()

class SpImage:
    def __init__(self, image:pygame.Surface, center=None):
        self.image = image
        w, h = image.get_size()
        if center is None:
            center = (w // 2, h // 2)
        self.center = center

    def get_image(self, x, y, angle, scale):
        '''
        将图片围绕相对图片左上角坐标self.center为旋转中心，旋转angle度，并将旋转中心移动到(x, y)
        '''
        #计算图片四点坐标
        w, h = self.image.get_size()
        m, n = self.center
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        def rotate(a, b):
            return (
                a * cos - b * sin,
                a * sin + b * cos
            )
        
        x1, y1 = rotate(-m, -n)
        x2, y2 = rotate(w - m, -n)
        x3, y3 = rotate(w - m, h - n)
        x4, y4 = rotate(-m, h - n)

        xmin = min(x1, x2, x3, x4) + x
        ymin = min(y1, y2, y3, y4) + y
        #计算旋转后的图片
        img = pygame.transform.rotozoom(self.image, -angle, scale)

        #计算图片的rect
        rect = img.get_rect()
        
        rect.x = int(xmin)
        rect.y = int(ymin)

        return img, rect 
        
    @classmethod
    def load(cls, path:str, center=None):
        image = pygame.image.load(path)
        return cls(image, center)

class Sprite:
    def __init__(self, stage:Stage, image:SpImage, x=0, y=0):
        global _unique_id
        self._id = _unique_id
        _unique_id += 1
        self._stage = stage
        self._images = [image]
        self._image_index = 0
        self._x = x
        self._y = y
        self._last_x = x
        self._last_y = y
        self._stage._sprites.append(self)
        self.rotatable = True #是否可以旋转
        self.is_hide = False #是否隐藏
        self._angle = 0
        self._last_angle = 0
        self._scale = 1
        self._tags = {"all"}
        self._rect = None
        self._button_scripts = [[None, None, None],[None, None, None]]
        self._children:List[Sprite] = []

    def add_tags(self, types:List[str]):
        self._tags = self._tags.union(types)

    def add_image(self, image):
        self._images.append(image)

    def show(self):
        if self.is_hide:
            return
        angle = self._angle if self.rotatable else 0
        image, rect = self._images[self._image_index].get_image(self._x, self._y, angle, self._scale)
        self._rect = rect
        self._stage._screen.blit(image, rect)
        dx = self._x - self._last_x
        dy = self._y - self._last_y
        da = self._angle - self._last_angle
        for child in self._children:
            child._x += dx
            child._y += dy
            
            child._x , child._y = (
                (child._x - self._x) * math.cos(math.radians(da)) - (child._y - self._y) * math.sin(math.radians(da)) + self._x,
                (child._x - self._x) * math.sin(math.radians(da)) + (child._y - self._y) * math.cos(math.radians(da)) + self._y
            )
            child._angle += da
            child.show()
        self._last_x = self._x
        self._last_y = self._y
        self._last_angle = self._angle
            
    def move(self, length):
        self._x += length * math.sin(math.radians(self._angle))
        self._y -= length * math.cos(math.radians(self._angle))

    def move_to(self, x, y):
        self._x = x
        self._y = y

    def rotate(self, angle):
        self._angle += angle

    def rotate_to(self, angle):
        self._angle = angle

    def next_image(self):
        self._image_index = (self._image_index + 1) % len(self._images)

    def last_image(self):
        self._image_index = (self._image_index - 1) % len(self._images)

    def set_image_index(self, index):
        self._image_index = index % len(self._images)

    def scale(self, scale):
        self._scale = scale

    def get_pos(self):
        return self._x, self._y

    def get_angle(self):
        return self._angle

    def get_angle_to(self, x, y):
        return math.degrees(math.atan2( x - self._x, self._y - y))
    
    def copy(self):
        new_sprite = Sprite(self._stage, self._images[0], self._x, self._y)
        for image in self._images[1:]:
            new_sprite.add_image(image)
        new_sprite.rotatable = self.rotatable
        new_sprite.is_hide = self.is_hide
        new_sprite._angle = self._angle
        new_sprite._scale = self._scale
        new_sprite._tags = self._tags.copy()
        new_sprite._button_scripts = self._button_scripts.copy()
        new_sprite.set_image_index(self._image_index)
        return new_sprite

    def remove(self):
        for i in range(len(self._stage._sprites)):
            if self._stage._sprites[i]._id == self._id:
                self._stage._sprites.pop(i)
                break

    def collide(self, tags=None):
        if tags is None:
            tags = ['all']
        if self.is_hide or not self._rect:
            return []

        return [
            i
            for i in self._stage._sprites
            if not i.is_hide
            and i is not self
            and i._tags.intersection(tags)
            and i._rect
            and self._rect.colliderect(i._rect)
        ]
    
    def on_left_press(self, script, *args):
        self._button_scripts[0][0] = [script, args]

    def on_middle_press(self, script, *args):
        self._button_scripts[0][1] = [script, args]

    def on_right_press(self, script, *args):
        self._button_scripts[0][2] = [script, args]

    def on_left_release(self, script, *args):
        self._button_scripts[1][0] = [script, args]

    def on_middle_release(self, script, *args):
        self._button_scripts[1][1] = [script, args]

    def on_right_release(self, script, *args):
        self._button_scripts[1][2] = [script, args]

    def bind(self, sprite):
        self._stage._sprites.remove(sprite)
        self._children.append(sprite)

    def unbind(self, sprite):
        self._children.remove(sprite)
        self._stage._sprites.append(sprite)
