'''
Chris Delaney
References
1. An Eight-Puzzle Solver in Python, downloaded: 2/18/18 from 
   https://gist.github.com/flatline/8382021
2. Paul de Palma
'''

from copy import deepcopy
import heapq
import queue as Q

#nested list representation of 8 puzzle. 0 is the blank
_init_state = [[2,8,3],
               [1,6,4],
               [7,0,5]]

_goal_state = [[1,2,3],
               [8,0,4],
               [7,6,5]] 

class EightPuzzle:
    def __init__(self):
        #child states will be kept in a list
        #the constructor adds the initial (i.e., parent state) to the list
        self.state_lst = [[row for row in _init_state]]
        self.opened = []
        self.closed = []
        self.latest_children = []
        self.depth = []
        self.depthidx = 0
        self.depth.append(self.depthidx)
        self.open_q = Q.PriorityQueue()
        self.visited = set()

    #displays all states in the list
    def display(self):
        i = 0
        for state in self.state_lst:
            i = i + 1
            print(i)
            for row in state:
                print(row)
            print("")
        

    #returns (row,col) of value in state indexed by state_idx  
    def find_coord(self, value, state_idx):
        for row in range(3):
            for col in range(3):
                if self.state_lst[state_idx][row][col] == value:
                    return (row,col)
           
    #returns list of (row, col) tuples which can be swapped for blank
    #these form the legal moves of state state_idx within the state list 
    def get_new_moves(self, state_idx):
        row, col = self.find_coord(0,state_idx) #get row, col of blank
        moves = []
        if row > 0:
            moves.append((row - 1, col))  #move from directly above
        if col > 0:
            moves.append((row, col - 1))  #move from the left
        if row < 2:
            moves.append((row + 1, col)) # move from the bottom
        if col < 2:
            moves.append((row, col + 1)) # move from the right
        return moves


    #Generates all child states for the state indexed by state_idx
    #in the state list.  Appends child states to the list
    def generate_states(self,state_idx):

        self.latest_children = []
        self.depthidx = self.depthidx + 1

        #get legal moves
        move_lst = self.get_new_moves(state_idx)
        
        #find coordinates of the blank position
        blank = self.find_coord(0,state_idx)

        #shift the blank and tile to be moved for each move 
        #append resulting state to the state list
        for tile in move_lst:
            #create a new state using deep copy 
            #ensures that matrices are completely independent
            clone = deepcopy(self.state_lst[state_idx])

            #move tile to position of the blank
            clone[blank[0]][blank[1]] = clone[tile[0]][tile[1]]

            #set tile position to 0                          
            clone[tile[0]][tile[1]] = 0
            
            if clone not in self.state_lst:
                self.state_lst.append(clone)
                self.latest_children.append(clone)
                self.depth.append(self.depthidx)


    def depth_first_search(self):
        self.opened.append(_init_state)

        while(self.opened):
            CS = self.opened.pop()

            if (CS == _goal_state):
                print(CS)
                return True

            else:
                i = self.state_lst.index(CS)
                if (self.depth[i] <= 5):
                    self.depthidx = self.depth[i]
                    self.generate_states(i)

                self.closed.append(CS) #outside if

                for child in reversed(self.latest_children):
                     if (child not in self.opened and child not in self.closed):
                         self.opened.append(child)

        return False

    def find_goalstate_coord(self, goal_state,value):
        for row in range(3):
            for col in range(3):
                if goal_state[row][col] == value:
                    return (row,col)     

    def heuristic(self, state_idx):
        score = 0
        for i in range(9):
            row, col = self.find_coord(i, state_idx)
            g_row, g_col = self.find_goalstate_coord(_goal_state,i)
            score = score + abs(row - g_row) + abs(col - g_col)
        return score

    def best_first_search(self):
        f = self.heuristic(0) + self.depth[0]
        g = self.depth[0]
        self.open_q.put((f, g, _init_state))
        while not self.open_q.empty():
            cs = self.open_q.get()[2]
            self.closed.append(cs)
            if (cs == _goal_state):
                return True
            else:
                cs_idx = self.state_lst.index(cs)
                self.generate_states(cs_idx)
                for child in self.latest_children:
                    c_idx = self.state_lst.index(child)
                    if child not in self.closed:
                        c_f = self.heuristic(c_idx)
                        if c_f == 0:
                            self.closed.append(child)
                            return True
                        self.open_q.put((c_f, self.depth[c_idx], child))
			
	    

def main():
    p = EightPuzzle()
    p.best_first_search()
    i = 0
    for state in p.closed:
        i = i + 1
        print(i)
        for row in state:
            print(row)
        print("")
    print("state list")
    p.display()

if __name__ == "__main__":
    main()
