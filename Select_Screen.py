from tkinter import *  # Button, Frame, Tk
import tkinter.ttk
from screeninfo import get_monitors  # pip install screeninfo in command line first
import sys
from PIL import ImageTk, Image  # pip install pillow
from screeninfo import get_monitors
import pathlib

rFactor = 1;
gFactor = 1;
bFactor = 1  # default rgb color strength 0-1
global testSelect  # 0: photo 1: gray slope (ramp)
testSelect = 0  # default slect photo

i=0
monitor_num = len(get_monitors())
print(str(monitor_num))
sWidth=[0] * monitor_num
sHeight=[0] * monitor_num
sX = [0] * monitor_num
sY = [0] * monitor_num
win1Canvas = [0] * monitor_num
win = [0] * monitor_num

i = 0
for monitor in get_monitors():  #search for monitor info
    sWidth[i] = monitor.width
    sHeight[i] = monitor.height
    sX[i] = monitor.x               #absolute coordinate X
    sY[i] = monitor.y               #absolute coordinate Y
    win1Canvas[i] = 0
    print(i, str(sWidth[i]) + 'x' + str(sHeight[i]), str(sX[i]) + 'x' + str(sY[i]))
    i+=1
screenQuad = int(sHeight[1] / 4)
screenWidth = sWidth[1]
root = Tk()
# root.iconbitmap(".\\resource\\C3Logo.ico")
x = sWidth[0] - 1400
y = 400
root.geometry("800x400+" + str(x) + "+" + str(y))
root.title("Test Utility")
notebook=tkinter.ttk.Notebook(root, width=280, height=700)
notebook.pack()
notebook.place(x=10, y=0)

tab1 = tkinter.Frame(root)
notebook.add(tab1, text="  Image Color Test  ")
tab2 = tkinter.Frame(root)
notebook.add(tab2, text="  Key 255  ")
tab3 = tkinter.Frame(root)
notebook.add(tab3, text="  liner  ")
tab4 = tkinter.Frame(root)
notebook.add(tab4, text="  Dot  ")
tab5 = tkinter.Frame(root)
notebook.add(tab5, text="  Stripe  ")

canvasWidth = 400
canvasHeight = 250
rootCanvas = Canvas(root, width=canvasWidth, height=canvasHeight, highlightthickness=0)
rootCanvas.pack()
canvasX = 300
canvasY = 50
rootCanvas.place(x=canvasX, y=canvasY)

#
# line = rootCanvas.create_line(2, 2, canvasWidth, 2, fill='black')
# line = rootCanvas.create_line(2, canvasHeight, canvasWidth, canvasHeight, fill='black')
# line = rootCanvas.create_line(2, 2, 2, canvasHeight, fill='black')
# line = rootCanvas.create_line(canvasWidth, 2, canvasWidth, canvasHeight, fill='black')

onWidth = 4
offWidth = 4
xPitch = onWidth + offWidth

win1 = Toplevel()
win1.geometry(f"{screenWidth}x{sHeight[1]}+{sX[1]}+{sY[1]}") # <- shift window right by sWidth[0] of main monitor
win1.overrideredirect(True)
win1.state('zoomed')

# win1.attributes('-fullscreen', True) # make main window full-screen
win1Canvas = Canvas(win1, width=screenWidth, height=sHeight[1], highlightthickness=0)
win1Canvas.pack()
root.focus_set()  # Ensures root window has focus to operate without mouse-click select

counter = IntVar(value=127)
gIncrement = IntVar(value=16)
grayStep = IntVar(value=2)
grayWidth = IntVar(value=4)
colorSelect = 7  # initialize global variable 1(B) 2(G) 4(R) 7(W)
xmin = 0  # xmax=canvasWidth
ymin = 0
canvasQuad = int(canvasHeight / 4)

cPath = pathlib.Path(__file__).parent.resolve()  # current script directory
file = str(cPath) + "\\resource\\PDI_Target.jpg"  # 5040 x 3600
global im
im = Image.open(file).convert('RGB')  # load and separate color


xlineNum = 0
ylineNum = 0
modeXY = 0
modeW = IntVar()
entryXNum = IntVar()
entryYNum = IntVar()
entry2XNum = IntVar()
entry2YNum = IntVar()
modeWS = IntVar()
lineWidthNum = 1

# ************** Functions & Classes ******************
def exitProgram():
    sys.exit(0)


def rgb2hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def grayRamp(sWidth, sQuad, canvasN):
    grayN = 0
    step = grayStep.get()
    width = grayWidth.get()
    r = int(colorSelect / 4)
    g = int(colorSelect / 2) - 2 * r
    b = colorSelect - 4 * r - 2 * g
    for x in range(xmin, sWidth, width):
        if grayN == 0 and step > 1:
            grayN += (step - 1)
        else:
            grayN += step
        if grayN > 255:
            grayN = 0
        gColor = rgb2hex(r * grayN, g * grayN, b * grayN)
        for i in range(x, x + width):
            if canvasN == 0:
                rootCanvas.create_line(i, ymin, i, (2 + 2) * sQuad, fill=gColor)
            else:
                win1Canvas.create_line(i, ymin, i, (2 + 2) * screenQuad, fill=gColor)


def recolorImage(rF, gF, bF):
    global im
    r1, g1, b1 = im.split()
    # color strength 0 - 1
    r1 = r1.point(lambda i: i * rF)
    g1 = g1.point(lambda i: i * gF)
    b1 = b1.point(lambda i: i * bF)
    im = Image.merge('RGB', (r1, g1, b1))
    img = im.resize((canvasWidth, canvasHeight))
    global my_image  # !!!!!!! This is very important. If not declared as global, image does not show !!!!
    my_image = ImageTk.PhotoImage(img)  # capture img as photo by ImageTk
    rootCanvas.create_image(0, 0, image=my_image, anchor=NW)
    img = im.resize((sWidth[1], sHeight[1]))
    global my_image2  # !!!!!!! This is very important. If not declared as global, image does not show !!!!
    my_image2 = ImageTk.PhotoImage(img)  # capture img as photo by ImageTk
    win1Canvas.create_image(0, 0, image=my_image2, anchor=NW)
    counter.set(2)

def gLevelImage(grayN, r, g, b):
    global hexColor
    hexColor = rgb2hex(r * grayN, g * grayN, b * grayN)
    if grayN < 200 or colorSelect == 1:
        textColor = "white"
    else:
        textColor = "black"
    rootCanvas.create_text(canvasWidth/2, canvasHeight/2, text=grayN, fill=textColor, font=('Arial', 14), justify="center")
    win1Canvas.configure(background=hexColor)  # set the colour to the next colour generated
    rootCanvas.configure(bg=hexColor)

def drowLine(grayN, r, g, b, lineWidth):
    global hexColor, xlineNum, ylineNum, modeXY
    rgb2hex(r * grayN, g * grayN, b * grayN)
    if xlineNum > sWidth[1]:
        xlineNum = 0
    elif xlineNum < 0:
        xlineNum = sWidth[1]
    if ylineNum > sHeight[1]:
        ylineNum = 0
    elif ylineNum < 0:
        ylineNum = sHeight[1]
    if modeW.get() == 1:
        bgColor = "white"
        lineColor = "black"
    else:
        bgColor = "black"
        lineColor = "white"
    win1Canvas.configure(background=bgColor)  # set the colour to the next colour generated
    rootCanvas.configure(background=bgColor)  # set the colour to the next colour generated
    if modeXY == 0:
        win1Canvas.create_line(xlineNum, 0, xlineNum, sHeight[1], fill=lineColor, width=lineWidth)
        win1Canvas.create_line(xlineNum+3, 0, xlineNum+3, sHeight[1], fill=lineColor, width=lineWidth)

        rootCanvas.create_text(canvasWidth / 2, canvasHeight / 2, text="X : "+str(xlineNum), fill=lineColor, font=('Arial', 14),
                               justify="center")
    else:
        win1Canvas.create_line(0,ylineNum,  sWidth[1], ylineNum, fill=lineColor, width=lineWidth)
        win1Canvas.create_line(0,ylineNum+3,  sWidth[1], ylineNum+3, fill=lineColor, width=lineWidth)

        rootCanvas.create_text(canvasWidth / 2, canvasHeight / 2, text="Y : "+str(ylineNum), fill=lineColor, font=('Arial', 14),
                               justify="center")

def drowDot(grayN, r, g, b):
    global hexColor, xDotNum, yDotNum
    rgb2hex(r * grayN, g * grayN, b * grayN)
    if xDotNum > sWidth[1]:
        xDotNum = 0
    elif xDotNum < 0:
        xDotNum = sWidth[1]
    if yDotNum > sHeight[1]:
        yDotNum = 0
    elif yDotNum < 0:
        yDotNum = sHeight[1]
    if modeW.get() == 1:
        bgColor = "white"
        dotColor = "black"
    else:
        bgColor = "black"
        dotColor = "white"
    win1Canvas.configure(background=bgColor)  # set the colour to the next colour generated
    rootCanvas.configure(background=bgColor)  # set the colour to the next colour generated
    win1Canvas.create_rectangle(xDotNum, yDotNum, xDotNum+2, yDotNum+2, fill=dotColor)
    rootCanvas.create_text(canvasWidth / 2, canvasHeight / 2, text="X : "+str(xDotNum)+"\nY : "+str(yDotNum), fill=dotColor, font=('Arial', 14),
                           justify="center")
def drowSprite(grayN, r, g, b):
    global hexColor
    rgb2hex(r * grayN, g * grayN, b * grayN)
    if modeWS == 1:
        bgColor = "white"
        lineColor = "black"
    else:
        bgColor = "black"
        lineColor = "white"
    win1Canvas.configure(background=bgColor)  # set the colour to the next colour generated
    rootCanvas.configure(background=bgColor)  # set the colour to the next colour generated
    for i in range(screenWidth):
        if (i < 16):
            continue
        if(screenWidth - 16) < i:
            continue
        if (i % 48) == 0:
            win1Canvas.create_line(i, 0, i, sHeight[1], fill=lineColor, width=1)
    rootCanvas.create_text(canvasWidth / 2, canvasHeight / 2, text="X : stripe", fill=lineColor,
                               font=('Arial', 14),
                               justify="center")



def displayUpdate():
    grayN = counter.get()
    r = int(colorSelect / 4)
    g = int(colorSelect / 2) - 2 * r
    b = colorSelect - 4 * r - 2 * g
    win1Canvas.delete("all")
    rootCanvas.delete("all")
    # column_On_Off_update()
    if testSelect == 0:
        recolorImage(r, g, b)  # pass colorFactors
    elif testSelect == 1:
        grayRamp(canvasWidth, canvasQuad, 0)  # 0 - root
        grayRamp(screenWidth, screenQuad, 1)  # 1 - 2nd screen
    elif testSelect == 2:
        gLevelImage(grayN, r, g, b)
    elif testSelect == 3:
        drowLine(grayN, r, g, b, lineWidthNum)
    elif testSelect == 4:
        drowDot(grayN, r, g, b)
    else:
        drowSprite(grayN, r, g, b)


def onSlopeSelect(event=None):
    gIncrement.set(int((gIncrement.get()) * 2))
    global testSelect
    testSelect = 1  # select slope
    if gIncrement.get() > 256:
        gIncrement.set(1)
    displayUpdate()


def onTestImageSelect(event=None):
    gIncrement.set(int((gIncrement.get()) / 2))
    global testSelect
    testSelect = 0  # select test photo
    if gIncrement.get() < 1:
        gIncrement.set(256)
    displayUpdate()

def onGraylevelSelect(event=None):
    gIncrement.set(int((gIncrement.get()) / 2))
    global testSelect
    testSelect = 2  # select test photo
    if gIncrement.get() < 1:
        gIncrement.set(256)
    displayUpdate()


def onDrowLineSelect(event=None):
    global testSelect, xlineNum, ylineNum, modeXY, linewidth
    testSelect = 3  # select test photo
    xlineNum = 0
    ylineNum = 0
    modeXY = 0
    linewidth = 1
    displayUpdate()

def onDrowLineXSelect(event=None):
    global testSelect, xlineNum, ylineNum, modeXY
    testSelect = 3  # select test photo
    xlineNum = 0
    ylineNum = 0
    modeXY = 0
    displayUpdate()

def onDrowLineYSelect(event=None):
    global testSelect, xlineNum, ylineNum, modeXY
    testSelect = 3  # select test photo
    xlineNum = 0
    ylineNum = 0
    modeXY = 1
    displayUpdate()

def onDrowDotSelect(event=None):
    global testSelect, xDotNum, yDotNum
    testSelect = 4  # select test photo
    xDotNum = 0
    yDotNum = 0
    displayUpdate()


def onDrowStripeSelect(event=None):
    global testSelect, modeWS
    testSelect = 5
    displayUpdate()

def onWhiteStripeMode(event=None):
    global testSelect, modeWS
    testSelect = 5
    displayUpdate()

def onClickInc(event=None):
    gIncrement.set(int((gIncrement.get()) * 2))
    if gIncrement.get() > 256:
        gIncrement.set(1)


def onClickDec(event=None):
    gIncrement.set(int((gIncrement.get()) / 2))
    if gIncrement.get() < 1:
        gIncrement.set(256)


def onClickUp(event=None):
    if counter.get() == 0 and gIncrement.get() > 1:
        counter.set(counter.get() + (gIncrement.get() - 1))
    else:
        counter.set(counter.get() + gIncrement.get())
    if counter.get() > 255:
        counter.set(0)
    displayUpdate()


def onClickDown(event=None):
    if counter.get() > 0 and counter.get() < gIncrement.get():
        counter.set(counter.get() - (gIncrement.get() - 1))
    else:
        counter.set(counter.get() - gIncrement.get())
    if counter.get() < 0:
        counter.set(255)
    displayUpdate()

def onClickUpX(event=None):
    global xlineNum
    if modeXY == 0:
        xlineNum += 1
    displayUpdate()

def onClickDownX(event=None):
    global xlineNum
    if modeXY == 0:
        xlineNum -= 1
    displayUpdate()

def onClickUpY(event=None):
    global ylineNum
    if modeXY == 1:
        ylineNum += 1
    displayUpdate()

def onClickDownY(event=None):
    global ylineNum
    if modeXY == 1:
        ylineNum -= 1
    displayUpdate()



def onWhiteMode(event=None):
    global modeXY
    displayUpdate()

def grayStepInc(event=None):
    grayStep.set(int((grayStep.get()) * 2))
    if grayStep.get() > 64:
        grayStep.set(1)
    displayUpdate()


def grayStepDec(event=None):
    grayStep.set(int((grayStep.get()) / 2))
    if grayStep.get() < 1:
        grayStep.set(64)
    displayUpdate()


def grayWidthInc(event=None):
    grayWidth.set(int((grayWidth.get()) * 2))
    if grayWidth.get() > 64:
        grayWidth.set(1)
    displayUpdate()


def grayWidthDec(event=None):
    grayWidth.set(int((grayWidth.get()) / 2))
    if grayWidth.get() < 1:
        grayWidth.set(64)
    displayUpdate()


class MenuButtons:
    hexColor = "white"

    def __init__(self, master):  # __init__(className, variable)
        # Tab 1 menu
        self.redButton = Button(tab1, text="Red", activebackground='red3', bg='red', fg='white', width=6, height=1,
                                command=self.rStart)
        self.greenButton = Button(tab1, text="Green", activebackground='green', bg='green3', fg='white', width=6,
                                  height=1, command=self.gStart)
        self.blueButton = Button(tab1, text="Blue", activebackground='blue4', bg='blue', fg='white', width=6, height=1,
                                 command=self.bStart)
        self.whiteButton = Button(tab1, text="White", activebackground='gray80', bg='white', fg='black', width=6,
                                  height=1, command=self.wStart)
        self.grayButton = Button(tab1, text="Gray Slope", activebackground='gray64', bg='gray80', fg='black', width=10,
                                 height=1, command=onSlopeSelect)
        self.imageButton = Button(tab1, text="Test Image", activebackground='gray64', bg='gray80', fg='black', width=10,
                                  height=1, command=onTestImageSelect)
        self.keyIndex = Label(tab1, text="Press: r/g/b/w s, t, Esc (Slope, Test Image)", width=40, height=1,
                              justify="left")
        self.instruction = Label(tab1, textvariable=gIncrement, width=5, height=1, justify="center")
        self.zone3Label1 = Label(tab1, text="Gray Step", width=9, height=1, justify="center", font=('Arial', 10))
        self.zone3Label2 = Label(tab1, text="Gray Width", width=9, height=1, justify="center", font=('Arial', 10))
        self.onDownButton3 = Button(tab1, text="-", activebackground='gray64', bg='gray80', fg='black',
                                    command=grayStepDec, font=('Arial', 12))
        self.onColLabel3 = Label(tab1, textvariable=grayStep, width=4, height=1, justify="center", font=('Arial', 10))
        self.onUpButton3 = Button(tab1, text="+", activebackground='gray64', bg='gray80', fg='black',
                                  command=grayStepInc, font=('Arial', 12))
        self.offDownButton3 = Button(tab1, text="-", activebackground='gray64', bg='gray80', fg='black',
                                     command=grayWidthDec, font=('Arial', 12))
        self.offColLabel3 = Label(tab1, textvariable=grayWidth, width=4, height=1, justify="center", font=('Arial', 10))
        self.offUpButton3 = Button(tab1, text="+", activebackground='gray64', bg='gray80', fg='black',
                                   command=grayWidthInc, font=('Arial', 12))
        # Tab 2 Menu
        self.graylevelButton = Button(tab2, text="Gray level""" activebackground='gray64', bg='gray80', fg='black', width=10,
                                 height=1, command=onGraylevelSelect)
        self.button1 = Button(tab2, text="Red", activebackground='red3', bg='red', fg='white', width=6, height=1,
                               command=self.rStart)
        self.button2 = Button(tab2, text="Green", activebackground='green', bg='green3', fg='white', width=6, height=1,
                               command=self.gStart)
        self.button3 = Button(tab2, text="Blue", activebackground='blue4', bg='blue', fg='white', width=6, height=1,
                               command=self.bStart)
        self.button4 = Button(tab2, text="White", activebackground='gray80', bg='white', fg='black', width=6, height=1,
                               command=self.wStart)
        self.upButton = Button(tab2, text="Up", activebackground='gray64', bg='gray80', fg='black', width=5, height=1,
                                command=onClickUp)
        self.downButton = Button(tab2, text="Down", activebackground='gray64', bg='gray80', fg='black', width=5,
                                  height=1, command=onClickDown)
        self.incLabel = Label(tab2, text="Increment", width=8, height=1, justify="center")
        self.keyIndex2 = Label(tab2, text="Press: L, R, G, B, W, Up, Down, Left, Right, Esc", width=40, height=1,
                               justify="left")

        self.plusButton = Button(tab2, text="+", activebackground='gray64', bg='gray80', fg='black', width=3, height=1,
                                  command=onClickInc)
        self.deltaGray = Label(tab2, textvariable=gIncrement, width=5, height=1, justify="center")
        self.minusButton = Button(tab2, text="-", activebackground='gray64', bg='gray80', fg='black', width=3,
                                   height=1, command=onClickDec)
        self.instruction = Label(tab2, textvariable=gIncrement, width=5, height=1, justify="center")

        # Tab3 liner
        self.linerButton = Button(tab3, text="liner", activebackground='gray64', bg='gray80', fg='black', width=10,
                                 height=1, command=onDrowLineSelect)
        self.buttonX = Button(tab3, text="Set X", activebackground='gray64', bg='gray80', fg='black', width=5, height=1,
                                command=onDrowLineXSelect)
        self.buttonY = Button(tab3, text="Set Y", activebackground='gray64', bg='gray80', fg='black', width=5, height=1,
                                command=onDrowLineYSelect)
        self.upButtonY = Button(tab3, text="Y Up", activebackground='gray64', bg='gray80', fg='black', width=5, height=1,
                                command=onClickUpY)
        self.downButtonY = Button(tab3, text="Y Down", activebackground='gray64', bg='gray80', fg='black', width=5,
                                  height=1, command=onClickDownY)
        self.upButtonX = Button(tab3, text="X Up", activebackground='gray64', bg='gray80', fg='black', width=5, height=1,
                                command=onClickUpX)
        self.downButtonX = Button(tab3, text="X Down", activebackground='gray64', bg='gray80', fg='black', width=5,
                                  height=1, command=onClickDownX)
        self.whiteModeButton = Checkbutton(tab3, text="White mode", activebackground='gray64', bg='gray80', fg='black', width=10,
                                  height=1, variable=modeW, command=onWhiteMode)
        self.entryX = Entry(tab3, width = 8, textvariable=entryXNum) # Entry to do
        self.entryY = Entry(tab3, width = 8, textvariable=entryYNum)
        self.lineWidth = Entry(tab3, width = 8 ) #textvariable =entrylineWidth
        self.setButton = Button(tab3, text="Set", activebackground='gray64', bg='gray80', fg='black', width=5,
                                  height=1, command=self.onClickSet)
        # Tab 4
        self.dotButton = Button(tab4, text="  Dot  ", activebackground='gray64', bg='gray80', fg='black', width=10,
                                 height=1, command=onDrowDotSelect)
        self.entryX2 = Entry(tab4, width=8, textvariable=entry2XNum)  # Entry to do
        self.entryY2 = Entry(tab4, width=8, textvariable=entry2YNum)

        # Tab 5
        self.stripeButton = Button(tab5, text="Stripe", activebackground='gray64', bg='gray80', fg='black', width=10,
                                  height=1, command=onDrowStripeSelect)

        dx = 70
        dy = 60
        x0 = 20
        y0 = 60
        y1 = 50
        self.redButton.place(x=x0, y=y0)
        self.greenButton.place(x=x0, y=y0 + dy)
        self.blueButton.place(x=x0, y=y0 + dy * 2)
        self.whiteButton.place(x=x0, y=y0 + dy * 3)
        self.grayButton.place(x=x0 + 110, y=y0)
        self.imageButton.place(x=x0 + 110, y=y0 + dy * 4)
        self.keyIndex.place(x=0, y=10)
        self.zone3Label1.place(x=x0 + 110, y=y0 + dy * 0.7)
        self.onDownButton3.place(x=x0 +95, y=y0 + dy*1.2, width=30, height=30)
        self.onColLabel3.place(x=x0 +135, y=y0 + dy*1.2, width=30, height=30)
        self.onUpButton3.place(x=x0 +175, y=y0 + dy*1.2, width=30, height=30)
        self.zone3Label2.place(x=x0 + 110, y=y0 + dy * 1.7)
        self.offDownButton3.place(x=x0 + 95, y=y0 + dy * 2.2, width=30, height=30)
        self.offColLabel3.place(x=x0 + 135, y=y0 + dy * 2.2, width=30, height=30)
        self.offUpButton3.place(x=x0 + 175, y=y0 + dy * 2.2, width=30, height=30)

        self.graylevelButton.place(x=x0 + 110, y=y0 + dy*0)
        self.button1.place(x=x0, y=y0)
        self.button2.place(x=x0, y=y0 + dy)
        self.button3.place(x=x0, y=y0 + dy * 2)
        self.button4.place(x=x0, y=y0 + dy * 3)
        self.upButton.place(x=150, y=y0 + dy )
        self.downButton.place(x=150, y=y0 + dy * 2)
        self.incLabel.place(x=375, y=y1 + dy * 3.5)
        self.plusButton.place(x=x0 + 95, y=y0 + dy * 3)
        self.deltaGray.place(x=x0 + 130, y=y0 + dy * 3)
        self.minusButton.place(x=x0 + 175, y=y0 + dy * 3)
        self.keyIndex2.place(x=0, y=10)
        y2 = 150
        x2 = screenWidth - 100

        self.linerButton.place(x=x0 + 50, y=y0 + dy*0)
        self.buttonX.place(x=x0, y=y0 + dy)
        self.buttonY.place(x=x0, y=y0 + dy * 2)
        self.upButtonX.place(x=150, y=y0 + dy)
        self.entryX.place(x=x0 + 58, y=y0 + dy)
        self.downButtonX.place(x=150+50, y=y0 + dy)
        self.upButtonY.place(x=150, y=y0 + dy * 2)
        self.entryY.place(x=x0 + 58, y=y0 + dy * 2)
        self.downButtonY.place(x=150 + 50, y=y0 + dy * 2)
        self.whiteModeButton.place(x=150, y=y0 + dy * 3)
        self.lineWidth.place(x=x0 + 58, y=y0 + dy * 3)
        self.setButton.place(x=x0, y=y0 + dy * 3)

        self.dotButton.place(x=x0 + 50, y=y0 + dy*0)
        self.entryX2.place(x=x0 + 58, y=y0 + dy)
        self.entryY2.place(x=x0 + 58, y=y0 + dy * 2)

        self.stripeButton.place(x=x0 + 50, y=y0 + dy * 0)

        master.bind('r', lambda
            event: self.rStart())  # bind the key to lambda function since pressed key value is not used (discarded)
        master.bind('g', lambda event: self.gStart())
        master.bind('b', lambda event: self.bStart())
        master.bind('w', lambda event: self.wStart())
        master.bind('s', lambda event: onSlopeSelect())
        master.bind('t', lambda event: onTestImageSelect())
        master.bind('l', lambda event: onGraylevelSelect())
        master.bind('x', lambda event: onDrowLineXSelect())
        master.bind('y', lambda event: onDrowLineYSelect())
        master.bind('<Right>', lambda event: onClickInc())
        master.bind('<Left>', lambda event: onClickDec())
        master.bind('<Up>', lambda event: onClickUp())
        master.bind('<Down>', lambda event: onClickDown())
        master.bind('<Right>', lambda event: onClickUpX())
        master.bind('<Left>', lambda event: onClickDownX())
        master.bind('<Up>', lambda event: onClickDownY())
        master.bind('<Down>', lambda event: onClickUpY())
        master.bind('<Return>', lambda event: submit())
        master.bind('<Escape>', lambda event: exitProgram())

    def rStart(self):  # alternate: def rStart(iself, _event=None):   # _event=None to prevent warnings
        global colorSelect
        colorSelect = 4
        displayUpdate()

    def gStart(self):
        global colorSelect
        colorSelect = 2
        displayUpdate()

    def bStart(self):
        global colorSelect
        colorSelect = 1
        displayUpdate()

    def wStart(self):
        global colorSelect
        colorSelect = 7
        displayUpdate()

    def onClickSet(self):
        global  lineWidthNum
        # print(str(self.lineWidth.get()))
        lineWidthNum = self.lineWidth.get()
        if int(lineWidthNum) < 1:
            lineWidthNum = 1
        else:
            lineWidthNum = self.lineWidth.get()
        displayUpdate()

    def submit(self):
        global ylineNum, xlineNum, xDotNum, yDotNum, testSelect, lineWidthNum
        if testSelect == 3:
            xlineNum = self.entryX.get()
            ylineNum = self.entryY.get()
            lineWidthNum = self.lineWidth.get()
        else:
            xDotNum = self.entry2X.get()
            yDotNum = self.entry2Y.get()
        displayUpdate()


# ************** Functions End ******************

rootButtons = MenuButtons(root)
displayUpdate()
root.mainloop()