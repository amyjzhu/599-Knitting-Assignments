"""
The Yarn Data Structure
"""
from typing import Optional, Tuple, Union

import networkx as networkx

from knit_graphs.Loop import Loop


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

    def __init__(self, yarn_id: str, knit_graph, last_loop: Optional[Loop] = None):
        """
        A Graph structure to show the yarn-wise relationship between loops
        :param yarn_id: the identifier for this loop
        :param last_loop: the loop to add onto this yarn at the beginning. May be none if yarn is empty.
        """
        self.yarn_graph: networkx.DiGraph = networkx.DiGraph()
        if last_loop is None:
            self.last_loop_id = None
        else:
            self.last_loop_id: int = last_loop.loop_id
        self._yarn_id: str = yarn_id
        self.knitgraph = knit_graph

    @property
    def yarn_id(self) -> str:
        """
        :return: the id of this yarn
        """
        return self._yarn_id

    def add_loop_to_end(self, loop_id: int = None, loop: Optional[Loop] = None,
                        is_twisted: bool = False) -> Tuple[int, Loop]:
        """
        Adds the loop at the end of the yarn
        :param is_twisted: The parameter used for twisting the loop if it is created in the method
        :param loop: The loop to be added at this id. If none, an non-twisted loop will be created
        :param loop_id: the id of the new loop, if the loopId is none, it defaults to 1 more than last put on this yarn
        :return: the loop_id added to the yarn, the loop added to the yarn
        """
        # TODO: Implement
        # If Loop Id is None generate a new id from provided loop or based on last id on this yarn
        # If no loop is provided create one with loop id and twisted parameter
        # Add Loop Id as a node to the yarn_graph and add parameter keyed to it at "loop" to store the loop
        # Add an edge between this loop and the loop before it on the yarn
        # Update last_loop_id
        # Return the created loop's id and the loop
        lid = loop_id
        first_stitch = False
        if self.last_loop_id is None:
            # TODO double-check handling of discrepant "last loop id"s
            self.last_loop_id = self.knitgraph.last_loop_id
            first_stitch = True

        if loop_id is None:    
            lid = self.last_loop_id + 1

        if loop is None:
            loop = Loop(lid, self.yarn_id, is_twisted)
        
        self.yarn_graph.add_node(lid, loop=loop)

        # only do this if it wasn't none to begin with 
        if not first_stitch:
            print("edge from:")
            print(self.last_loop_id)
            print(lid)
            # can only connect if there are previous loops
            self.yarn_graph.add_edge(self.last_loop_id, lid)
                    
        self.last_loop_id = lid

    
        return (lid, loop)

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
