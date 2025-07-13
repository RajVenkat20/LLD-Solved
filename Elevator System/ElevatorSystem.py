from enum import Enum
import time
from threading import Lock, Condition, Thread

class Direction(Enum):
    UP = 1
    DOWN = 2
class Request:
    def __init__(self, srcFloor, desFloor):
        self.srcFloor = srcFloor
        self.desFloor = desFloor

class Elevator:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.requests = []
        self.currFloor = 1
        self.currDirection = Direction.UP
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def addRequest(self, request):
        with self.lock:
            if(len(self.requests) < self.capacity):
                self.requests.append(request)
                print(f"Elevator {self.id} added request: {request.srcFloor} to {request.desFloor}")
                self.condition.notify_all()

    def getNextRequest(self):
        with self.lock:
            while(not self.requests):
                self.condition.wait()
            return self.requests.pop(0)

    def processRequests(self):
        while(self.requests):
            request = self.getNextRequest()
            self.processRequest(request)
        
    def processRequest(self, request: Request):
        startFloor = request.srcFloor
        endFloor = request.desFloor

        if(startFloor < endFloor):
            self.currDirection = Direction.UP
            for i in range(startFloor, endFloor + 1):
                self.currFloor = i
                print(f"Elevator {self.id} reached floor {self.currFloor}")
                time.sleep(1)
            print("\n")
        elif(startFloor > endFloor):
            self.currDirection = Direction.DOWN
            for i in range(startFloor, endFloor - 1, -1):
                self.currFloor = i
                print(f"Elevator {self.id} reached floor {self.currFloor}")
                time.sleep(1)
            print("\n")
        else:
            print("You are already in the desired floor!")

class ElevatorController:
    def __init__(self, numElevators, capacity):
        self.elevators = []
        for i in range(numElevators):
            elevator = Elevator(i + 1, capacity)
            self.elevators.append(elevator)

    def requestElevator(self, srcFloor, desFloor):
        optimalElevator = self.findOptimalElevator(srcFloor, desFloor)
        optimalElevator.addRequest(Request(srcFloor, desFloor))
        optimalElevator.processRequests()

    def findOptimalElevator(self, srcFloor, desFloor):
        optimalElevator = None
        minDistance = float('inf')

        for elevator in self.elevators:
            distance = abs(srcFloor - elevator.currFloor)
            if(distance < minDistance):
                minDistance = distance
                optimalElevator = elevator

        return optimalElevator

controller = ElevatorController(3, 5)
time.sleep(1)
controller.requestElevator(10, 12)
time.sleep(1)
controller.requestElevator(1, 5)
time.sleep(1)
controller.requestElevator(2, 1)
