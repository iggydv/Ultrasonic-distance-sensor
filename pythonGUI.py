##
## pythonGUI.py
##
## pythonGUI - The GUI for out Design E344 project

#Imports
from SerialComms import SerialComms
from tkinter import *
from util import *

#Globals
tk = Tk()
com = SerialComms('COM1', 9600)

#GUI Class
class DistanceSense(Frame):
    #Attributes
    title = "Distance Sense"
    master = None

    p=5

    wSettings=None
    wConnection=None
    wStream=None

    bStream=None

    bQuit=None

    #Constructor
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)

        self.master.title(self.title)
        self.master.resizable(width=False, height=False)

        self.wSettings = LabelFrame(self, text="Settings", padx=self.p, pady=self.p)
        self.wSettings.grid(row=0, column=1, rowspan=2, sticky=W+E+N+S, padx=self.p, pady=self.p)

        self.wConnection = LabelFrame(self, text="Connection", padx=self.p, pady=self.p)
        self.wConnection.grid(row=0, column=0, sticky=W+E+N+S, padx=self.p, pady=self.p)

        self.wStream = LabelFrame(self, text="Stream", padx=self.p, pady=self.p)
        self.wStream.grid(row=1, column=0, sticky=W+E+N+S, padx=self.p, pady=self.p)

        self.createSettingsWidget(self.wSettings)
        self.createConnectionWidget(self.wConnection)
        self.createStreamWidget(self.wStream)

        bQuit = Button(self, text="Quit",command= master.destroy, padx=self.p, pady=self.p)
        bQuit.grid(row=2, column=1, sticky=E+S, padx=self.p, pady=self.p)

        self.pack(padx=self.p, pady=self.p)

    #Create Settings Widget
    def createSettingsWidget(self, widget):
        def _send(msg, lbl="Command sent"):
            updateLabel(lbl)
            com.send(msg)
            Clear_tf()

        def updateLabel(lbl="Command sent"):
            sStatus.set(lbl)
            clearStatus()

        def sendString():
            message = T.get()

            if not com.isOpen:
                updateLabel("Not connected")
            elif message in ['led.green','led.red','led.yellow','led.sensor','led.off',
                            'sensor.on','sensor.off']:
                _send(message)
            elif message == 'stream.on' :
                if(self.bStream['text'] == "Turn Stream On"):
                    self.updateStream()
                    updateLabel()
                else:
                    _send(message)
            elif message == 'stream.off':
                if(self.bStream['text'] == "Turn Stream Off"):
                    self.updateStream()
                    updateLabel()
                else:
                    _send(message)
            elif 'set.green' in message or 'set.red' in message or 'set.yellow' in message:
                _send(message)
            else:
                #Error
                updateLabel("Invalid command")
                pass

            Clear_tf()
            return

        def Clear_tf():
            T.delete(0, END)
            T.insert(0, "")
            return

        def clearStatus():
            nonlocal iCounter
            iCounter = (iCounter + 1) % 3e12

            def _clearStatus(myCounter):
                if(myCounter == iCounter):
                    sStatus.set("")

            widget.after(3000, _clearStatus, iCounter)

        def cal_zero():
            if com.isOpen:
                _send("calibrate.zero", "Calibarting zero")
            else:
                updateLabel("Not connected")
            return

        def cal_one():
            if com.isOpen:
                _send("calibrate.one", "Calibarting one")
            else:
                updateLabel("Not connected")
            return

        sStatus = StringVar("")
        iCounter = 0

        Calibrate_zero = Button(self.wSettings, text = "Calibrate Zero",command = cal_zero)
        Calibrate_one = Button(self.wSettings, text = "Calibrate One",command = cal_one)
        C = Label(widget, text= "Enter Command:")
        T = Entry(self.wSettings)
        Send = Button(self.wSettings, text = "Send", command = sendString)
        lStatus = Label(widget, textvar=sStatus)

        Calibrate_zero.pack(fill=X, padx=self.p, pady=self.p/2)
        Calibrate_one.pack(fill=X, padx=self.p, pady=self.p/2)
        C.pack(fill=X,padx=self.p, pady=self.p/2)
        T.pack(fill=X,padx=self.p, pady=self.p/2)
        Send.pack(fill=X, padx=self.p ,pady=self.p/2)
        lStatus.pack(fill=X, padx=self.p, pady=self.p/2)
        return

    #Create Connection Widget
    def createConnectionWidget(self, widget):
        #Connect on button click
        def fButtonClick():
            #Setup SerialComms
            com.setBaudrate(int(eBaud.get()))
            com.setCOMPort(ePort.get())

            #Connect/Disconnect
            if com.isOpen:
                com.close()
            else:
                com.open()

        def eBaudValidate(text):
            for i in text:
                if not i.isdigit():
                    return False
            return True

        def setStatusColor(c):
            lStatusMain.config(fg=c)

        lPort = Label(widget, text="Serial Port")
        lPort.grid(row=0, column=0, sticky=W, padx=self.p, pady=self.p/2)

        ePort = Entry(widget)
        ePort.insert(END, com.COMPort)
        ePort.grid(row=0, column=1, sticky=W, padx=self.p, pady=self.p/2)

        lBaud = Label(widget, text="Baudrate")
        lBaud.grid(row=1, column=0, sticky=W, padx=self.p, pady=self.p/2)

        eBaud = Entry(widget, validate='key',
                      validatecommand=(widget.register(eBaudValidate), '%S') )
        eBaud.insert(END, com.baudrate)
        eBaud.grid(row=1, column=1, sticky=W, padx=self.p, pady=self.p/2)

        lStatus1 = Label(widget, text="Status")
        lStatus1.grid(row=2, column=0, sticky=W, padx=self.p, pady=self.p/2)

        fStatus = Frame(widget)
        fStatus.grid(row=2, column=1, sticky=W, padx=self.p, pady=self.p/2)

        sStatusMain = StringVar(widget, "Disconnected")
        sStatusMessage = StringVar(widget, "")
        sConnect = StringVar(widget, "Connect")

        lStatusMain = Label(fStatus, textvariable=sStatusMain, font="-size 9 -weight bold")
        lStatusMain.pack(side=LEFT)
        lStatusMessage = Label(fStatus, textvariable=sStatusMessage)
        lStatusMessage.pack(side=LEFT)

        com.registerConnectionWidget(sStatusMain, sStatusMessage, sConnect, setStatusColor)

        fConnect = Frame(widget)
        fConnect.grid(row=3, column=0, columnspan=2, padx=self.p, pady=self.p/2)

        bConnect = Button(fConnect, command=fButtonClick, textvariable=sConnect,
                           )
        bConnect.pack()

        return

    #Create Stream Widget
    def createStreamWidget(self, widget):
        distanceCur=0
        distancePrev=0
        velocity=0
        missingData = 0

        #Get distance measurement from Arduino
        def getDistance():
            nonlocal missingData

            recArray = com.receive()
            if len(recArray) > 0:
                distanceArduino = float(recArray[len(recArray) - 1])
                missingData = 0
            else:
                distanceArduino = -1
                missingData = missingData + 1
            return distanceArduino

        #Update the distance
        def updateDistance():
            nonlocal distancePrev
            nonlocal distanceCur

            distanceArduino = getDistance()
            if distanceArduino != -1:
                distancePrev = distanceCur
                distanceCur = calcAverage(distancePrev, distanceArduino)
                lDistanceValue['text'] = str("{0:06.2f}".format(distanceCur) + " cm")
            return

        #Update the velocity
        def updateVelocity():
            nonlocal velocity
            lVelocityValue['text'] = str("{0:06.2f}".format(velocity) + " km/h")
            return

        #Update the measurements
        def updateMeasurements(call):
            nonlocal distanceCur

            if com.isOpen and bStream['text'] == "Turn Stream Off":
                if call == 1:
                    distanceArduino = getDistance()
                    if distanceArduino != -1:
                        distanceCur = distanceArduino
                        widget.after(100, updateMeasurements, 0)
                    else:
                        widget.after(100, updateMeasurements, 1)
                else:
                    updateDistance()
                    updateVelocity()
                    widget.after(100, updateMeasurements, 0)
            return

        #Turn stream on or off
        def updateStream():
            if com.isOpen:
                if bStream['text'] == "Turn Stream On":
                    bStream['text'] = "Turn Stream Off"
                    com.send('stream.on')
                    widget.after(150, updateMeasurements, 1)
                else:
                    com.send('stream.off')
                    bStream['text'] = "Turn Stream On"
            return

        widget.grid_columnconfigure(0, weight = 1)
        widget.grid_columnconfigure(1, weight = 1)

        lDistance = Label(widget, text= "Distance:")
        lDistance.grid(row=0, column=0, sticky=W, padx=self.p, pady=self.p/2)

        lDistanceValue = Label(widget, text= str("{0:06.2f}".format(distanceCur) + " cm"))
        lDistanceValue.grid(row=0, column=1, sticky=W, padx=self.p, pady=self.p/2)

        lVelocity = Label(widget, text= "Velocity:")
        lVelocity.grid(row=1, column=0, sticky=W, padx=self.p, pady=self.p/2)

        lVelocityValue = Label(widget, text= str("{0:06.2f}".format(velocity) + " km/h"))
        lVelocityValue.grid(row=1, column=1, sticky=W, padx=self.p, pady=self.p/2)

        fStream = Frame(widget)
        fStream.grid(columnspan=2, padx=self.p, pady=self.p/2)

        bStream = Button(fStream, text= "Turn Stream On", command=updateStream)
        bStream.pack()
        self.bStream = bStream
        self.updateStream = updateStream

        return

app = DistanceSense(tk)
app.mainloop()
