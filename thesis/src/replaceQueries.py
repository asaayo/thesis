#  	Author: 		Brandon Trumble
#	Purpose: 		Modify existing codebases that interact with databases
#				to protect them from SQL injection
#	Created: 		9/16/14
#	Last Modified:          10/15/14
#	
#	Changes:		v 0.1: 		Created file
#				v 0.11:		Begin work on replacing unsafe queries
#                               v 0.12:         Continue work on unsafe queries
#

import sys
import fileinput
import shutil

def main():
    print("The purpose of this file is twofold, to update existing queries to make them safer, and to put them through a filter so unsafe queries can be caught.")
    file = raw_input("Enter the file which you would like to modify: ")
    print("File: " + file)
    #We're going to make a copy of the file and only modify the copy
    shutil.copyfile(file, file+"~")
    file = file+"~"
    print(file)
    toMod = ""
    #Loop through the input file and get all the lines where SQL statements occur
    for line in fileinput.input(file, inplace=1):
        print(line)
        if "SELECT" in line:
            toMod += line
            print(toMod)
        if "DELETE" in line:
            toMod += line
            print(toMod)
        if "INSERT" in line:
            toMod += line
            print(toMod)
    print(toMod)

def fixQueries(toMod):
    print("fixQueries")

if __name__ == '__main__':
    main()
