import subprocess
import pyautogui as pag
import time
import os
import pytesseract as pyt
import cv2
from datetime import datetime, timedelta


def lclick(x, y):
    pag.mouseDown(x=x, y=y, button="left")
    time.sleep(0.01)
    pag.mouseUp()


def rclick(x, y):
    pag.mouseDown(x=x, y=y, button="right")
    time.sleep(0.01)
    pag.mouseUp(button="right")


def setupfirstbomb(run):
    if run:
        subprocess.run(["/usr/bin/open", "/Applications/Keep Talking and Nobody Explodes.app"])
    time.sleep(1)
    pag.mouseDown(x=700, y=500, button="left")
    pag.mouseUp()
    time.sleep(0.3)
    lclick(850, 320)
    lclick(900, 630)
    time.sleep(10)
    color = pag.screenshot(region=(300, 600, 1, 1)).getpixel((0, 0))[0]
    while color < 100:
        color = pag.screenshot(region=(300, 600, 1, 1)).getpixel((0, 0))[0]
        pass
    time.sleep(2)
    lclick(700, 500)
    return


def setuplog(truncate):
    os.chdir("../../../../../Applications/logs")
    oldlog = open("ktane.log", "r+")
    if truncate:
        oldlog.truncate()
    return oldlog


def setupmodules():
    mods = {"FrontFace": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}, "RearFace": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}}
    for line in bombinfo:
        if " on face " in line:
            line = line[0:-1]
            token = line.split(" ")
            mods[token[8][:-1]][token[11]] = token[5]
    return mods


def setupedgework():
    inedgework = {"Serial": "", "Batteries": 0, "Indicators": {}, "Parallel Port": False}
    for line in bombinfo:
        token = line.split(" ")
        if "Serial Number" in line:
            inedgework["Serial"] = token[7][:-1]
        if "Battery Widget" in line:
            inedgework["Batteries"] = inedgework["Batteries"] + int(token[7][:-1])
        if "Indicator Widget" in line:
            inedgework["Indicators"][token[8]] = token[7]
        if "Port Widget" in line:
            if "Parallel" in line:
                inedgework["Ports"] = True
    return inedgework


def solvemodule(module):
    pag.moveTo(100, 100)
    if module == "ButtonComponent":
        starttime = timedelta(hours=datetime.utcnow().hour, minutes=datetime.utcnow().minute, seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)
        for line in setuplog(0):
            timetoken = line.split(" ")
            if "Round start" in line:
                starttime = timedelta(hours=float(timetoken[2][0:2]), minutes=float(timetoken[2][3:5]), seconds=float(timetoken[2][6:8]), milliseconds=float(timetoken[2][9:13]))
        buttontext = pag.screenshot(region=(635, 430, 155, 75))
        text = pyt.image_to_string(buttontext)
        buttontext.save("bt.png")
        grayed = cv2.imread("bt.png")
        grayed = cv2.cvtColor(grayed, cv2.COLOR_BGR2GRAY)
        grayedtext = pyt.image_to_string(grayed)
        inverted = cv2.bitwise_not(grayed)
        if "HOLD" in (text + grayedtext + pyt.image_to_string(inverted)) and buttontext.getpixel((20, 4))[0] > 200 and buttontext.getpixel((20, 4))[1] < 100 and buttontext.getpixel((20, 4))[2] < 100:
            lclick(710, 470)
            return
        elif "ABORT" in (text + grayedtext + pyt.image_to_string(inverted)) and buttontext.getpixel((20, 4))[2] > 100 and buttontext.getpixel((20, 4))[1] < 100 and buttontext.getpixel((20, 4))[0] < 100:
            pass
        elif "DETONATE" in (text + grayedtext + pyt.image_to_string(inverted)) and edgework["Batteries"] > 1:
            lclick(710, 470)
            return
        elif "FRK" in edgework["Indicators"]:
            if edgework["Indicators"]["FRK"] == "lit" and edgework["Batteries"] > 2:
                lclick(710, 470)
                return
        pag.mouseDown(710, 470)
        time.sleep(1)
        strip = (pag.screenshot(region=(820, 480, 1, 1))).getpixel((0, 0))
        if strip[2] > 200 and strip[0] < 150 and strip[1] < 150:
            while True:
                timer = timedelta(minutes=5) - (timedelta(hours=datetime.utcnow().hour, minutes=datetime.utcnow().minute, seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond) - starttime)
                if "4" in str(timer)[3:7]:
                    time.sleep(0.1)
                    pag.mouseUp()
                    break
        elif strip[0] > 150 and strip[1] > 150 and strip[2] < 100:
            while True:
                timer = timedelta(minutes=5) - (timedelta(hours=datetime.utcnow().hour, minutes=datetime.utcnow().minute, seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond) - starttime)
                if "5" in str(timer)[3:7]:
                    time.sleep(0.1)
                    pag.mouseUp()
                    break
        else:
            while True:
                timer = timedelta(minutes=5) - (timedelta(hours=datetime.utcnow().hour, minutes=datetime.utcnow().minute, seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond) - starttime)
                if "1" in str(timer)[3:7]:
                    time.sleep(0.1)
                    pag.mouseUp()
                    break
    elif module == "KeypadComponent":
        solutions = [["QI", "AT", "LM", "LB", "SP", "HQ", "BC"], ["BE", "QI", "BC", "OC", "OS", "HQ", "U?"], ["CO", "BU", "OC", "XI", "OR", "LM", "OS"], ["S6", "BP", "BT", "SP", "XI", "U?", "SM"], ["TR", "SM", "BT", "CD", "BP", "Q3", "FS"], ["S6", "BE", "PZ", "AE", "TR", "BN", "OM"]]
        blacklist = []
        if os.getcwd() != "/Users/charliebeutter/Desktop/KTANE-TAS-ASSETS":
            os.chdir("../../Users/CharlieBeutter/Desktop/KTANE-TAS-ASSETS")
        onscreen = {}
        correctcolumn = 0
        done = False
        inbreak = False
        for column in solutions:
            inbreak = False
            for symbol in blacklist:
                if symbol in column:
                    inbreak = True
                    break
            if inbreak:
                continue
            breakcount = 0
            foundcount = 0
            for symbol in column:
                test = pag.locateCenterOnScreen(symbol + ".png", confidence=0.85, grayscale=True)
                if test is None:
                    blacklist.append(symbol)
                    breakcount += 1
                    if breakcount == 4:
                        break
                else:
                    foundcount += 1
                    onscreen[symbol] = test
                    if foundcount == 4:
                        done = True
                        correctcolumn = column
                        break
            if done:
                break
        for symbol in correctcolumn:
            if symbol in onscreen:
                pag.mouseDown(onscreen[symbol])
                pag.mouseUp()
    elif module == "WireSetComponent":
        def cut(cwire):
            wireloci = [(735, 375), (740, 400), (730, 430), (740, 460), (745, 490), (740, 520)]
            pag.mouseDown(wireloci[cwire - 1])
            pag.mouseUp()
        wireim = pag.screenshot(region=(650, 345, 180, 200))
        wires = [wireim.getpixel((16, 11)), wireim.getpixel((21, 46)), wireim.getpixel((22, 77)), wireim.getpixel((27, 107)), wireim.getpixel((20, 144)), wireim.getpixel((21, 179))]
        wirecolors = []
        wirepos = []
        for wire in wires:
            if wire[0] > 150 and wire[1] < 100 and wire[2] < 100:
                wirecolors.append("Red")
                wirepos.append(wires.index(wire) + 1)
            if wire[0] > 150 and wire[1] > 150 and wire[2] > 150:
                wirecolors.append("White")
                wirepos.append(wires.index(wire) + 1)
            if wire[0] < 100 and wire[1] < 100 and wire[2] > 150:
                wirecolors.append("Blue")
                wirepos.append(wires.index(wire) + 1)
            if wire[0] > 150 and wire[1] > 150 and wire[2] < 100:
                wirecolors.append("Yellow")
                wirepos.append(wires.index(wire) + 1)
            if wire[0] < 10 and wire[1] < 10 and wire[2] < 10:
                wirecolors.append("Black")
                wirepos.append(wires.index(wire) + 1)
        totalwires = "0"
        for line in setuplog(0):
            token = line.split()
            if "Wires.Count" in line:
                totalwires = token[8]
        if totalwires == "3":
            if "Red" not in wirecolors:
                cut(wirepos[1])
            elif wirecolors[-1] == "White":
                cut(wirepos[-1])
            elif wirecolors.count("Blue") > 1:
                wirecolors.reverse()
                for wire in wirecolors:
                    if wire == "Blue":
                        cut(wirepos[(3 - wirecolors.index(wire)) - 1])
                        return
            else:
                cut(wirepos[-1])
        elif totalwires == "4":
            if wirecolors.count("Red") > 1 and (int(edgework["Serial"][-1]) % 2) == 1:
                wirecolors.reverse()
                for wire in wirecolors:
                    if wire == "Red":
                        cut(wirepos[(4 - wirecolors.index(wire)) - 1])
                        return
            elif wirecolors[-1] == "Yellow" and wirecolors.count("Red") == 0:
                cut(wirepos[0])
            elif wirecolors.count("Blue") == 1:
                cut(wirepos[0])
            elif wirecolors.count("Yellow") > 1:
                cut(wirepos[-1])
            else:
                cut(wirepos[1])
        elif totalwires == "5":
            if wirecolors[-1] == "Black" and (int(edgework["Serial"][-1]) % 2) == 1:
                cut(wirepos[3])
            elif wirecolors.count("Red") == 1 and wirecolors.count("Yellow") > 1:
                cut(wirepos[0])
            elif wirecolors.count("Black") == 0:
                cut(wirepos[1])
            else:
                cut(wirepos[0])
        elif totalwires == "6":
            if wirecolors.count("Yellow") == 0 and (int(edgework["Serial"][-1]) % 2) == 1:
                cut(wirepos[2])
            elif wirecolors.count("Yellow") == 1 and wirecolors.count("White") > 1:
                cut(wirepos[3])
            elif wirecolors.count("Red") == 0:
                cut(wirepos[-1])
            else:
                cut(wirepos[3])


def solvefront():
    locations = {}
    for loc in modules["FrontFace"]:
        if modules["FrontFace"][loc] != "EmptyComponent" and modules["FrontFace"][loc] != "TimerComponent":
            locations[loc] = modules["FrontFace"][loc]
    for loc in locations:
        time.sleep(0.4)
        if loc == "0":
            lclick(406, 249)
        elif loc == "1":
            lclick(632, 247)
        elif loc == "2":
            lclick(868, 248)
        elif loc == "3":
            lclick(393, 469)
        elif loc == "4":
            lclick(630, 460)
        elif loc == "5":
            lclick(867, 470)
        solvemodule(modules["FrontFace"][loc])
        mx, my = pag.position()
        rclick(mx, my)


def newbomb(run):
    if run:
        subprocess.run(["/usr/bin/open", "/Applications/Keep Talking and Nobody Explodes.app"])
    time.sleep(1)
    time.sleep(10)
    color = pag.screenshot(region=(300, 600, 1, 1)).getpixel((0, 0))[0]
    while color < 100:
        color = pag.screenshot(region=(300, 600, 1, 1)).getpixel((0, 0))[0]
        pass
    time.sleep(2)
    lclick(700, 500)
    return


log = setuplog(1)
setupfirstbomb(1)
bombinfo = log.readlines()[1:]
modules = setupmodules()
edgework = setupedgework()
os.chdir("../../Users/CharlieBeutter/Desktop/KTANE-TAS-ASSETS")
solvefront()
time.sleep(12)
lclick(750, 590)
lclick(750, 590)
time.sleep(5)
for game in range(0, 1000):
    log = setuplog(1)
    setupfirstbomb(0)
    bombinfo = log.readlines()[1:]
    modules = setupmodules()
    edgework = setupedgework()
    os.chdir("../../Users/CharlieBeutter/Desktop/KTANE-TAS-ASSETS")
    solvefront()
    time.sleep(12)
    lclick(750, 590)
    lclick(750, 590)
    time.sleep(5)
