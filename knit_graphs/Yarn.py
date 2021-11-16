"""
The Yarn Data Structure
"""
from typing import Optional, Tuple, Union, List

import networkx as networkx

from knit_graphs.Loop import Loop
from knitting_machine.Machine_State import Yarn_Carrier

class Yarn:
    """
    A class to represent a yarn structure
    ...

    Attributes
    ----------
    yarn_graph: networkx.DiGraph
        A directed graph structure (always a list) of loops on the yarn
    last_loop_id: int
        The id of the last loop on the yarn, none if no loops on the yarn
    """

    def __init__(self, yarn_id: str, knit_graph, last_loop: Optional[Loop] = None, carrier_id: int = 3):
        """
        A Graph structure to show the yarn-wise relationship between loops
        :param knit_graph: The knitgraph the yarn is used in
        :param yarn_id: the identifier for this loop
        :param last_loop: the loop to add onto this yarn at the beginning. May be none if yarn is empty.
        """
        self.knit_graph = knit_graph
        assert 0 < carrier_id < 11, f"Invalid yarn carrier {carrier_id}"
        self._carrier: Yarn_Carrier = Yarn_Carrier(carrier_id)
        self.yarn_graph: networkx.DiGraph = networkx.DiGraph()
        if last_loop is None:
            self.last_loop_id = None
        else:
            self.last_loop_id: int = last_loop.loop_id
        self._yarn_id: str = yarn_id
        self.knitgraph = knit_graph

    @property
    def carrier(self) -> Yarn_Carrier:
        """
        :return: the yarn-carrier holding this yarn
        """
        return self._carrier

    @property
    def yarn_id(self) -> str:
        """
        :return: the id of this yarn
        """
        return self._yarn_id

    def add_skip_loops(self, loop_id: int = None, loop: Optional[Loop] = None,
                        is_twisted: bool = False, length_multiple = 1) -> Tuple[List[Tuple[int, Loop]], Tuple[int, Loop]]:
        lid = loop_id
        first_stitch = False

        # TODO: THIS ONLY WORKS IF WE ALWAYS SUPPLY ID 
        # MAYBE REMOVE ABILITY TO SELF-SPECIFY 
        
        # if we didn't have any other stitches on this yarn
        # then the last_loop_id is none and we don't want to make a connection
        if self.last_loop_id is None:
            # TODO double-check handling of discrepant "last loop id"s
            # currently taking from global knitgraph
            self.last_loop_id = self.knitgraph.last_loop_id
            first_stitch = True


        # we weren't given a loop id, so just take 1 + last_loop_id
        if loop_id is None:    
            lid = self.last_loop_id + 1
            
        loops = []
        for i in range(length_multiple - 1):
            int_loop = Loop(lid+i, self.yarn_id, is_twisted=False, skip=True)
            self.yarn_graph.add_node(lid + i, loop=int_loop)
            loops.append((lid+i, int_loop))
           
        new_lid = lid + length_multiple - 1

        # create a Loop if needed
        if loop is None:
            loop = Loop(new_lid, self.yarn_id, is_twisted)
        
        # add node to graph
        # TODO: hack to make sure it's the right lid, but may break. enforce!!!!
        #loop.loop_id = new_lid 
        
        self.yarn_graph.add_node(new_lid, loop=loop)

        # if there were stitches on the yarn, then connect them yarnwise
        if not first_stitch:
            # can only connect if there are previous loops
            # if there should be multiple in between, make some dummy loops 
            for i in range(length_multiple):
                # connect 
                self.yarn_graph.add_edge(lid + i - 1, lid + i)
            # connect the last edge
            self.yarn_graph.add_edge(self.last_loop_id, lid)
                    
        # and set the last_loop_id to this one
        self.last_loop_id = new_lid

        # TODO: need to return all the middle stitches so we can get courses properly
    
        return (loops, (new_lid, loop))

    def add_loop_to_end(self, loop_id: int = None, loop: Optional[Loop] = None,
                        is_twisted: bool = False, length_multiple = 1) -> Tuple[int, Loop]:
        """
        Adds the loop at the end of the yarn
        :param is_twisted: The parameter used for twisting the loop if it is created in the method
        :param loop: The loop to be added at this id. If none, an non-twisted loop will be created
        :param loop_id: the id of the new loop, if the loopId is none,
            it defaults to 1 more than last put on the knit Graph (CHANGE)
        :return: the loop_id added to the yarn, the loop added to the yarn
        :param length_multiple: How many needles apart are this stitch from last stitch (1 = next to each other)
        """
        lid = loop_id
        first_stitch = False

        # TODO: REVERT TO ORIGINAL
        
        # if we didn't have any other stitches on this yarn
        # then the last_loop_id is none and we don't want to make a connection
        if self.last_loop_id is None:
            # TODO double-check handling of discrepant "last loop id"s
            # currently taking from global knitgraph
            self.last_loop_id = self.knitgraph.last_loop_id
            first_stitch = True


        # we weren't given a loop id, so just take 1 + last_loop_id
        if loop_id is None:    
            lid = self.last_loop_id + 1
            
        for i in range(length_multiple - 1):
           self.yarn_graph.add_node(lid + i, loop=Loop(lid+i, self.yarn_id, is_twisted=False, skip=True))
           
        new_lid = lid + length_multiple - 1

        # create a Loop if needed
        if loop is None:
            loop = Loop(new_lid, self.yarn_id, is_twisted)
        
        # add node to graph
        # TODO: hack to make sure it's the right lid, but may break. enforce!!!!
        #loop.loop_id = new_lid 
        self.yarn_graph.add_node(new_lid, loop=loop)

        # if there were stitches on the yarn, then connect them yarnwise
        if not first_stitch:
            # can only connect if there are previous loops
            # if there should be multiple in between, make some dummy loops 
            for i in range(length_multiple - 1):
                # connect 
                self.yarn_graph.add_edge(lid, lid + i)
            # connect the last edge
            self.yarn_graph.add_edge(self.last_loop_id, lid)
                    
        # and set the last_loop_id to this one
        self.last_loop_id = new_lid

        # TODO: need to return all the middle stitches so we can get courses properly
    
        return (new_lid, loop)

    def __contains__(self, item: Union[int, Loop]) -> bool:
        """
        :param item: the loop being checked for in the yarn
        :return: true if the loop_id of item or the loop is in the yarn
        """
        if type(item) is int:
            return self.yarn_graph.has_node(item)
        elif isinstance(item, Loop):
            return self.yarn_graph.has_node(item.loop_id)

    def __getitem__(self, item: int) -> Loop:
        """
        :param item: the loop_id being checked for in the yarn
        :return: the Loop on the yarn with the matching id
        """
        if item not in self:
            raise AttributeError
        else:
            return self.yarn_graph.nodes[item].loop
