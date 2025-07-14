from enum import Enum
from threading import Lock
from abc import ABC, abstractmethod
from datetime import date
from typing import Dict
import uuid

class RoomStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    OCCUPIED = "OCCUPIED"

class RoomType(Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    DELUXE = "DELUXE"
    SUITE = "SUITE"

class ReservationStatus(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELED = "CANCELED"

class Payment(ABC):
    @abstractmethod
    def processPayment(self, amount) -> bool:
        pass

class CashPayment(Payment):
    def processPayment(self, amount) -> bool:
        return True
    
class CardPayment(Payment):
    def processPayment(self, amount) -> bool:
        return True
    
class Room:
    def __init__(self, id, type, price):
        self.id = id
        self.type = type
        self.price = price
        self.status = RoomStatus.AVAILABLE
        self.lock = Lock()

    def bookRoom(self):
        with self.lock:
            if(self.status == RoomStatus.AVAILABLE):
                self.status = RoomStatus.BOOKED
            else:
                raise ValueError("Room is not available for booking")
    
    def checkIn(self):
        with self.lock:
            if(self.status == RoomStatus.BOOKED):
                self.status = RoomStatus.OCCUPIED
            else:
                raise ValueError("Room is not booked!")
    
    def checkOut(self):
        with self.lock:
            if(self.status == RoomStatus.OCCUPIED):
                self.status = RoomStatus.AVAILABLE
            else:
                raise ValueError("Room is not occupied!")

class Reservation:
    def __init__(self, id, guest, room, checkInDate, checkOutDate):
        self.id = id
        self.guest = guest
        self.room = room
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
        self.status = ReservationStatus.CONFIRMED
        self.lock = Lock()

    def cancelReservation(self):
        with self.lock:
            if(self.status == ReservationStatus.CONFIRMED):
                self.status = ReservationStatus.CANCELED
            else:
                raise ValueError("Reservation is not confirmed!")

class Guest:
    def __init__(self, id, name, email, phoneNumber):
        self._id = id
        self._name = name
        self._email = email
        self._phoneNumber = phoneNumber

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phoneNumber(self):
        return self._phoneNumber

class HotelManagementSystem:
    def __init__(self):
        self.guests = {}
        self.rooms = {}
        self.reservations = {}
        self.lock = Lock()

    def addGuest(self, guest: Guest):
        self.guests[guest.id] = guest
    
    def getGuest(self, guestId):
        return self.guests.get(guestId, None)
    
    def addRoom(self, room: Room):
        self.rooms[room.id] = room
    
    def getRoom(self, roomId):
        return self.rooms.get(roomId, None)
    
    def bookRoom(self, guest: Guest, room: Room, checkInDate, checkOutDate):
        with self.lock:
            if(room.status == RoomStatus.AVAILABLE):
                room.bookRoom()
                reservationId = self.generateReservationId()
                reservation = Reservation(reservationId, guest, room, checkInDate, checkOutDate)
                self.reservations[reservationId] = reservation
                return reservation
            return None

    def cancelReservation(self, resId):
        with self.lock:
            reservation = self.reservations.get(resId, None)
            if(reservation):
                reservation.cancelReservation()
                del self.reservations[resId]

    def checkIn(self, resId):
        with self.lock:
            reservation = self.reservations.get(resId, None)
            if(reservation and reservation.status == ReservationStatus.CONFIRMED):
                reservation.room.checkIn()
            else:
                raise ValueError("Invalid reservation or reservation not confirmed!")

    def checkOut(self, resId, payment: Payment):
        with self.lock:
            reservation = self.reservations.get(resId, None)
            if(reservation and reservation.status == ReservationStatus.CONFIRMED):
                room = reservation.room
                amount = room.price * (reservation.checkOutDate - reservation.checkInDate).days
                if(payment.processPayment(amount)):
                    room.checkOut()
                    del self.reservations[resId]
                else:
                    raise ValueError("Payment Failed!")
            else:
                raise ValueError("Invalid reservation or reservation not confirmed!")
        
    def generateReservationId(self):
        return f"RES{uuid.uuid4().hex[:8].upper()}"

hotel = HotelManagementSystem()

guest1 = Guest("G1", "John Doe", "john123@gmail.com", "1234567890")
guest2 = Guest("G2", "Jane Smith", "jane123@gmail.com", "1234567899")
room1 = Room("R1", RoomType.SINGLE, 100)
room2 = Room("R2", RoomType.DOUBLE, 200)

hotel.addGuest(guest1)
hotel.addGuest(guest2)
hotel.addRoom(room1)
hotel.addRoom(room2)

checkInDate = date.today()
checkOutDate = checkInDate.replace(day=checkInDate.day + 3)
res1 = hotel.bookRoom(guest1, room1, checkInDate, checkOutDate)
if(res1):
    print(f"Reservation Created: {res1.id}")
else:
    print("Room not available for booking.")

hotel.checkIn(res1.id)
print(f"Checked in: {res1.id}")

payment = CardPayment()
hotel.checkOut(res1.id, payment)
print(f"Checked out: {res1.id}")

hotel.cancelReservation(res1.id)
print(f"Reservation cancelled: {res1.id}")
