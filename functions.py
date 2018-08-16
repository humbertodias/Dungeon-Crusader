import pygame as pg
from os import path
import traceback
import xml.etree.ElementTree as ET

import settings as st
import sprites as spr

vec = pg.math.Vector2


def clamp(var, lower, upper):
    # restrains a variable's value between two values
    return max(lower, min(var, upper))


def remap(n, start1, stop1, start2, stop2):
    # https://p5js.org/reference/#/p5/map
    newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
    if (start2 < stop2):
        return clamp(newval, start2, stop2)
    else:
        return clamp(newval, stop2, start2)
    

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, dir_):
    if dir_ == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # hit from left
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.w / 2
            # hit from right
            elif hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.w / 2
                            
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
            
    elif dir_ == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # hit from top
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.h / 2
            # hit from bottom
            elif hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.h / 2
                
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def screenWrap(player, dungeon):
    #checks if the player goes outside the screen
    #if they do, set their new position based on where they went
    index = list(dungeon.room_index)
    direction = ''
    new_pos = vec(player.rect.center)
    if player.rect.left < st.TILESIZE:
        direction = 'LEFT'
        player.vel = vec(0, 0)
        new_pos.x  = st.WIDTH - player.rect.width - st.TILESIZE
        index[1] -= 1
    if player.rect.right > st.WIDTH - st.TILESIZE:
        direction = 'RIGHT'
        player.vel = vec(0, 0)
        new_pos.x = player.hit_rect.width + st.TILESIZE
        index[1] += 1
    if player.rect.top < st.GUI_HEIGHT + st.TILESIZE:
        player.vel = vec(0, 0)
        direction = 'UP'
        new_pos.y = st.HEIGHT - player.hit_rect.height - st.TILESIZE
        index[0] -= 1
    if player.rect.bottom > st.HEIGHT - st.TILESIZE:
        player.vel = vec(0, 0)
        direction = 'DOWN'
        new_pos.y = player.rect.height + st.GUI_HEIGHT + st.TILESIZE
        index[0] += 1
    try:
        return direction, index, new_pos
    except Exception:
        traceback.print_exc()


def transitRoom(game, dungeon):
    # get the index of the next and the previous room
    index_next = dungeon.room_index
    index_prev = game.prev_room
    # select the rooms based on the indices
    room_current = dungeon.rooms[index_prev[0]][index_prev[1]]
    room_next = dungeon.rooms[index_next[0]][index_next[1]]
     
    # remove all sprite from the previous room
    room_current.object_data = []
    for sprite in game.all_sprites:
        if sprite != game.player:
            # store the current objects
            if hasattr(sprite, 'updatData'):
                sprite.updateData()
            if hasattr(sprite, 'data'):
                room_current.object_data.append(sprite.data)
            sprite.kill()
    
    if room_next.visited == False:
        # if room not visited, get the object data from the initial layout
        data = room_next.layout    
        for d in data:
            try:
                spr.create(game, d)
            except Exception:
                traceback.print_exc()
                pass
        
        room_next.visited = True
    
    else:
        # if room already visited, get the objects from the stored data
        data = room_next.object_data    
        for d in data:
            try:
                spr.create(game, d)
            except Exception:
                traceback.print_exc()
                pass
    

def loadImage(filename, scale=st.GLOBAL_SCALE):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'images')
    file = path.join(img_folder, filename)
    try:
        img = pg.image.load(file).convert_alpha()
        width, height = img.get_width(), img.get_height()
        size = (int(width * scale), int(height * scale))
        return pg.transform.scale(img, size)
    except Exception:
        traceback.print_exc()
        return


def img_list_from_strip(filename, width, height, startpos, number, scale=True, 
                        size=st.TILESIZE):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'images')
    file = path.join(img_folder, filename)
    try:
        img = pg.image.load(file).convert_alpha()
    except Exception:
        traceback.print_exc()
        return
    img_set = []
    for i in range(startpos, (startpos + number)):
        rect = ((i * width, 0), (width, height))
        if scale and size == st.TILESIZE:
            subimg = pg.transform.scale(img.subsurface(rect), 
                                        (st.TILESIZE, st.TILESIZE))
        elif scale and size != st.TILESIZE:
            subimg = pg.transform.scale(img.subsurface(rect), 
                                        (size[0] * st.GLOBAL_SCALE, size[1] * 
                                         st.GLOBAL_SCALE))
        else:
            subimg = img.subsurface(rect)
        img_set.append(subimg)
    return img_set


def getSubimg(image, width, height, topleft, scale=True):

    rect = (topleft, (width, height))
    if scale:
        subimg = pg.transform.scale(image.subsurface(rect), 
                                    (st.TILESIZE, st.TILESIZE))
    else:
        subimg = image.subsurface(rect)
    return subimg
    

def tileImageScale(filename, size_w, size_h, scale=1, 
                   alpha=False):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'images')
    file = path.join(img_folder, filename)
    try:
        img = pg.image.load(file).convert()
        if alpha:
            color = img.get_at((0,0))
            img.set_colorkey(color)
    except Exception:
        traceback.print_exc()
        return
    
    # size of the tileset
    width, height = img.get_width(), img.get_height()
    tiles_hor = width // size_w
    tiles_vert = height // size_h
    wh_ratio = size_w / size_h
    tileset = []
    for i in range(tiles_vert):
        for j in range(tiles_hor):
            rect = (size_w * j, size_h * i, size_w, size_h)
            subimg = img.subsurface(rect)
            tileset.append(pg.transform.scale(
                    subimg, (int(st.TILESIZE_SMALL * scale * wh_ratio), 
                             int(st.TILESIZE_SMALL * scale))))
    #print(filename, len(tileset))
    return tileset


def tileRoom(game, tileset, index):
    image = pg.Surface((st.WIDTH, st.HEIGHT - st.GUI_HEIGHT))
    data = game.dungeon.rooms[index[0]][index[1]].tiles
    
    for i in range(len(data)):
        for j in range(len(data[i])):
            x = j * st.TILESIZE_SMALL
            y = i * st.TILESIZE_SMALL
            try:
                image.blit(tileset[data[i][j]], (x, y))
            except Exception:
                traceback.print_exc()
                return
    return image


def compare(str1, str2):
    # checks if two strings contain the same letters, but in any order
    if len(str1) != len(str2):
        return False
    
    str_temp1 = str1
    str_temp2 = str2
    for s in str1:
        if s not in str_temp2:
            return False
        else:
           str_temp2 = str_temp2.replace(s, '', 1)

    for s in str2:
        if s not in str_temp1:
            return False
        else:
           str_temp1 = str_temp1.replace(s, '', 1)
           
    return True


def keyDown(events):
    for event in events:
        if event.type == pg.KEYDOWN:
            return event.key

    
def tileset_from_tmx(filename):
    directory = path.dirname(__file__)
    room_folder = path.join(directory, 'rooms')
    file = path.join(room_folder, filename)

    tree = ET.parse(file)
    root = tree.getroot()
    
    # get csv tile data
    data = root[1][0].text
    
    data = data.replace(' ', '')
    data = data.strip('\n')      
    data = data.split('\n')
    
    array = [line.strip(',').split(',') for line in data]
    
    for i in range(len(array)):
        for j in range(len(array[i])):
            array[i][j] = int(array[i][j]) - 1
    
    return array    


def objects_from_tmx(filename):
    directory = path.dirname(__file__)
    room_folder = path.join(directory, 'rooms')
    file = path.join(room_folder, filename)

    tree = ET.parse(file)
    root = tree.getroot()
    
    # get object data as a list of dictionaries
    objects = [obj.attrib for obj in root.iter('object')]
    for o in objects:
        for key, value in o.items():
            try:
                o[key] = int(value) * st.GLOBAL_SCALE
            except:
                pass
    
    return objects
