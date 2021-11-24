import os,keyboard,time

settings = {
    "userjf" : False,
    "systemjf" : False,
    "dmpfiles" : False,
    "cleanmgrC" : False,
    "cleanmgrD" : False,
    "recyclebin" : False,
    "windowsupdate" : False,
}

def cls():
    os.system("cls")
def cmd(cmd : str):
    os.system(cmd + " > NUL 2>&1")
def clean(path : str):
    cmd(f'forfiles /p {path} /c "cmd /c if @isdir==FALSE (del /q /f /s @file) else (rd /s /q @file)"')

def stt(setting : bool):
    return "#" if setting else " "

def printsettings():
    cls()
    print(f"""
1: [{stt(settings["userjf"])}] user junk files\n
2: [{stt(settings["systemjf"])}] system junk files\n
3: [{stt(settings["dmpfiles"])}] dump files\n
4: [{stt(settings["cleanmgrC"])}] cleanmgr (C:)\n
5: [{stt(settings["cleanmgrD"])}] cleanmgr (D:)\n
6: [{stt(settings["recyclebin"])}] recycle bin\n
7: [{stt(settings["windowsupdate"])}] windows update\n
    """)
def onkeypress(event : keyboard.KeyboardEvent):
    inp = event.name
    cur = None
    if inp == "1":
        cur = "userjf"
    elif inp == "2":
        cur = "systemjf"
    elif inp == "3":
        cur = "dmpfiles"
    elif inp == "4":
        cur = "cleanmgrC"
    elif inp == "5":
        cur = "cleanmgrD"
    elif inp == "6":
        cur = "recyclebin"
    elif inp == "7":
        cur = "windowsupdate"
    elif inp == "enter":
        if not ("True" in str(settings)):
            printsettings()
            print("error: you must have atleast one selected")
            return
        else:
            keyboard.unhook_all()
            cls()
            initiate()
            return
    else:
        return
    settings[cur] = not settings[cur]
    printsettings()
def initiate():
    if settings["userjf"]:
        print("removing user junk files")
        clean("%tmp%")
        print()
    if settings["systemjf"]:
        print("removing system junk files")
        clean("%windir%\Temp")
        print()
    if settings["dmpfiles"]:
        print("removing dump files")
        cmd("del /q /f /s C:\*.dmp")
        print()
    if settings["cleanmgrC"]:
        print("running cleanmgr (C:)")
        cmd("cleanmgr /d C")
        print()
    if settings["cleanmgrD"]:
        print("running cleanmgr (D:)")
        cmd("cleanmgr /d D")
        print()
    if settings["recyclebin"]:
        print("clearing recycle bin")
        cmd("del /q /f /s C:\$Recycle.Bin\*.*")
        print()
    if settings["windowsupdate"]:
        print("cleaning windows update (stopping wuauserv)")
        cmd("net stop wuauserv")
        print("cleaning windows update (removing softwaredistribution)")
        cmd("rd /s /q %windir%\SoftwareDistribution")
        print("cleaning windows update (clearing servicing\LCU)")
        clean("%windir%\servicing\LCU")
        print("cleaning windows update (cleaning up components with DISM)")
        cmd("dism /Online /Cleanup-Image /StartComponentCleanup /ResetBase")
        cmd("dism /Online /Cleanup-Image /StartComponentCleanup")
    print("done!!!")

printsettings()

keyboard.on_press(onkeypress)

while True:
    time.sleep(60)
