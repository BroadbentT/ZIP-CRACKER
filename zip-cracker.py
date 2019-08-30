#!/usr/bin/python
# coding:UTF-8

# -------------------------------------------------------------------------------------
#                  PYTHON UTILITY FILE TO CRACK ENCRYPTED ZIP FILES
#                BY TERENCE BROADBENT BSc CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import fileinput

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
   print "Please run this python script as root..."
   exit(True)

if len(sys.argv) < 2:
   print "Use the command python zip-cracker.py secure.zip..."
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
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

checklist = ["rockyou", "fcrackzip", "hashcat"]
installed = True

for check in checklist:
   cmd = "locate -i " + check + " > /dev/null"
   checked = os.system(cmd)
   if checked != 0:
      print "\n" + check + " is missing..."
      installed = False

if installed == False:
   print "Install missing dependencies before you begin...\n"
   exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Display my universal banner.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def header ():
   os.system("clear")
   print " ________ ____     ____ ____      _    ____ _  _______ __     "
   print "|__  /_ _|  _ \   / ___|  _ \    / \  / ___| |/ / ____|  _ \  "
   print "  / / | || |_) | | |   | |_) |  / _ \| |   | ' /|  _| | |_) | "
   print " / /_ | ||  __/  | |___|  _ <  / ___ \ |___| . \| |___|  _ <  "
   print "/____|___|_|      \____|_| \_\/_/   \_\____|_|\_\_____|_| \_\ "
   print "                                                              "
   print "    BY TERENCE BROADBENT BSc CYBER SECURITY (FIRST CLASS)     "
   print "                                                              "
   print "FILENAME: " + filename + ".\n"

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : The main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['[1].']="Dictionary Attack."
menu['[2].']="Hash Attack."
menu['[3].']="Brute Force Attack."
menu['[4].']="Exit."

while True: 
   header()
   options=menu.keys()
   options.sort()
   for entry in options: 
      print entry, menu[entry]
   selection=raw_input("\nPlease Select: ")
   print ""

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Menu option selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='1':
      print "Crack Selected    : Dictionary attack."
      dictionary = "/usr/share/wordlists/rockyou.txt"		# change as required
      if os.path.isfile(dictionary):
         print "Crack Dictionary  : " + dictionary + "."
      else:
         print "System Error      : Dictionary not found."
         exit(True)
      print "Crack Status      : Cracking file."
      os.system("fcrackzip -v -D -u -p " + dictionary + " " + filename + " > Answer.txt")
      os.system("awk '/pw ==/{print $NF}' Answer.txt > Password.txt")
      password = open("Password.txt").readline().rstrip()
      if password == "":	
         print "Crack Status      : Dictionary exhausted.\n"
      else:      
         print "Cracked Password  : " + password + ".\n"
      os.remove('Answer.txt')
      os.remove('Password.txt')
      exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Menu option selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '2':
      print "Crack Selected    : Hash attack."
      print "Crack Status      : Creating hash."
      os.system("zip2john " + filename + " > hash.txt 2>&1")
      os.system("sed 1d hash.txt > hash2.txt")
      os.remove('hash.txt')
      print "Crack Status      : Comparing hash values."
      os.system("john hash2.txt --pot=pass.txt > dump.txt 2>&1")
      password = open("pass.txt").readline()
      a,b =  password.split(':')
      b = b.replace('\n','')
      if password == "":
         print "Crack Status      : Hash crack exhausted.\n"
      else:
         print "Cracked Password  : " + b + "."
      os.remove('hash2.txt')
      os.remove('dump.txt')
      os.remove('pass.txt')
      exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Menu option selected - Brute force attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '3':
      print "Crack Selected    : Brute force attack (1-8 characters)."
      print "Crack Status      : Conducting numeric attack first."
      os.system("fcrackzip -c 1 -m zip1 -l 1-8 -u " + filename + " > Answer.txt")
      os.system("awk '/pw ==/{print $NF}' Answer.txt > Password.txt")
      password = open("Password.txt").readline().rstrip()
      if password == "":	
         print "Crack Status      : Numeric bruteforce exhausted."
      else:      
         print "Cracked Password  : " + password + ".\n"
      if password == "":
         print "Crack Status      : Now trying alphanumeric."
         os.system("fcrackzip -m zip1 -l 1-8 -u " + filename + " > Answer.txt")
         os.system("awk '/pw ==/{print $NF}' Answer.txt > Password.txt")
         password = open("Password.txt").readline().rstrip()
         if password == "":	
            print "Crack Status      : Alphanumeric bruteforce exhausted.\n"
         else:      
            print "Cracked Password  : " + password + ".\n"
      os.remove('Answer.txt')
      os.remove('Password.txt')
      exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 1.0                                                                
# Details : Menu option selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '4': 
      exit(False)
#Eof
