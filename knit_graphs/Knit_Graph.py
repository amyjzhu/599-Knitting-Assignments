"""The graph structure used to represent knitted objects"""
from enum import Enum
from typing import Dict, Optional, List, Tuple, Union

import networkx

from knit_graphs.Loop import Loop
from knit_graphs.Yarn import Yarn


class Pull_Direction(Enum):
    """An enumerator of the two pull directions of a loop"""
    BtF = "BtF"
    FtB = "FtB"

    def opposite(self):
        """
        :return: returns the opposite pull direction of self
        """
        if self is Pull_Direction.BtF:
            return Pull_Direction.FtB
        else:
            return Pull_Direction.BtF


class Knit_Graph:
    """
    A class to knitted structures
    ...

    Attributes
    ----------
    graph : networkx.DiGraph
        the directed-graph structure of loops pulled through other loops
    loops: Dict[int, Loop]
        A map of each unique loop id to its loop
    yarns: Dict[str, Yarn]
         Yarn Ids mapped to the corresponding yarn
    """

    def __init__(self):
        self.graph: networkx.DiGraph = networkx.DiGraph()
        self.loops: Dict[int, Loop] = {}
        self.last_loop_id: int = -1
        self.yarns: Dict[str, Yarn] = {}

    def add_loop(self, loop: Loop):
        """
        :param loop: the loop to be added in as a node in the graph
        """
        # Add a node with the loop id to the graph with a parameter keyed to it at "loop" to store the loop
        # If this loop is not on its specified yarn add it to the end of the yarn
        # Add the loop to the loops dictionary

        
        # add loop to graph (with Loop as attribute)
        loop_id = loop.loop_id
        self.graph.add_node(loop_id, loop=loop)
        self.last_loop_id = loop_id

        # add to list of loops
        self.loops[loop_id] = loop

        # get associated yarn
        yarn_id = loop.yarn_id
        yarn = self.yarns[yarn_id]

        if yarn is None:
            raise AttributeError

        # if this loop isn't already on the yarn, add to end of yarn
        if (not yarn.__contains__(loop)):
            yarn.add_loop_to_end(loop_id, loop)
            


    def add_yarn(self, yarn: Yarn):
        """
        :param yarn: the yarn to be added to the graph structure
        """
        self.yarns[yarn.yarn_id] = yarn

    def connect_loops(self, parent_loop_id: int, child_loop_id: int,
                      pull_direction: Pull_Direction = Pull_Direction.BtF,
                      stack_position: Optional[int] = None, depth: int = 0, parent_offset: int = 0,):
        """
        Creates a stitch-edge by connecting a parent and child loop
        :param parent_offset: The direction and distance, oriented from the front, to the parent_loop
        :param depth: -1, 0, 1: The crossing depth in a cable over other stitches. 0 if Not crossing other stitches
        :param parent_loop_id: the id of the parent loop to connect to this child
        :param child_loop_id:  the id of the child loop to connect to the parent
        :param pull_direction: the direction the child is pulled through the parent
        :param stack_position: The position to insert the parent into, by default add on top of the stack
        """
        # Make an edge in the graph from the parent loop to the child loop. The edge should have three parameters:
        # "pull_direction", "depth", and "parent_offset"
        # add the parent loop to the child's parent loop stack

        # make an edge
        # want to add a notion of length 
        self.graph.add_edge(parent_loop_id, child_loop_id, pull_direction=pull_direction, depth=depth,\
             parent_offset = parent_offset)

        # get the loops from loop storage
        loop = self.loops[child_loop_id]
        parent = self.loops[parent_loop_id]
        # add the parent loop
        loop.add_parent_loop(parent, stack_position)


    def get_courses(self) -> Tuple[Dict[int, float], Dict[float, List[int]]]:
        """
        Course information will be used to generate instruction for knitting machines and
         visualizations that structure knitted objects like grids.
         Evaluation of a course structure should be done in O(n*m) time where n is the number of loops in the graph and
         m is the largest number of parent loops pulled through a single loop (rarely more than 3).
        :return: A dictionary of loop_ids to the course they are on,
        a dictionary or course ids to the loops on that course in the order of creation
        The first set of loops in the graph is on course 0.
        A course change occurs when a loop has a parent loop that is in the last course.
        """
       
        # by default, assign the same course as the neighbor
        # (solves the problems of yarn-overs, etc)
        # then check the parents
        # if the parents exist, the loop must be on a course
        # greater than the latest parent
        
        knitgraph = self.graph 
        # assumptions about how the knitgraph works
        first_id = 0
        first_course = 0

        # get the first node in the graph (one with no in edges)
        first = list(networkx.topological_sort(knitgraph))[first_id]

        # store a list of loops on each course and a loop-to-course map
        on_each_course = dict()
        loop_to_course = dict()

        # we have the id of the first element
        loop = knitgraph.nodes[first]["loop"]
        # this node obviously goes on the first course
        loop_to_course[first] = first_course
        on_each_course.setdefault(first_course, []).append(first)

        # now we're working with other nodes in the same course
        current_course = first_course

        # now get the yarn neighbor
        # something different might happen if different yarns suddenly appear...
        yarn = self.yarns[loop.yarn_id]

        if yarn is None:
            raise AttributeError
        
        # find the neighbors of the loop on the yarn 
        outs = list(yarn.yarn_graph.neighbors(first))
    
        assert(len(outs) <= 1) # Yarn can't have two out edges
        while (len(outs) > 0):
            # grab the neighbor
            out = outs[0]
            temp = current_course
            # need the Loop info for parents
            node = knitgraph.nodes[out]["loop"]
            # get the maximum course of all parents
            parent_max = max([loop_to_course[x.loop_id] for x in node.parent_loops] + [-1]) # in case no parents
            # compare parents to current course
            course = max([parent_max + 1, temp])

            loop_to_course[out] = course
            on_each_course.setdefault(course, []).append(out)
            # update course we're working with
            current_course = course

            # get the next neighbors
            outs = list(yarn.yarn_graph.neighbors(out))

        return (loop_to_course, on_each_course)

    def __contains__(self, item: Union[int, Loop]) -> bool:
        """
        :param item: the loop being checked for in the graph
        :return: true if the loop_id of item or the loop is in the graph
        """
        if type(item) is int:
            return self.graph.has_node(item)
        elif isinstance(item, Loop):
            return self.graph.has_node(item.loop_id)

    def __getitem__(self, item: int) -> Loop:
        """
        :param item: the loop_id being checked for in the graph
        :return: the Loop in the graph with the matching id
        """
        if item not in self:
            raise AttributeError
        else:
            return self.graph.nodes[item]["loop"]
