import subprocess
import pyautogui as pag
import time
import os
import pytesseract as pyt
import cv2


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
    time.sleep(0.3)
    pag.mouseUp()
    lclick(700, 300)
    lclick(900, 610)
    time.sleep(15)
    lclick(700, 500)
    time.sleep(0.8)
    return time.monotonic()


def setuplog():
    os.chdir("../../../../../Applications/logs")
    oldlog = open("ktane.log", "r+")
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


def solvemodule(module, loop):
    if module == "ButtonComponent":
        buttontext = pag.screenshot(region=(635, 430, 155, 75))
        text = pyt.image_to_string(buttontext)
        buttontext.save("bt" + str(loop) + ".png")
        grayed = cv2.imread("bt" + str(loop) + ".png")
        grayed = cv2.cvtColor(grayed, cv2.COLOR_BGR2GRAY)
        grayedtext = pyt.image_to_string(grayed)
        inverted = cv2.bitwise_not(grayed)
        print(edgework)
        if "HOLD" in (text + grayedtext + pyt.image_to_string(inverted)) and buttontext.getpixel((20, 4))[0] > 200 and buttontext.getpixel((20, 4))[1] < 100 and buttontext.getpixel((20, 4))[2] < 100:
            lclick(710, 470)
            return
        elif "ABORT" in (text + grayedtext + pyt.image_to_string(inverted)) and buttontext.getpixel((20, 4))[2] > 100 and buttontext.getpixel((20, 4))[1] < 100 and buttontext.getpixel((20, 4))[0] < 100:
            print("nope")
        elif "DETONATE" in (text + grayedtext + pyt.image_to_string(inverted)) and edgework["Batteries"] > 1:
            lclick(710, 470)
            return
        elif "FRK" in edgework["Indicators"]:
            if edgework["Indicators"]["FRK"] == "lit" and edgework["Batteries"] > 2:
                lclick(710, 470)
                print("why god oh why help me please oh god")
                return
        pag.mouseDown(710, 470)
        time.sleep(1)
        strip = (pag.screenshot(region=(820, 480, 1, 1))).getpixel((0, 0))
        print(strip)
        if strip[2] > 200 and strip[0] < 150 and strip[1] < 150:
            print("Strip Blue")
            while True:
                if "4" in str((round(300 - (time.monotonic() - starttime), 0) - (round(300 - (time.monotonic() - starttime), 0)) % 60)/60)[:-1][:-1] + str((round(300 - (time.monotonic() - starttime), 0)) % 60)[:-1][:-1]:
                    print(str((round(300 - (time.monotonic() - starttime), 0) - (round(300 - (time.monotonic() - starttime), 0)) % 60)/60)[:-1][:-1] + str((round(300 - (time.monotonic() - starttime), 0)) % 60)[:-1][:-1])
                    pag.mouseUp()
                    break
        elif strip[0] > 150 and strip[1] > 150 and strip[2] < 100:
            print("Strip Yellow")
            while True:
                if "5" in str((round(300 - (time.monotonic() - starttime), 0) - (round(300 - (time.monotonic() - starttime), 0)) % 60)/60)[:-1][:-1] + str((round(300 - (time.monotonic() - starttime), 0)) % 60)[:-1][:-1]:
                    print(str((round(300 - (time.monotonic() - starttime), 0) - (round(300 - (time.monotonic() - starttime), 0)) % 60)/60)[:-1][:-1] + str((round(300 - (time.monotonic() - starttime), 0)) % 60)[:-1][:-1])
                    pag.mouseUp()
                    break
        else:
            print("Strip Other")
            while True:
                if "1" in str((round(300 - (time.monotonic() - starttime), 0) - (round(300 - (time.monotonic() - starttime), 0)) % 60)/60)[:-1][:-1] + str((round(300 - (time.monotonic() - starttime), 0)) % 60)[:-1][:-1]:
                    print((str((round(300 - (time.monotonic() - starttime), 0) - (round(300 - (time.monotonic() - starttime), 0)) % 60)/60)[:-1][:-1] + str((round(300 - (time.monotonic() - starttime), 0)) % 60)[:-1][:-1]))
                    pag.mouseUp()
                    break


def solvefront(loop):
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
        solvemodule(modules["FrontFace"][loc], loop)
        mx, my = pag.position()
        rclick(mx, my)


log = setuplog()
starttime = setupfirstbomb(1)
bombinfo = log.readlines()[1:]
modules = setupmodules()
edgework = setupedgework()
os.chdir("../../Users/CharlieBeutter/Desktop/TestScreenies")
solvefront(0)
time.sleep(1)
pag.press("esc")
time.sleep(0.7)
lclick(1000, 400)
lclick(1000, 400)
time.sleep(1)
for game in range(0, 1000):
    log = setuplog()
    starttime = setupfirstbomb(1)
    bombinfo = log.readlines()[1:]
    modules = setupmodules()
    edgework = setupedgework()
    os.chdir("../../Users/CharlieBeutter/Desktop/TestScreenies")
    solvefront(game + 1)
    time.sleep(1)
    pag.press("esc")
    time.sleep(0.7)
    lclick(1000, 400)
    lclick(1000, 400)
    time.sleep(1)
