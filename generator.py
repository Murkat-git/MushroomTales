import pytmx
import pygame
import random
import math
from copy import deepcopy
from pytmx.util_pygame import load_pygame

MIN_DIST = 5
MAX_DIST = 10


class Room:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.layers = dict()
        self.connectors = []
        self.rect = None

    def set_rect(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect

    def add_connector(self, x, y):
        self.connectors.append((x, y))

    def get_connectors(self):
        return self.connectors

    def set(self, layer, x, y, gid):
        if layer not in self.layers:
            self.layers[layer] = [[0] * self.width for _ in range(self.height)]

        self.layers[layer][y][x] = gid

    def get(self):
        return self.layers


def find_nearest_connector_tiles(room1: Room, room2: Room):
    mind_dist = math.inf
    offset1 = room1.get_rect().topleft
    offset2 = room2.get_rect().topleft
    print(offset1, offset2)
    coords_of_tiles = [(None, None), (None, None)]
    for x1, y1 in room1.get_connectors():
        for x2, y2 in room2.get_connectors():
            coords1 = (x1 + offset1[0], y1 + offset1[1])
            coords2 = (x2 + offset2[0], y2 + offset2[1])
            if mind_dist > math.dist(coords1, coords2):
                mind_dist = math.dist(coords1, coords2)
                coords_of_tiles = [coords1, coords2]
    print(coords_of_tiles)
    return coords_of_tiles


class Generator:
    def __init__(self, path):
        self.tmx_data = load_pygame(path)

        print(self.tmx_data.layernames)

        floor_layer_ind = 0
        connections_layer_ind = 1
        self.floor_layer = self.tmx_data.layers[floor_layer_ind]
        self.connections_layer = self.tmx_data.layers[connections_layer_ind]
        self.filler_tile = self.tmx_data.get_tile_gid(0, 0, floor_layer_ind)
        self.bridge_tile = self.tmx_data.get_tile_gid(1, 0, floor_layer_ind)
        self.land_tile = self.tmx_data.get_tile_gid(2, 0, floor_layer_ind)
        self.stop_tile = self.tmx_data.get_tile_gid(3, 0, floor_layer_ind)
        self.connector = self.tmx_data.get_tile_gid(4, 0, floor_layer_ind)

        self.layouts_of_rooms = self.cut_rooms()

    def generate(self, num_rooms):
        self.clear_map()
        self.fill_map()

        rooms = []
        connections = []
        while len(rooms) < num_rooms:
            room = deepcopy(random.choice(self.layouts_of_rooms))
            if len(rooms) == 0:
                x = random.randint(0, self.tmx_data.width - room.width)
                y = random.randint(0, self.tmx_data.height - room.height)
            else:
                random_room = random.choice(rooms)
                distance = random.randint(MIN_DIST, MAX_DIST)
                point_x, point_y = random_room.get_rect().center
                a = random_room.get_rect().width / 2
                b = random_room.get_rect().height / 2
                theta = random.uniform(0, 2 * math.pi)
                x = int(point_x + a * math.cos(theta) + distance * math.cos(theta))
                y = int(point_y + b * math.sin(theta) + distance * math.sin(theta))

                if x < 0 or y < 0 or x + room.width >= self.tmx_data.width or y + room.height >= self.tmx_data.height:
                    continue

            room.set_rect(pygame.Rect(x, y, room.width, room.height))

            intersects = False
            for other_room in rooms:
                if room.get_rect().colliderect(other_room.get_rect()):
                    intersects = True
                    break
            if not intersects:
                if len(rooms) == 0:
                    self.place_room(room)
                    rooms.append(room)
                    continue
                room_tile, previous_room_tile = find_nearest_connector_tiles(room, random_room)
                start_x, start_y = room_tile
                end_x, end_y = previous_room_tile

                path = self.connect_rooms(rooms, connections, start_x, start_y, end_x, end_y)
                if path:
                    self.place_room(room)
                    connections.append(path)
                    rooms.append(room)
                # else:
                #     print("oops")

        for i in connections:
            for x, y in i:
                self.connections_layer.data[y][x] = self.bridge_tile

        return self.tmx_data

    def place_room(self, room):
        offset_x = room.get_rect().x
        offset_y = room.get_rect().y
        for layer_name, tiles in room.get().items():
            layer = self.tmx_data.get_layer_by_name(layer_name)
            for x in range(room.width):
                for y in range(room.height):
                    layer.data[offset_y + y][offset_x + x] = tiles[y][x]

    def connect_rooms(self, rooms, connections, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x1 > x0 else -1
        sy = 1 if y1 > y0 else -1
        err = dx - dy

        path = []
        while x0 != x1 or y0 != y1:
            for room in rooms:
                if room.get_rect().collidepoint(x0, y0):
                    return False
            for connection in connections:
                for x, y in connection:
                    if x == x0 and y == y0:
                        return False
            path.append((x0, y0))
            e2 = 2 * err
            if e2 > -dx:
                err -= dy
                x0 += sx
            else:
                err += dx
                y0 += sy
        for connection in connections:
            for x, y in connection:
                if x == x0 and y == y0:
                    return False
        path.append((x1, y1))
        return path

    def fill_map(self):
        for x in range(self.floor_layer.width):
            for y in range(self.floor_layer.height):
                self.floor_layer.data[y][x] = self.filler_tile

    def clear_map(self):
        for layer in self.tmx_data.layers:
            if type(layer) != pytmx.TiledTileLayer:
                continue
            for x in range(layer.width):
                for y in range(layer.height):
                    layer.data[y][x] = 0

    def cut_rooms(self):
        tile_size = self.tmx_data.tilewidth
        rooms = []

        for rectangle in self.tmx_data.get_layer_by_name("Rooms"):
            room = Room(int(rectangle.width) // tile_size, int(rectangle.height) // tile_size)
            for layer in self.tmx_data.layers:
                if type(layer) != pytmx.TiledTileLayer:
                    continue
                for x in range(room.width):
                    for y in range(room.height):
                        xx = int(rectangle.x) // tile_size + x
                        yy = int(rectangle.y) // tile_size + y
                        room.set(layer.name, x, y, layer.data[yy][xx])
                        if layer.data[yy][xx] == self.connector:
                            room.add_connector(x, y)
            rooms.append(room)
        return rooms
