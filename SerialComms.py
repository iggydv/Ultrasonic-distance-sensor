##
## SerialComms.py
##
## SerialComms - A class for serial communication with an Arduino loaded with the "Controller" sketch (Design E344)
## Updated on 25/08/2015
## Author: R. D. Beyers
##
## This is free software - you may redistribute and modify it freely.
## This software is provided without any warranty
##

import serial
import time

class SerialComms():

    ## Class constructor - automatically called when instantiated
    ## Need to pass the COM port and baudrate as arguments
    ## Example: s = SerialComms('COM6', 19200)
    def __init__(self, COMPort, baudrate):
        self.COMPort = COMPort
        self.baudrate = baudrate
        self.isOpen = False

    ## Method for receiving serial data from the Arduino
    ## Empties the serial buffer into self.buf
    ## Separates messages on newline characters ('\n') and stores all the received messages in an array
    def receive(self):
        self.buf = ''
        messageArray = []
        numCharsRead = 0
        if (self.isOpen):
            while(self.serial.inWaiting() > 0):
                self.buf = self.buf + self.serial.read().decode("ascii")
                numCharsRead += 1
            if (numCharsRead > 0):
                self.buf = self.buf.rstrip('\n')
                messageArray = self.buf.split('\n')
        return messageArray

    ## Sends "message" to the Arduino
    ## Automatically adds a newline character ('\n') to tell the Arduino where the message ends
    def send(self, message):
        self.serial.write(str(message + "\n").encode())

    ## Closes the serial connection
    def close(self):
        self.isOpen = False
        self.serial.close()
        self.setStatusColor("black")
        self.sStatusMain.set("Disconnected")
        self.sConnectText.set("Connect")

    ## Opens the serial connection using the specified COM port and baud rate
    def open(self):
        try:
            self.serial = serial.Serial(self.COMPort, self.baudrate)
            self.isOpen = True
            self.sConnectText.set("Disconnect")
            self.sStatusMain.set("Connected")
            self.sStatusMessage.set("")
            self.setStatusColor("green")
        except serial.SerialException as e:
            self.sStatusMessage.set("Cannot open device")
            self.setStatusColor("red")
        except ValueError as e:
            self.sStatusMessage.set("Invalid Baudrate")
            self.setStatusColor("red")

    ## Sets the COM port
    ## Has no effect on a currently active serial connection, until it is closed and re-opened
    def setCOMPort(self, COMPort):
        self.COMPort = COMPort

    ## Sets the baud rate
    ## Has no effect on a currently active serial connection, until it is closed and re-opened
    def setBaudrate(self, baudrate):
        self.baudrate = baudrate

    def registerConnectionWidget(self,sStatusMain, sStatusMessage, sConnectText, setStatusColor):
        self.sStatusMain = sStatusMain
        self.sStatusMessage = sStatusMessage
        self.sConnectText = sConnectText
        self.setStatusColor = setStatusColor
