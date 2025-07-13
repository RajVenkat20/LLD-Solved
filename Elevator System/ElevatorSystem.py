from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2

class Request:
    def __init__(self, sourceFloor, destinationFloor):
        self.sourceFloor = sourceFloor
        self.destinationFloor = destinationFloor

class Elevator:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.currFloor = 1
        self.direction = Direction.UP
        self.requests = []
        self.lock = Lock()