#!/usr/bin/python
# coding:UTF-8

# -------------------------------------------------------------------------------------
#                  A PYTHON SCRIPT FILE TO CRACK ENCRYPTED ZIP FILES
#                BY TERENCE BROADBENT BSc CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import pyfiglet

from termcolor import colored

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
   print("Please run this python script as root...")
   exit()

if len(sys.argv) < 2:
   print("Use the command python3 zip-cracker.py secure.zip...")
   exit()

fileName = sys.argv[1]

if os.path.exists(fileName) == 0:
   print(("File " + fileName + " was not found, did you spell it correctly?..."))
   exit()

filextends = fileName[-3:]

if filextends != "zip":
   print("This is not a .zip file...\n...")
   exit ()

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Create function call for my header display.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def header ():
   os.system("clear")
   ascii_banner = pyfiglet.figlet_format("ZIP CRACKER").upper()
   print((colored(ascii_banner.rstrip("\n"), 'red', attrs=['bold'])))
   print((colored("     BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)     \n", 'yellow', attrs=['bold'])))
   print("Selected filename: " + fileName + "\n")

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

installed = True
checklist = ["usr/bin/fcrackzip", "/usr/bin/hashcat"]

header()
for check in checklist:
   cmd = "locate -i " + check + " > /dev/null"
   checked = os.system(cmd)
   if checked != 0:
      print(("I cannot find " + check + "..."))
      installed = False

if installed == False:
   print("\nInstall the above missing dependencies before you begin...\n")
   exit ()

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : The main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['1']="Dictionary Attack."
menu['2']="Hash Attack."
menu['3']="Brute Force Attack."
menu['4']="Exit."

while True: 
   header()
   options=list(menu.keys())
   options.sort()
   for entry in options: 
      print(entry, menu[entry])
   print(colored("\n[?] Please select an option: ",'green'),end='')
   selection=input()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='1':
      dictionary = "/usr/share/wordlists/rockyou.txt"								#  USER CHANGEABLE LOCATION OF DICTIONARY
      if os.path.exists(dictionary):
         print("\n[+] Crack status : Using dictionary " + dictionary + "...")
      else:
         print("\n[-] Crack status : The identified dictionary on line 121 of this script, was not found!!...\n")
         exit()         
      print("[+] Crack status : Using words in dictionary as password, please wait...")   
      os.system("fcrackzip -v -D -u -p " + dictionary + " '" + fileName + "' > F1.tmp")
      os.system("awk '/pw ==/{print $NF}' F1.tmp > F2.tmp")      
      password = open("F2.tmp").readline().rstrip()
      if password != "":	    
         print(colored("\n[!] Found password '" + password + "'\n",'green'))
      else:
         print("[-] Crack status  : Dictionary exhausted...\n")         
      os.system("rm *.tmp")
      exit ()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   elif selection == '2':
      if not os.path.exists("/usr/sbin/zip2john"):								# USER CHANGEABLE LOCATION OF ZIP2JOHN
         print("\n[-] Crack status : The identified file on line 147 of this script, was not found!!...")	
         exit()         
      os.system("zip2john '" + fileName + "' > F1.tmp 2>&1")
      os.system("sed -i '1d' F1.tmp")
      os.system("sed -i 's/" + fileName + "://g' F1.tmp")      
      hashdata = open("F1.tmp").readline().rstrip()
      print("\n[+] Crack status : Hash extracted " + hashdata[:55] + "...")      
      print("[+] Crack status : Comparing hash values, please wait...")
      os.system("john F1.tmp --pot=F2.tmp > F3.tmp 2>&1")     
      password = open("F2.tmp").readline()
      null,hashpass =  password.split(':')
      if password != "":
         print(colored("\n[!] Found password '" + hashpass.rstrip("\n") + "'\n",'green'))
      else:
         print("Crack status : Hash values exhausted\n")
      os.system("rm *.tmp")
      exit ()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Brute force attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '3':
      print("\n[+] Crack status : Conducting numeric attack first (1-8 characters)...")
      os.system("fcrackzip -c 1 -m zip1 -l 1-8 -u '" + fileName + "' > F1.tmp")
      os.system("awk '/pw ==/{print $NF}' F1.tmp > F2.tmp")      
      password = open("F2.tmp").readline().rstrip()
      if password != "":	
         print(colored("\n[!] Found password '" + password + "'\n",'green'))
         os.system("rm *.tmp")
         exit()
      else:
         print("[-] Crack status : Numeric bruteforce exhausted...")
      print("[+] Crack status : Now trying alphanumeric (1-8 characters)...")
      os.system("fcrackzip -m zip1 -l 1-8 -u '" + fileName + "' > F1.tmp")
      os.system("awk '/pw ==/{print $NF}' F1.tmp > F2.tmp")
      password = open("F2.tmp").readline().rstrip()         
      if password != "":	   
         print(colored("\n[!] Found password '" + password + "'\n",'green'))
      else:
         print("[-] Crack status : Alphanumeric bruteforce exhausted...\n")
      os.system("rm *.tmp")
      exit()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '4': 
      print("\n")
      quit()
      
# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

   else:
      pass

#Eof
