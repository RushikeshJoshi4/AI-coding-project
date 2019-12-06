import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random
from pprint import pprint

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc
        self.count1=0

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic
        This function will do both Constraint Propagation and check
        the consistency of the network
        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.
        Note: remember to trail.push variables before you assign them
        Return: a tuple of a dictionary and a bool. The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
                The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):
        # self.trail.placeTrailMarker()
        mapV = {}
        for variable in self.network.variables:
            if variable.isAssigned():
                for varNeighbor in self.network.getNeighborsOfVariable(variable):
                    if varNeighbor.domain.contains(variable.getAssignment()):
                        self.trail.push(varNeighbor)
                        varNeighbor.removeValueFromDomain(variable.getAssignment())
                        mapV[varNeighbor] = varNeighbor.getDomain()
                    if varNeighbor.domain.isEmpty():
                        # self.trail.undo()
                        return [mapV, False]
                    
        # self.trail.trailMarker.pop()
        return [ mapV , True ] 



        

    # =================================================================
    # Arc Consistency
    # =================================================================
    def arcConsistency( self ):
        assignedVars = []
        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)
        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

    
    """
        Part 2 TODO: Implement both of Norvig's Heuristics
        This function will do both Constraint Propagation and check
        the consistency of the network
        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.
        (2) If a constraint has only one possible place for a value
            then put the value there.
        Note: remember to trail.push variables before you assign them
        Return: a pair of a dictionary and a bool. The dictionary contains all variables 
                that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
                The bool is true if assignment is consistent, false otherwise.
    """
    
    def norvigCheck (self):
        try:
            return self.norvigCheckHelper()
        except:
            return [{}, True]

    def norvigCheckHelper ( self ):
        # self.trail.placeTrailMarker()
        # print("incrementing count1")
        # self.count1+=1
        # if self.count1%100==0:
        #     print(self.count1)
        # if self.count1==10000:
        #     print(self.count1)
        #     import sys
        #     sys.exit()

        mapV = {}
        for variable in self.network.variables:
            if variable.isAssigned():
                for varNeighbor in self.network.getNeighborsOfVariable(variable):
                    if varNeighbor.domain.contains(variable.getAssignment()):
                        self.trail.push(varNeighbor)
                        varNeighbor.removeValueFromDomain(variable.getAssignment())
                        
                    if varNeighbor.domain.isEmpty():
                        return [mapV, False]
        
        # for variable in self.network.variables:
        #     if not variable.isAssigned:
        #         if variable.domain.isEmpty():
        #             print('******************************************88')
        #             return [mapV, False]

        #         if len(variable.domain.values)==1:
        #             self.trail.push(variable)
        #             variable.assign(variable.domain.values[0])

        # print("Norvig check's first part is done!")
        # print("Now, board is: ")
        # print(self.gameboard)

        rows = dict()
        cols = dict()
        blocks = dict()
        for v in self.network.variables:
            row = v.row
            col = v.col
            block = v.block

            if not (row in rows.keys()):
                rows[row] = []
            if not (col in cols.keys()):
                cols[col] = []
            if not (block in blocks.keys()):
                blocks[block] = []

            rows[row].append(v)
            cols[col].append(v)
            blocks[block].append(v)

        # for row in rows:
        #     print("Row: "+str(row))
        #     for var in rows[row]:
        #         print(var)
        #     print("")

        unique_row, unique_col, unique_block = {}, {}, {}
        for unit, unique in zip([rows, cols, blocks], [unique_row, unique_col, unique_block]):
            # counter = [0] * (self.gameboard.N+1)
            
            for unit_key in unit.keys():
                counter = [0] * (self.gameboard.N+1)
                var_list = unit[unit_key]
                # print("Var list:")
                # for v in var_list:
                #     print(v)
                # print("-----------")

                for v in var_list:
                    if v.assigned: 
                        counter[v.getAssignment()]+=1
                        continue
                    for value in v.domain.values:
                        counter[value]+=1
                        if counter[value]==1:
                            # print("Assigning")
                            # print("Value: "+str(value)+" Variable: ")
                            # print(v)
                            unique[value] = v
                        elif counter[value]==2:
                            # print("Deleting")
                            # print("Value: "+str(value)+" Variable: ")
                            # print(v)
                            del unique[value]
                
                for i, counter_element in enumerate(counter):
                    if counter_element ==0 and i !=0:
                        return [mapV, False]
            # print("uniq: ")
            # pprint(unique)
            # print('-----------------')
            # break

        # print(unique_row)
        count = 0
        for unique in unique_row, unique_col, unique_block:
            for unique_key in unique:
                count+=1
                value = unique_key
                v = unique[value]
                self.trail.push(v)
                v.assignValue(value)
                mapV[v] = value
        # if count!=3 and count!=0: print("norvig check count:"+str(count))

        # self.trail.pop()
        return [ mapV , True ] 

    
    def getTournCC ( self ):
        return False


    # ==================================================================
    # Utility functions
    # =================================================================
    def _getAllUnassignedVariables(self):
        unassignedVariables = []
        for v in self.network.variables:
            if not v.isAssigned():
                unassignedVariables.append(v)
        return unassignedVariables
    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic
        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        variables = self._getAllUnassignedVariables()
        min_ = float('inf')
        min_variable = None
        for v in variables:
            if min_ > len(v.domain.values):
                min_ = len(v.domain.values)
                min_variable = v
        # print('in getMRV returning '+str(min_variable))
        return min_variable        


    """
        Part 2 TODO: Implement the Degree Heuristic
        Return: The unassigned variable with the most unassigned neighbors
    """
    def getDegree ( self ):
        return None

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker
        Return: The unassigned variable with the smallest domain and affecting the  most unassigned neighbors.
                If there are multiple variables that have the same smallest domain with the same number of unassigned neighbors, add them to the list of Variables.
                If there is only one variable, return the list of size 1 containing that variable.
    """
    def MRVwithTieBreaker ( self ):
        ans = []
        min_domain = self.getMRV()
        ans.append(min_domain)
        if min_domain==None:
            return [None]
        for variable in self.network.variables:
            if variable.size()==min_domain.size():
                ans.append(variable)
        maxDegree = -1
        maxVariable = {}
        temp = []
        for var in ans:
            count = 0
            for varNeighbor in self.network.getNeighborsOfVariable(variable):
                if not varNeighbor.isAssigned():
                    count+=1
            if count > maxDegree:
                maxDegree = count
                temp = []
                temp.append(var)
            if count == maxDegree:
                temp.append(var)
        return temp

        '''
        tieMRV = []
        smallestVariableSize = float('inf')
        for variable in self.network.variables:
            if not variable.isAssigned():
                if variable.size() <= smallestVariableSize  or tieMRV == []:
                    if variable.size() == smallestVariableSize:
                        tempList =  tieMRV
                        tempList.append(variable)
                        maxVariable = []
                        largest = -1
                        for var in tempList:
                            constraintsVariable = self.network.getConstraintsContainingVariable(var)
                            degreeCostraintVariable = []
                            for constraint in constraintsVariable:
                                varsConstraint = constraint.vars
                                for v in varsConstraint:
                                    if not v.isAssigned():
                                        degreeCostraintVariable.append(v)
                            if len(degreeCostraintVariable) >= largest:
                                maxVariable.append(var)
                                maxDegree = len(degreeCostraintVariable)
                        tieMRV = maxVariable
                        smallestVariableSize = maxDegree
                    else:
                        tieMRV = [variable]
                        smallestVariableSize = variable.size()
        
        if(len(tieMRV)==0):
            return [None]
        return tieMRV'''
    """
         Optional TODO: Implement your own advanced Variable Heuristic
         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic
        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.
        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """

    def getValuesLCVOrder(self, v):
        """
            TODO: LCV heuristic
        """ 
        temp = {}
        for value in v.domain.values:
            count = 0
            for neighborV in self.network.getNeighborsOfVariable(v):
                if value in neighborV.domain.values:
                    count = count +1
            temp[value]=count
        sortedTemp = sorted(temp.items(),key= lambda x:x[1])
        result = []
        for item in sortedTemp:
            result.append(item[0])
        return result
    






    """
         Optional TODO: Implement your own advanced Value Heuristic
         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self ):
        if self.hassolution:
            return

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            for var in self.network.variables:

                # If all variables haven't been assigned
                if not var.isAssigned():
                    print ( "Error" )

            # Success
            self.hassolution = True
            return

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recurse
            if self.checkConsistency():
                self.solve()

            # If this assignment succeeded, return
            if self.hassolution:
                return

            # Otherwise backtrack
            self.trail.undo()

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()[1]

        # if self.cChecks == "arcConsistency":
        #     return self.arcConsistency()

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()[1]

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "Degree":
            return self.getDegree()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]


        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            x = self.getfirstUnassignedVariable()
            # print('selectNextVariable was called, returning: '+str(x))
            return x

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)