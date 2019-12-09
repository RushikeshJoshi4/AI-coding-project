#!/usr/bin/env python3

import sys
import os
import math
import SudokuBoard
import Constraint
import ConstraintNetwork
import BTSolver
import Trail
import time
import io

"""
    Main driver file, which is responsible for interfacing with the
    command line and properly starting the backtrack solver.
"""

def blockPrint():
    sys.stdout = io.StringIO()

def main (args_=[]):
    to_print = True
    args = None
    # print(args_)
    # print(args_)
    if len(args_)==0:
        args = sys.argv    
    else:
        args = args_[:-1]
        if not args_[-1]:
            to_print = False
        #print("to_print: ",to_print)
    
    #if to_print:
        #blockPrint()

    # Important Variables
    file   = "";
    var_sh = "";
    val_sh = "";
    cc     = "";

    for arg in [args[i] for i in range(1, len(args))]:
        if arg == "MRV":
            var_sh = "MinimumRemainingValue"

        elif arg == "MAD":
            var_sh = "MRVwithTieBreaker"

        elif arg == "LCV":
            val_sh = "LeastConstrainingValue"

        elif arg == "FC":
            cc = "forwardChecking"

        elif arg == "NOR":
            cc = "norvigCheck"

        elif arg == "TOURN":
            var_sh = "tournVar"
            val_sh = "tournVal"
            cc     = "tournCC"

        else:
            file = arg;

    trail = Trail.Trail();

    if file == "":
        sudokudata = SudokuBoard.SudokuBoard( 3,3,7)
        if to_print: print(sudokudata)

        solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, cc )
        if cc in ["forwardChecking","norvigCheck","tournCC"]:
            solver.checkConsistency()
        solver.solve()

        if solver.hassolution:
            if to_print: print( solver.getSolution() )
            if to_print: print( "Trail Pushes: " + str(trail.getPushCount()) )
            if to_print: print( "Backtracks: " + str(trail.getUndoCount()) )

        else:
            if to_print: print( "Failed to find a solution" )
            return False

        return True

    if os.path.isdir(file):
        listOfBoards = None

        try:
            listOfBoards = os.listdir ( file )
        except:
            if to_print: print ( "[ERROR] Failed to open directory." )
            return False

        numSolutions = 0
        for f in listOfBoards:
            if to_print: print ( "Running board: " + str(f) )
            sudokudata = SudokuBoard.SudokuBoard( filepath=os.path.join( file, f ) )

            solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, cc )
            if cc in ["forwardChecking","norvigCheck","tournCC"]:
                solver.checkConsistency()
            solver.solve()

            if solver.hassolution:
                numSolutions += 1;

        if to_print: print ( "Solutions Found: " + str(numSolutions) )
        if to_print: print ( "Trail Pushes: " + str(trail.getPushCount()) )
        if to_print: print ( "Backtracks: "  + str(trail.getUndoCount()) )

        return True

    sudokudata =  SudokuBoard.SudokuBoard( filepath=os.path.abspath( file ) )
    if to_print: print(sudokudata)

    solver = BTSolver.BTSolver( sudokudata, trail, val_sh, var_sh, cc )
    if cc in ["forwardChecking","norvigCheck","tournCC"]:
        solver.checkConsistency()
    solver.solve()

    if solver.hassolution:
        if to_print: print( solver.getSolution() )
        if to_print: print( "Trail Pushes: " + str(trail.getPushCount()) )
        if to_print: print( "Backtracks: " + str(trail.getUndoCount()) )
        return True
    else:
        if to_print: print( "Failed to find a solution" )
        return False

# main()
