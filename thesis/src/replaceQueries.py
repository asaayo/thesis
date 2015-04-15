# coding=utf-8
#  	Author: 		Brandon Trumble
#	Purpose: 		Modify existing codebases that interact with databases
#				to protect them from SQL injection
#	Created: 		9/16/14
#	Last Modified:          11/03/14
#	
#	Changes:		v 0.1: 		Created file
#				v 0.11:		Begin work on replacing unsafe queries
#                               v 0.12:         Continue work on unsafe queries
#                               v 0.13:         More unsafe query work
#


import sys
import fileinput
import shutil
import re

oldstdout = sys.stdout

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
        if "->prepare" in line:
            print "Prepared statement detected, execution not needed"
            exit(0)
            
        if "SELECT" in line:
            toMod = line
            fix_queries(toMod)
            
        elif "DELETE" in line:
            toMod = line
            fix_queries(toMod)
            
        elif "INSERT" in line:
            toMod = line
            fix_queries(toMod)
        else:
            print line
            
#fix_queries is a function designed to fix unsafe queries in php
#any time a line is detected that contains a SQL command word (INSERT, DELETE, SELECT)
#it is passed into fix_queries
def fix_queries(toMod):
    #Regular expression to find PHP variables
    pattern = re.compile('\$\w+')
    #Return a list of php variables found as an iterator
    #iterator containes a list of match objects
    iter = pattern.finditer(toMod)
    #Returns character location of PHP variable strings
    for i in iter:
        #debug to print the locations of phpvars
        #print i.span()
        #currentWord is the first phpvar token
        #if it's a $mysqli-> statement, we want to let it through
        currentWord = toMod[i.start(0):i.end(0)]
        #debug to check that -> proceeds the first variable
        #print toMod[i.end(0):i.end(0)+2]
        if toMod[i.end(0):i.end(0)+2] == "->":
            #have to use stdout to prevent line from breaking and a space from being appended
            sys.stdout.write("$stmt = " + currentWord)
            #if a string is followed by ->, it's probably a 
            #mysqli statement, so we don't want to remove it
            toMod=toMod[i.end(0):]
    modded = re.sub('\$\w+','?',toMod)
    
    print modded
    build_prepared_statement(toMod)
    
def build_prepared_statement(toMod):
    
    global oldstdout
    
    pattern = re.compile('\$\w+')
    iter = pattern.finditer(toMod)
    
    #Mind parameter types: s = string, i = integer, d = double, b = blob
    sys.stdout.write("$stmt->bind_param(\'")
    #no way to find the length of an iterator without iterating through it
    for i in iter:
        oldstdout.write("Enter parameter type for " + toMod[i.start(0):i.end(0)] + " :")
        oldstdout.flush()
        input=raw_input()
        sys.stdout.write(input)
    
    sys.stdout.write("\'")
    
    iter = pattern.finditer(toMod)
    for i in iter:
        sys.stdout.write(" ," + toMod[i.start(0):i.end(0)])
        
    sys.stdout.write(")\n\n")
    
    sys.stdout.write("$stmt->execute()\n\n")
    
    
if __name__ == '__main__':
    main()
