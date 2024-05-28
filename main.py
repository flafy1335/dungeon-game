import pygame
from pygame import *
import sys
from os.path import join, getsize
import os
import random 

window = display.set_mode((700, 500))
timer = pygame.time.Clock()

def load_and_transform_images(directory, size):
    """
    Загружает все изображения из указанной директории, изменяет их размер до заданного и добавляет в список.

    :param directory: путь к директории с изображениями
    :param size: новый размер изображений (ширина, высота)
    :return: список трансформированных изображений
    """
    transformed_images = []

    # Перебираем файлы в директории
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Полный путь к файлу
            file_path = os.path.join(directory, filename)
            
            # Загрузка и трансформация изображения
            try:
                image = pygame.image.load(file_path)
                image = pygame.transform.scale(image, size)
                transformed_images.append(image)
            except pygame.error as e:
                print(f"Не удалось загрузить изображение: {file_path}. Ошибка: {e}")

    return transformed_images

monsters = load_and_transform_images('monster',(150,150))
spider_attack = load_and_transform_images('spider_attack', (300,300))
spider_walk = load_and_transform_images('spider_walk', (300,300))
spider_stand = load_and_transform_images('spider_stand', (300,300))
spider_jump = load_and_transform_images('spider_jump', (300,300))
torch_images = load_and_transform_images('torch', (70,70))

class Spider:
    def __init__(self,textures_stand, textures_attack, textures_walk, textures_jump,
                 x,y, direction,hp,speed):
        self.slow_counter = 0
        self.animation_counter = 0
        self.x = x
        self.y = y
        self.direction = direction
        self.hp = hp
        self.speed = speed
        self.maxhp = hp
        self.width = 300
        self.attack_left = textures_attack
        self.walk_left = textures_walk
        self.stand_left = textures_stand
        self.jump_left = textures_jump
        self.attack_right = []
        self.walk_right = []
        self.stand_right = []
        self.jump_right = []
        self.status = 'walk'
        self.hpbar = Hp(x=self.x, y=self.y, height=10, width=100, picture_red='red_square.png', picture_green='green_square.png')
        for texture in self.attack_left:
            texture = transform.flip(texture, True, False)
            self.attack_right.append(texture)
        for texture in self.walk_left:
            texture = transform.flip(texture, True, False)
            self.walk_right.append(texture)
        for texture in self.stand_left:
            texture = transform.flip(texture, True, False)
            self.stand_right.append(texture)
        for texture in self.jump_left:
            texture = transform.flip(texture, True, False)
            self.jump_right.append(texture)
        self.hpbar = Hp(x=self.x, y=self.y, height=10, width=100, picture_red='red_square.png', picture_green='green_square.png')
        self.picture = self.stand_left[0]
        self.mask = pygame.mask.from_surface(self.picture)
        self.mask_stand_left = pygame.mask.from_surface(self.stand_left[0])
        self.mask_stand_right = pygame.mask.from_surface(self.stand_right[0])
        self.mask_attack_left = pygame.mask.from_surface(self.attack_left[0])
        self.mask_attack_right = pygame.mask.from_surface(self.attack_right[0])
        self.mask_walk_left = pygame.mask.from_surface(self.walk_left[0])
        self.mask_walk_right = pygame.mask.from_surface(self.walk_right[0])

    def animation_stand(self):
        if self.direction == 'right':
            self.textures = self.stand_right
        if self.direction == 'left':
            self.textures = self.stand_left
        self.picture = self.textures[self.animation_counter]
        self.slow_counter += 1
        if self.slow_counter == 3:
            self.slow_counter = 0
            self.animation_counter += 1
        if self.animation_counter == len(self.textures):
            self.animation_counter = 0
    def walk(self): #хотьба
        self.animation_walk()
        can_move_x = True
        can_move_y = True
        new_x = self.x
        new_y = self.y
        if self.x + 150 < link.x:
            new_x += self.speed
            self.direction = 'right'
        else:
            self.direction = 'left'
            new_x -= self.speed
        if self.y + 150 < link.y:
            new_y += self.speed
        else:
            new_y -= self.speed
        offset_x = link.x - self.x
        offset_y = link.y - new_y
        if self.mask.overlap_area(link.mask_left, (offset_x, offset_y)):
            can_move_y = False
            can_move_x = False

        offset_x = link.x - new_x + 150
        offset_y = link.y - self.y
        print (offset_x)
        if offset_x > 150 and offset_x < 180:
            self.status = 'attack'
        if offset_x < 350 and offset_x > 300:
            self.status = 'attack'
        if self.mask.overlap_area(link.mask_left, (offset_x, offset_y)):
            can_move_x = False

        if can_move_x == True:
            self.x = new_x
        if can_move_y == True:
            self.y = new_y
    
    def attack(self):
        self.animation_attack()
        if self.x + 150 < link.x:
            self.direction = 'right'
        else:
            self.direction = 'left'
        offset_walk = link.x - self.x + 150
        if offset_walk < 120:
            self.status = 'walk'
        if offset_walk > 415:
            self.status = 'walk'
        print(offset_walk)
            


    def animation_attack(self):
        if self.direction == 'right':
            self.textures = self.attack_right
        if self.direction == 'left':
            self.textures = self.attack_left
        self.picture = self.textures[self.animation_counter]
        self.mask = pygame.mask.from_surface(self.picture)
        self.slow_counter += 1
        if self.slow_counter == 5:
            self.slow_counter = 0
            self.animation_counter += 1
        if self.animation_counter == len(self.textures):
            self.animation_counter = 0

    def animation_walk(self):
        if self.direction == 'right':
            self.textures = self.walk_right
        if self.direction == 'left':
            self.textures = self.walk_left
        try:
            self.picture = self.textures[self.animation_counter]
        except:
            self.animation_counter = 0
        self.slow_counter += 1
        if self.slow_counter == 5:
            self.slow_counter = 0
            self.animation_counter += 1
        if self.animation_counter == len(self.textures):
            self.animation_counter = 0
        self.mask = pygame.mask.from_surface(self.textures[0])



    def animation_jump(self):
        if self.direction == 'right':
            self.textures = self.jump_right
        if self.direction == 'left':
            self.textures = self.jump_left
        self.picture = self.textures[self.animation_counter]
        self.mask = pygame.mask.from_surface(self.picture)
        self.slow_counter += 1
        if self.slow_counter == 5:
            self.slow_counter = 0
            self.animation_counter += 1
        if self.animation_counter == len(self.textures):
            self.animation_counter = 0
    def jump(self):
        self.animation_jump()
    
    def show(self):
        print(self.status)
        window.blit(self.picture, (self.x, self.y))
        self.hpbar.show()
        if self.status == 'walk':
            self.walk()
        elif self.status == 'jump':
            self.jump()
        elif self.status == 'attack':
            self.attack()
        
        
        
        self.hpbar.x = self.x
        self.hpbar.y = self.y
        self.hpbar.picture_green = pygame.transform.scale(self.hpbar.picture_green, (self.hpbar.width/self.maxhp*self.hp, 10))

class Torch:
    def __init__(self,x,y,textures):
        self.x = x
        self.y = y
        self.textures = textures
        self.slow_counter = 0
        self.animation_counter = 0
        self.picture = textures[0]
    def animation(self):
        self.picture = self.textures[self.animation_counter]
        self.slow_counter += 1
        if self.slow_counter == 5:
            self.slow_counter = 0
            self.animation_counter += 1
        if self.animation_counter == len(self.textures):
            self.animation_counter = 0
    def show(self):
        self.animation()
        window.blit(self.picture, (self.x, self.y))





class Monster:
    def __init__(self,textures, x, y, direction, hp, aktiv_zone_high, aktiv_zone_width, speed):
        self.textures_right = textures
        self.aktiv_zone_high = aktiv_zone_high
        self.aktiv_zone_width = aktiv_zone_width
        self.speed = speed
        self.textures_left = []
        self.hp = hp
        self.maxhp = hp
        for texture in self.textures_right:
            texture = transform.flip(texture, True, False)
            self.textures_left.append(texture)
        self.x = x
        self.y = y
        self.hpbar = Hp(x=self.x, y=self.y, height=10, width=100, picture_red='red_square.png', picture_green='green_square.png')
        self.direction = direction #направление
        self.slow_counter = 0   #счетчик замедления
        self.animation_counter = 0 #счетчик анимации
        self.animation()
        self.picture = self.textures[0]
        self.mask = pygame.mask.from_surface(self.picture)

    def show(self):
        self.animation()
        self.walk() 
        window.blit(self.picture,(self.x, self.y))
        self.hpbar.show()
        self.hpbar.x = self.x
        self.hpbar.y = self.y
        self.hpbar.picture_green = pygame.transform.scale(self.hpbar.picture_green, (self.hpbar.width/self.maxhp*self.hp, 10))

    def animation(self):
        if self.direction == 'right':
            self.textures = self.textures_right
        if self.direction == 'left':
            self.textures = self.textures_left
        self.picture = self.textures[self.animation_counter]    #выбираем картинку из self.textures под номером self.animation_counter
        self.slow_counter += 1
        if self.slow_counter == 5:
            self.slow_counter = 0
            self.animation_counter += 1
        if self.animation_counter == len(self.textures): #если счетчик равен длине списка с текстурами
            self.animation_counter = 0

    def walk(self): #хотьба
        can_move_x = True
        can_move_y = True
        new_x = self.x
        new_y = self.y
        if self.x < link.x:
            new_x += self.speed
            self.direction = 'right'
        else:
            self.direction = 'left'
            new_x -= self.speed
        if self.y < link.y:
            new_y += self.speed
        else:
            new_y -= self.speed
        offset_x = link.x - self.x
        offset_y = link.y - new_y
        if self.mask.overlap_area(link.mask_left, (offset_x, offset_y)):
            can_move_y = False

        offset_x = link.x - new_x
        offset_y = link.y - self.y
        if self.mask.overlap_area(link.mask_left, (offset_x, offset_y)):
            can_move_x = False
        for wall in link.room.walls:
            offset_wall_x = wall.x - self.x
            offset_wall_y = wall.y - new_y
            if self.mask.overlap_area(wall.mask, (offset_wall_x, offset_wall_y)):
                can_move_y = False
                break
        for wall in link.room.walls:
            offset_wall_x = wall.x - new_x
            offset_wall_y = wall.y - self.y
            if self.mask.overlap_area(wall.mask, (offset_wall_x, offset_wall_y)):
                can_move_x = False
                break
        if can_move_x == True:
            self.x = new_x
        if can_move_y == True:
            self.y = new_y

            
class Player:
    def __init__(self, picture, width, height, x, y, textures, direction, room, sword_textures):
        self.textures = textures
        self.sword_textures = sword_textures
        self.textures_left = []
        self.sword_textures_left = []
        self.textures_right = []
        self.sword_textures_right = []
        self.width = width 
        self.height = height
        self.animation_counter = 0
        self.slow_counter = 0 
        self.direction = direction #направление
        for name in self.textures: #пробегаемя по каждому названию текстурки
            pic = image.load(name)
            pic = transform.scale(pic, (self.width, self.height)) #изменяем размеры картинки
            self.textures_left.append(pic) #добавляем в список self.textures_left загруженную картинку (пока повернута в лево)
            pic_right = transform.flip(pic, 1, 0)
            self.textures_right.append(pic_right) #добавляем в self.textures_right развернутую картинку
        for name in self.sword_textures:
            pic = image.load(name)
            pic = transform.scale(pic, (self.width*1.20, self.height))
            self.sword_textures_left.append(pic)
            pic_right = transform.flip(pic, 1,0)
            self.sword_textures_right.append(pic_right)
        self.x = x
        self.y = y
        self.picture = self.textures_right[0]
        self.room = room
        self.mask_left = pygame.mask.from_surface(self.textures_left[0])
        self.mask_right = pygame.mask.from_surface(self.textures_right[0])
        self.mask = self.mask_left
        self.atack_flag = False
        self.atack_counter = 0

    def collision(self, newx, newy, any_key): #обработка столкновений
        can_move_x = True
        can_move_y = True
        for obj in self.room.objects: #проверяем объекты в комнате
            offset_x = obj.x - self.x
            offset_y = obj.y - newy
            if self.mask_left.overlap_area(obj.mask, (offset_x, offset_y))>0: #если пересечение наей маски и маски объекта больше 0
                can_move_y = False #флаг опускается дальше нельзя идти(вверх, вниз)
                break
        for obj in self.room.objects:
            offset_x = obj.x - newx
            offset_y = obj.y - self.y
            if self.mask_left.overlap_area(obj.mask, (offset_x, offset_y))>0:
                can_move_x = False
                break
        
        for obj in self.room.walls: #проверяем объекты в комнате
            offset_x = obj.x - self.x
            offset_y = obj.y - newy
            if self.mask_left.overlap_area(obj.mask, (offset_x, offset_y))>0: #если пересечение наей маски и маски объекта больше 0
                can_move_y = False #флаг опускается дальше нельзя идти(вверх, вниз)
                break
        for obj in self.room.walls:
            offset_x = obj.x - newx
            offset_y = obj.y - self.y
            if self.mask_left.overlap_area(obj.mask, (offset_x, offset_y))>0:
                can_move_x = False
                break
        for tower in self.room.towers:
            offset_x = tower.x - self.x
            offset_y = tower.y - newy
            if self.mask_left.overlap_area(tower.mask, (offset_x, offset_y))>0: #если пересечение наей маски и маски объекта больше 0
                can_move_y = False #флаг опускается дальше нельзя идти(вверх, вниз)
                break
        for tower in self.room.towers:
            offset_x = tower.x - newx
            offset_y = tower.y - self.y
            if self.mask_left.overlap_area(tower.mask, (offset_x, offset_y))>0:
                can_move_x = False
                break
        for door in self.room.doors:
            offset_x = door.x - self.x
            offset_y = door.y - self.y
            if self.mask_left.overlap_area(door.mask, (offset_x, offset_y))>0:
                if door.nextroom == 1:
                    self.room = testroom
                if door.nextroom == 2:
                    self.room = testroom2
                if door.nextroom == 3:
                    self.x = 0
                    self.y = 0
                    self.room = testroom3
                self.x = door.newx
                self.y = door.newy
                self.controls()
                print(door.newx, door.newy)
        
        for chest in self.room.chests:
            offset_x = chest.x - self.x
            offset_y = chest.y - self.y
            if self.mask_left.overlap_area(chest.mask, (offset_x, offset_y))>0:
                if any_key[K_e]:
                    chest.status = 'open'


        if newx <= 0:
            can_move_x = False
        if newy <= 0:
            can_move_y = False
        if newx >= 700-self.width:
            can_move_x = False
        if newy >= 500-self.height:
            can_move_y = False
        return can_move_x, can_move_y

    
    def show(self):
        if self.atack_flag == True:
            self.atack_animation()
        window.blit(self.picture, (self.x, self.y,))
        self.atack()

    def animation(self):
        if self.direction == 'left':
            self.picture = self.textures_left[self.animation_counter]
            if self.slow_counter == 5: #замедлитель
                self.animation_counter += 1
                self.slow_counter = 0
            else:
                self.slow_counter += 1
        if self.direction == 'right':
            self.picture = self.textures_right[self.animation_counter]
            if self.slow_counter == 5:
                self.animation_counter += 1
                self.slow_counter = 0
            else:
                self.slow_counter += 1
        if self.animation_counter == len(self.textures):
            self.animation_counter = 0
    def controls(self):
        newx = self.x #где окажемся по x 
        newy = self.y #где окажемся по y
        any_key = pygame.key.get_pressed()
        button_mouse = pygame.mouse.get_pressed()
        if any_key[K_SPACE] and self.atack_flag == False:
            self.atack_flag = True
        if self.atack_flag == False:
            
            if any_key[K_w]:
                newy -= 5
                self.animation()
            elif any_key[K_s]:
                newy += 5
                self.animation()
            if any_key[K_d]:
                self.direction = 'right'
                newx += 5 
                self.animation()
            elif any_key[K_a]:
                self.direction = 'left'
                newx -= 5
                self.animation()
        can_move_x, can_move_y = self.collision(newx, newy, any_key) #проверяем можем ли идти вверх, вниз и влево, вправо
        if can_move_x == True:
            self.x = newx
        if can_move_y == True:
            self.y = newy
    def atack(self):
        for obj in self.room.objects:
            if isinstance(obj, (Monster, Spider)):
                offset_x = obj.x - self.x
                offset_y = obj.y - self.y
                if self.mask.overlap_area(obj.mask, (offset_x, offset_y))>0:
                    if self.atack_flag == True:
                        if (self.x < obj.x+obj.width/2 and self.direction == 'right') or (self.x > obj.x+obj.width/2 and self.direction == 'left'):
                            obj.hp -= 4
                            if obj.direction == 'left':
                                obj.x += 7
                            if obj.direction == 'right':
                                obj.x -= 7
                            print(obj.hp)
                            if obj.hp < 0:
                                self.room.objects.remove(obj)
                    break

    def atack_animation(self):
        if self.direction == 'left':
            textures = self.sword_textures_left
        if self.direction == 'right':
            textures = self.sword_textures_right
        self.picture = textures[self.atack_counter]
        self.mask = pygame.mask.from_surface(self.picture)
        self.slow_counter += 1
        if self.slow_counter >= 4:
            self.atack_counter += 1
            self.slow_counter = 0
        if self.atack_counter == 4:
            self.atack_flag = False
            self.animation()
            self.atack_counter = 0
class Floor:
    def __init__(self, picture, width, height, x, y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.picture = image.load(picture)
        self.picture = transform.scale(self.picture, (self.width, self.height))
    def show(self):
        window.blit(self.picture, (self.x, self.y))

class Hp:
    def __init__(self, x, y, height, width, picture_red, picture_green):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.picture_red = image.load(picture_red)
        self.picture_green = image.load(picture_green)
        self.picture_red = transform.scale(self.picture_red, (self.width, self.height))
        self.picture_green = transform.scale(self.picture_green, (self.width, self.height))
    def show(self):
        window.blit(self.picture_red, (self.x, self.y))
        window.blit(self.picture_green, (self.x, self.y))



class Wall:
    def __init__(self, 
                 picture, width, height, x, y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.picture = image.load(picture)
        self.picture = transform.scale(self.picture, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.picture)

    def show(self):
        window.blit(self.picture, (self.x, self.y))

class Door:
    def __init__(self, picture, width, height, x, y, nextroom, newx, newy):
        self.newx = newx
        self.newy = newy
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.picture = image.load(picture)
        self.picture = transform.scale(self.picture, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.picture)
        self.nextroom = nextroom

    def show(self):
        window.blit(self.picture, (self.x, self.y))

class Arrow:
    def __init__(self, picture, width, height, x, y):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.picture = image.load(picture)
        self.picture = transform.scale(self.picture, (self.width, self.height))
        self.picture = transform.rotate(self.picture, 45)
        self.speed = 5
    def show(self):
        window.blit(self.picture, (self.x, self.y))
        self.y -= self.speed

class Tower:
    def __init__(self, width, height, x, y, shoot):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.picture = image.load('tower/башня.png')
        self.picture = transform.scale(self.picture, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.picture)
        self.shoot = shoot
    def fire(self):
        keys = pygame.key.get_pressed()
        if random.randint(0,15) == 1:
            if random.randint(0,15) == 1:

        
                if self.shoot == True:
                    link.room.dekoration.append(Arrow(width=100, height=100, x=self.x+40, y=self.y, picture='стрела.png'))

    def show(self):
        window.blit(self.picture, (self.x, self.y))


class Chest:
    def __init__(self, picture, width, height, x, y, picture_close, status, picture_gold):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.picture_close = image.load(picture_close)
        self.picture_close = transform.scale(self.picture_close, (self.width, self.height))
        self.picture_gold = image.load(picture_gold)
        self.picture_gold = transform.scale(self.picture_gold, (self.width, self.height))
        self.status = status
        self.picture = image.load(picture)
        self.picture = transform.scale(self.picture, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.picture)

    def show(self):
        if self.status == 'open':
            window.blit(self.picture, (self.x, self.y))
        if self.status == 'close':
            window.blit(self.picture_close, (self.x, self.y))
        if self.status == 'gold':
            window.blit(self.picture_gold, (self.x, self.y))
        

class Room:
    def __init__(self, room_map, objects, doors, chests, dekoration,):
        self.doors = doors
        self.dekoration = dekoration
        self.objects = objects
        self.room_map = room_map
        self.floors = []
        self.walls = []
        self.towers = []
        self.arrows = []
        self.chests = chests

    def show(self):
        for floor in self.floors:
            floor.show()
        for doors in self.doors:
            doors.show()
        for chests in self.chests:
            chests.show()
        for walls in self.walls:
            walls.show()
        link.show()
        for obj in self.objects:
            obj.show()
        for towers in self.towers:
            towers.show()
        for dekoration in self.dekoration:
            dekoration.show()



    def build(self):
        with open(self.room_map,'r') as file:
            lines = file.readlines()
            y = 0
            for line in lines:
                line = line.rstrip('\n')
                line = line.split(',')
                x = 0
                for symbol in line:
                    if symbol == '1':
                        self.floors.append(Floor(x=x, y=y, height=50, width=50, picture='floor/dirt_1.png'))
                    elif symbol == '2':
                        self.walls.append(Wall(x=x, y=y ,height=50, width=50, picture='floor/dirt_7.png'))
                    elif symbol == '3':
                        self.floors.append(Floor(x=x, y=y, height=50, width=50, picture='floor/dirt_8.png'))
                    elif symbol == '4':
                        self.walls.append(Wall(x=x, y=y, height=50, width=50, picture='floor/wall.png'))
                    elif symbol == '5':
                        self.floors.append(Floor(x=x, y=y,height=100, width=100, picture='floor/floorr.jpg'))
                    elif symbol == '6':
                        self.floors.append(Tower(x=x, y=y, height=110, width=80))
                    x += 50
                y += 50


link_textures = [
    'zelda_go_1.png',
    'zelda_go_2.png',
    'zelda_go_3.png',
    'zelda_go_4.png',
    'zelda_go.png',
]

link_textures_sword = [
    'zelda_sword_1.png',
    'zelda_sword_2.png',
    'zelda_sword_3.png',
    'zelda_sword_4.png',
]

#создаем противников
spider = Spider(textures_stand=spider_stand, textures_walk=spider_walk, textures_jump=spider_jump, textures_attack=spider_attack, x=100, y=100, direction='left', hp=800, speed=1)
monster1 = Monster(textures=monsters, x=600, y=300, direction='left', hp=100, aktiv_zone_high=100, aktiv_zone_width=100, speed=1)
monster2 = Monster(textures=monsters, x=10, y=350, direction='left', hp=100, aktiv_zone_high=100, aktiv_zone_width=100, speed=2)
monster3 = Monster(textures=monsters, x=600, y=30, direction='left', hp=100, aktiv_zone_high=100, aktiv_zone_width=100, speed=1)
#двери
door = Door(picture='door/dd31cc050e0f4a51cc516c24bb792899U7hZdRHEiVh2Z38U-0.png', width=60, height=80, x=5, y=5, nextroom=2, newx=50, newy=50)
door2 = Door(picture='door/dd31cc050e0f4a51cc516c24bb792899U7hZdRHEiVh2Z38U-0.png', width=60, height=80, x=600, y=400, nextroom=1, newx=50, newy=50)
door3 = Door(picture='door/dd31cc050e0f4a51cc516c24bb792899U7hZdRHEiVh2Z38U-0.png', width=60, height=80, x=10, y=400, nextroom=3, newx=400, newy=350)
#создаем сундуки
testchest = Chest(picture='chest_empty.png', width=40, height=60, x=550, y=0, picture_close='chest_lock.png', status='close', picture_gold='chest_gold.png')
testchest2 = Chest(picture='chest_empty.png', width=40, height=60, x=300, y=450, picture_close='chest_lock.png', status='gold', picture_gold='chest_gold.png')
testchest3 = Chest(picture='chest_empty.png', width=40 ,height=60, x=300, y=450, picture_close='chest_lock.png', status='gold',picture_gold='chest_gold.png')
#факел
torch1 = Torch(textures=torch_images, x=0, y=-25)
torch2 = Torch(textures=torch_images, x=630, y=-25)
torch3 = Torch(textures=torch_images, x=0, y=385)
torch4 = Torch(textures=torch_images, x=630, y=385)
arrow = Arrow(width=100, height=100, x=200, y=200, picture='стрела.png')
#создаем комнаты
testroom = Room(objects=[monster1, monster2], room_map='map.txt', doors = [door], chests=[testchest, testchest2], dekoration=[])
testroom.build()
testroom2 = Room(objects=[monster3], room_map='map2.txt', doors =[door2, door3], chests=[testchest3], dekoration=[])
testroom2.build()
testroom3 = Room(objects=[spider], room_map='map3.txt', doors =[], chests=[], dekoration=[torch1, torch2, torch3, torch4, arrow])
testroom3.build()
#создаем персонажа
link = Player(picture='zelda_go_1.png', width=70, height=70, x=200, y=200, textures=link_textures, direction='right', room=testroom, 
              sword_textures=link_textures_sword)
#башня
koords = [(0,10),(70,10),(140,10), (210,10), (280,10), (350,10),(420,10), (490,10), (560,10), (560,430), (630,10), (630,80), (630,150), (630,220), (630,290), (630,360), (630,430),
          (0,80), (0,150), (0,220), (0,290), (0,360)]
koords_shoot = [(0,430), (70,430), (140,430), (210,430), (280,430), (350,430), (420,430), (490,430)]

for x,y in koords:
    tower = Tower(height=110, width=80, x=x-6, y=y-15, shoot = False)
    testroom3.walls.append(tower)
for x,y in koords_shoot:
    tower = Tower(height=110, width=80, x=x-6, y=y-15, shoot = True)
    testroom3.towers.append(tower)





while True:
    #здесь заканчивается загрузка и начинается игра
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    link.room.show()
    link.controls()
    link.collision(newx=link.x, newy=link.y, any_key=pygame.key.get_pressed())
    for tower in link.room.towers:
        pass
        #tower.fire()
    display.update()
    timer.tick(60)
#! Доделать стреры вылет из башен, запуск Q

