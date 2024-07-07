from typing import Any, List, Generator
import pygame
import time
import math
import os

os.system('')

def error(text):
    print(f'\033[91m[Error] {text}\033[0m')

def warning(text):
    print(f'\033[93m[Warning] {text}\033[0m')

def info(text):
    print(f'\033[94m[Info] {text}\033[0m')

def success(text):
    print(f'\033[92m[Success] {text}\033[0m')

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
        return vector.angle_to((0, 0)), vector.length()
    
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
        return vector.angle_to((0, 0)), vector.length()
    
class MouseVector:

    @classmethod
    def get(cls):
        x, y = pygame.mouse.get_pos()
        return x, y

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
        self._characters:List[Sprite] = [] #角色的展示顺序
        self._scripts:List[Generator] = [] #角色脚本的展示顺序
        self.running = True
        self.fps = 30
    
    def title(self, title):
        pygame.display.set_caption(title)

    def icon(self, icon):
        pygame.display.set_icon(icon)

    def add_script(self, script:Generator):
        next(script) # 执行一次脚本
        self._scripts.append(script)

    def add_background(self, image):
        image = pygame.transform.scale(image, (self._w, self._h))
        self._backgrounds.append(image)

    def add_background_load(self, path):
        self.add_background(pygame.image.load(path))

    def mainloop(self):
        last_time = time.time()
        while self.running:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self._screen.fill((255, 255, 255))
            if len(self._backgrounds) > 0:
                self._screen.blit(self._backgrounds[self._background_index], (0, 0))

            for generator in self._scripts[:]:
                try:
                    generator.send(delta_time)
                except StopIteration:
                    self._scripts.remove(generator)

            for character in self._characters:
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
        self._stage = stage
        self._images = [image]
        self._image_index = 0
        self._x = x
        self._y = y
        self._stage._characters.append(self)
        self.rotatable = True #是否可以旋转
        self.is_hide = False #是否隐藏
        self._angle = 0
        self._scale = 1

    def add_image(self, image):
        self._images.append(image)

    def show(self):
        if self.is_hide:
            return
        angle = self._angle if self.rotatable else 0
        image, rect = self._images[self._image_index].get_image(self._x, self._y, angle, self._scale)
        self._stage._screen.blit(image, rect)


    def move(self, length):
        self._x += length * math.cos(math.radians(self._angle))
        self._y += length * math.sin(math.radians(self._angle))

    def move_to(self, x, y):
        self._x = x
        self._y = y

    def moveXY(self, x, y):
        self._x += x
        self._y += y

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

    def get_angle(self):
        return self._angle

    def get_angle_to(self, x, y):
        return math.degrees(math.atan2(y - self._y, x - self._x))
    
    def copy(self):
        new_sprite = Sprite(self._stage, self._images[0], self._x, self._y)
        for image in self._images[1:]:
            new_sprite.add_image(image)
        new_sprite.rotatable = self.rotatable
        new_sprite.is_hide = self.is_hide
        new_sprite._angle = self._angle
        new_sprite._scale = self._scale
        new_sprite.set_image_index(self._image_index)
        return new_sprite

    def remove(self):
        self._stage._characters.remove(self)
