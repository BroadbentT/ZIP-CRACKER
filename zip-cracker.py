#!/usr/bin/python

# -------------------------------------------------------------------------------------
#                 PYTHON UTILITY FILE TO CRACK ENCRYPTED OFFICE FILES
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Load any required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import fileinput

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Show a universal header.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print "_______ ____     ____ ____      _    ____ _  _______ ____     "
print "|__  /_ _|  _ \   / ___|  _ \    / \  / ___| |/ / ____|  _ \  "
print "  / / | || |_) | | |   | |_) |  / _ \| |   | ' /|  _| | |_) | "
print " / /_ | ||  __/  | |___|  _ <  / ___ \ |___| . \| |___|  _ <  "
print "/____|___|_|      \____|_| \_\/_/   \_\____|_|\_\_____|_| \_\ "
print "                                                              "
print "    BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)     "
print "                                                              "

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "Please run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "Use the command python office-cracker.py microsoft.docx..."
    exit(True)

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "File " + filename + " was not found, did you spell it correctly?..."
    exit(True)

filextends = filename[-3:]

if filextends != "zip":
    print "Incorrect file format...."
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

checklist = ["rockyou.txt", "fcrackzip.list"] #, "hashcat.py"]
installed = True

for check in checklist:
    cmd = "locate " + check + " > /dev/null"
    checked = os.system(cmd)
    if checked != 0:
        print check + " is missing..."
        installed = False

if installed == True:
    print "All required dependencies are pre-installed...\n"
else:
    print "Install missing dependencies before you begin..."
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: The main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['1']="Dictionary Attack."
menu['2']="Hash Attack."
menu['3']="Brute Force Attack."
menu['4']="Exit"

while True: 
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]
    selection=raw_input("Please Select: ") 

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option one selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    if selection =='1':
        print "\nCrack Selected    : Dictionary Attack"
        dictionary = "/usr/share/wordlists/rockyou.txt"
        print "Using Dictionary  : " + dictionary
        os.system("fcrackzip -v -D -u -p " + dictionary + " " + filename + " > Answer.txt")
        os.system("awk '/pw ==/{print $NF}' Answer.txt > Password.txt")
        password = open("Password.txt").readline().rstrip()
        if password == "":	
            print "Crack Status      : Dictionary exhausted...\n"
        else:      
            print "File Password     : " + password
        os.remove('./Answer.txt')
        os.remove('./Password.txt')
        exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option two selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '2':
        print "\nCrack Selected    : Hash Attack"
        print "Crack Status      : Currently unsupported..."
        exit (True)

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option three selected - Brute force attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '3':
        cracked = False
        print "\nCrack Selected    : Brute Force Attack"
        print "Crack Status      : Numeric - please wait..."
        os.system("fcrackzip -c 1 -m zip1 -l 1-8 -u " + filename + " > Answer.txt")
        os.system("awk '/pw ==/{print $NF}' Answer.txt > Password.txt")
        password = open("Password.txt").readline().rstrip()
        if password == "":	
            print "Crack Status      : Numeric bruteforce exhausted...\n"
        else:      
            print "File Password     : " + password
            cracked = True
        os.remove('./Answer.txt')
        os.remove('./Password.txt')
        if cracked == True:
            exit (True)
        else:
            print "Crack Status      : AlphaNumeric - please wait..."
            os.system("fcrackzip -m zip1 -l 1-8 -u " + filename + " > Answer.txt")
            os.system("awk '/pw ==/{print $NF}' Answer.txt > Password.txt")
            password = open("Password.txt").readline().rstrip()
            if password == "":	
                print "Crack Status      : Numeric bruteforce exhausted...\n"
            else:      
                print "File Password     : " + password
            os.remove('./Answer.txt')
            os.remove('./Password.txt')
            exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option three selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '4': 
        break

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

    else:
        print ""

#Eof
