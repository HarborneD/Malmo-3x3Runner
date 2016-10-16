import MalmoPython
import os
import sys
import time
import json



class GridViewRunnerAgent:
    
    def __init__(self,traversable_list,victory_block):
        self.current_state = "0:0"
        
        self.actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]
        self.OppositeActions = {0:1, 1:0, 2:3, 3:2}
        
        self.state_graph = {}
        self.queue = []

        self.visited = set([])
        
        self.traversable_types = traversable_list
    	self.victory_type = victory_block

    	self.final_block_found = False

    def TakeNextAction(self,world_state,agent_host):
    	if(len(world_state.observations) > 0):
	    	if(not self.final_block_found):
	            if self.current_state not in self.state_graph.keys():
	                final_block_found = self.ProcessSurroundingBlocks(world_state)

	            print "Graph:"
	            print self.state_graph
	            print 

	            print "Queue:"
	            print self.queue
	            print

	            if(len(self.queue) > 0):
	                destination_state = self.queue.pop()
	                next_directions = self.GetDirections(destination_state)

	                print "Directions:"
	                print next_directions
	                print

	                move_count = 0
	                for direction in next_directions:
	                    # print "Direction:"
	                    # print direction
	                    # print
	                    move_count += 1
	                    print "move_count"
	                    print move_count
	                    try:
	                    	#time.sleep(0.3)
	                    	#if(move_count > 1):
	                    		#time.sleep(0.3)
	                        agent_host.sendCommand(direction)
	                        self.visited.add(destination_state)
	                        self.current_state = destination_state
	                    except RuntimeError as e:
	                        print "Failed to send command: %s" % e

    def GetSurroundingBlockList(self,world_state):
        grid = []

        if world_state.number_of_observations_since_last_state > 0: # Have any observations come in?
            msg = world_state.observations[-1].text                 # Yes, so get the text
            observations = json.loads(msg)                          # and parse the JSON
            grid = observations.get(u'floor3x3', 0)                 # and get the grid we asked for

        return grid

    def ProcessSurroundingBlocks(self,world_state):
        block_list = self.GetSurroundingBlockList(world_state)

        connected_states = []

        msg = world_state.observations[-1].text                 # Yes, so get the text
        observations = json.loads(msg)                          # and parse the JSON
        rotation = observations.get(u'Yaw', 0)                 # and get the grid we asked for

        print "block_list"
        print block_list
        print

        for block_type_index in range(0,len(block_list)):
            if block_list[block_type_index] in self.traversable_types:
                new_state = self.GetStateCodeFromObservationIndex(self.current_state,block_type_index,rotation)

                if(new_state == ""):
                	continue
                connected_states.append(new_state)

                if new_state not in self.queue:
                    if new_state not in self.visited:
                    	self.queue.append(new_state)

                if block_list[block_type_index] == self.victory_type:
                	self.final_block_found = True
                	break

        self.state_graph[self.current_state] = connected_states
        

    def GetStateCodeFromObservationIndex(self,current_state,index,rotation=0):
        state_split = current_state.split(':')

        state_x = int(state_split[0])
        state_y = int(state_split[1])

        # if(rotation != 90):
        #     index = 8-index

        if index == 0:
            state_x += -1
            state_y += 1

            return ""

        elif index == 1:
            state_x += 0
            state_y += 1

        elif index == 2:
            state_x += 1
            state_y += 1

            return ""

        elif index == 3:
            state_x += -1
            state_y += 0

        elif index == 4:
            state_x += 0
            state_y += 0

            return ""

        elif index == 5:
            state_x += 1
            state_y += 0

        elif index == 6:
            state_x += -1
            state_y += -1

            return ""

        elif index == 7:
            state_x += 0
            state_y += -1

        elif index == 8:
            state_x += 1
            state_y += -1

            return ""

        return str(state_x)+":"+str(state_y)


    def GetDirections(self,destination_state):
    	
    	print "looking for path from " + self.current_state + " to " + destination_state
    	#shortest_path = self.FindShortestPath(self.state_graph,self.current_state,destination_state)
    	path = self.FindPath(self.state_graph,self.current_state,destination_state)

    	print "path found:"
    	print path
    	print 

    	directions = []

    	# for destination_node_index in range(1,len(shortest_path)):
    	# 	directions.append(self.GetMoveCommandState2State(shortest_path[destination_node_index-1],shortest_path[destination_node_index] ) )

    	for destination_node_index in range(1,len(path)):
    		directions.append(self.GetMoveCommandState2State(path[destination_node_index-1],path[destination_node_index] ) )

    	return directions

    def GetMoveCommandState2State(self,from_state,to_state):

    	from_split = from_state.split(':')
    	to_split = to_state.split(':')	

    	from_x = int(from_split[0])
    	from_y = int(from_split[1])

    	to_x = int(to_split[0])
    	to_y = int(to_split[1])

    	if(to_x > from_x):
    		return "moveeast 1"
    	elif(from_x > to_x):
    		return "movewest 1"
    	elif(to_y > from_y):
    		return "movenorth 1"
    	else:
    		return "movesouth 1"

    def FindShortestPath(self,graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = self.FindShortestPath(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest


    def FindPath(self,graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in path:
                newpath = self.FindPath(graph, node, end, path)
                if newpath: return newpath
        return None
        
