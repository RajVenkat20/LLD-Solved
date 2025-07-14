from enum import Enum
import uuid, time
from datetime import datetime
from abc import ABC

class VehicleType(Enum):
    CAR = 1
    BIKE = 2
    TRUCK = 3

class Vehicle(ABC):
    def __init__(self, licensePlate, vehicleType):
        self.licensePlate= licensePlate
        self.type = vehicleType

    def getType(self):
        return self.type

class Car(Vehicle):
    def __init__(self, licensePlate):
        super().__init__(licensePlate, VehicleType.CAR)

class Bike(Vehicle):
    def __init__(self, licensePlate):
        super().__init__(licensePlate, VehicleType.BIKE)

class Truck(Vehicle):
    def __init__(self, licensePlate):
        super().__init__(licensePlate, VehicleType.TRUCK)

class ParkingSpot:
    def __init__(self, spotNumber):
        self.spotNumber = spotNumber
        self.vehicleType = VehicleType.CAR
        self.parkedVehicle = None

    def isAvailable(self):
        return self.parkedVehicle is None
    
    def parkVehicle(self, vehicle: Vehicle):
        if(self.isAvailable() and vehicle.getType() == self.vehicleType):
            self.parkedVehicle = vehicle
        else:
            raise ValueError("Invalid vehicle type or spot already occupied")

    def unparkVehicle(self):
        self.parkedVehicle = None
    
    def getVehicleType(self):
        return self.vehicleType
    
    def getParkedVehicle(self):
        return self.parkedVehicle
    
    def getSpotNumber(self):
        return self.spotNumber
class Level:
    def __init__(self, floor, numSpots):
        self.floor = floor
        self.parkingSpots = [ParkingSpot(i) for i in range(numSpots)]
    
    def parkVehicle(self, vehicle: Vehicle):
        for spot in self.parkingSpots:
            if(spot.isAvailable() and spot.getVehicleType() == vehicle.getType()):
                spot.parkVehicle(vehicle)
                return True
        return False

    def unparkVehicle(self, vehicle: Vehicle):
        for spot in self.parkingSpots:
            if(not spot.isAvailable() and spot.getParkedVehicle() == vehicle):
                spot.unparkVehicle()
                return True
        return False

    def displayAvailableSpots(self):
        print(f"Level {self.floor} Availability:")
        for spot in self.parkingSpots:
            print(f"Spot {spot.getSpotNumber()}: {'Available' if spot.isAvailable() else 'Occupied'}")
        
class ParkingLot:
    def __init__(self):
        self.levels = []

    def addLevel(self, level: Level):
        self.levels.append(level)
    
    def parkVehicle(self, vehicle: Vehicle):
        for level in self.levels:
            if(level.parkVehicle(vehicle)):
                return True
        return False
    
    def unparkVehicle(self, vehicle: Vehicle):
        for level in self.levels:
            if(level.unparkVehicle(vehicle)):
                return True
        else:
            return False
        
    def displayAvailability(self):
        for level in self.levels:
            level.displayAvailableSpots()
        print()

parkingLot = ParkingLot()
parkingLot.addLevel(Level(1, 2))
parkingLot.addLevel(Level(2, 2))   

car = Car("ABC123")
# truck = Truck("DEF456")
# bike = Bike("GHI789")
car2 = Car("DEF456")

parkingLot.displayAvailability()

parkingLot.parkVehicle(car)
parkingLot.parkVehicle(car2)

parkingLot.displayAvailability()

parkingLot.unparkVehicle(car2)
parkingLot.displayAvailability()

