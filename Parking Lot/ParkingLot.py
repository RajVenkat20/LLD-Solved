from enum import Enum
import uuid, time
from datetime import datetime

class VehicleType(Enum):
    CAR = 1
    BIKE = 2
    TRUCK = 3

class Vehicle:
    def __init__(self, licensePlate, vehicleType):
        self.licensePlate = licensePlate
        self.vehicleType = vehicleType

class ParkingSlot:
    def __init__(self, slotId, vehicleType):
        self.slotId = slotId
        self.vehicleType = vehicleType
        self.isAvailable = True

class ParkingFloor:
    def __init__(self, floorNumber):
        self.floorNumber = floorNumber
        self.slots = {vtype: [] for vtype in VehicleType}
    
    def addSlot(self, slot):
        self.slots[slot.vehicleType].append(slot)

    def getAvailableSlot(self, vehicleType):
        for slot in self.slots[vehicleType]:
            if(slot.isAvailable):
                return slot
        
        return None

class ParkingLot:
    def __init__(self, name):
        self.name = name
        self.floors = []

    def addFloor(self, floor):
        self.floors.append(floor)

    def parkVehicle(self, vehicle):
        for floor in self.floors:
            slot = floor.getAvailableSlot(vehicle.vehicleType)
            if(slot):
                slot.isAvailable = False
                return Ticket(vehicle, slot)
        
        return None

    def unparkVehicle(self, ticket):
        ticket.slot.isAvailable = True
        return Payment(ticket)

class Ticket:
    def __init__(self, vehicle, slot):
        self.tickedId = str(uuid.uuid4())
        self.issuedAt = datetime.now()
        self.vehicle = vehicle
        self.slot = slot

class Payment:
    def __init__(self, ticket, ratePerHour=10):
        self.ticket = ticket
        self.paidAt = datetime.now()
        self.amount = self._calculateAmount(ratePerHour)

    def _calculateAmount(self, rate):
        duration = self.paidAt - self.ticket.issuedAt
        hours = max(1, int(duration.total_seconds() / 3600))
        return rate * hours
    
lot = ParkingLot("GS")
floor = ParkingFloor(1)

for i in range(2):
    floor.addSlot(ParkingSlot(f"CAR-{i + 1}", VehicleType.CAR))

lot.addFloor(floor)

car = Vehicle("Agent47", VehicleType.CAR)
ticket1 = lot.parkVehicle(car)

if(ticket1):
    # truck = Vehicle("SamRaj1", VehicleType.TRUCK)
    # ticket2 = lot.parkVehicle(truck)

    time.sleep(1)

    payment = lot.unparkVehicle(ticket1)
    # payment = lot.unparkVehicle(ticket2)

    print(f"Vehicle: {ticket1.vehicle.licensePlate} parked at {ticket1.slot.slotId}")
    print(f"Payment: ${payment.amount} for {(payment.paidAt - ticket1.issuedAt).seconds} seconds")

else:
    print("Couldn't park the vehicle!")