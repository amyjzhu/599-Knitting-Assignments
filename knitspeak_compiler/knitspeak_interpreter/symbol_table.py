"""Symbol Table structure holds definitions of stitches and context for number variables"""
from typing import Dict, Union

from knit_graphs.Knit_Graph import Pull_Direction
from knitspeak_compiler.knitspeak_interpreter.cable_definitions import Cable_Definition
from knitspeak_compiler.knitspeak_interpreter.stitch_definitions import Stitch_Definition, Stitch_Lean


class Symbol_Table:
    """
    A class used to keep track of how stitches and number variables have been defined. Includes language defaults
    """

    def __init__(self):
        self._symbol_table: Dict[str, Union[Cable_Definition, Stitch_Definition, int]] = {"k": self._knit(), "p": self._purl(),
                                                                                          "yo": self._yo(), "slip": self._slip()}
        self._decreases()
        self._cables()
        # set current row variable
        self._symbol_table["current_row"] = 0

    def _cables(self):
        # Todo: Add cable symbols keyed to their definitions to the symbol table
        #  (i.e., self._symbol_table[{cable_name}] = Cable_Definition(...))
        #  for every combination of right and left loop counts create cables that:
        #   lean left, lean right, lean left and purl, lean right and purl,
        #  e.g. for 1 left stitch and 2 right stitches you will have:
        #   LC1|2, LC1P|2, LC1|2P, LC1P|2P, RC1|2, RC1P|2, RC1|2P, RC1P|2P
        #  each group of loops can have 1, 2, or 3 loops
        raise NotImplementedError

    def _decreases(self):
        # Todo: add decrease symbols keyed to their definitions to the symbol table
        #  (i.e., self[{stitch_name}] = Stitch_Definition(...))
        #  You need to implement the following stitches: k2tog,k3tog, p2tog, p3tog,
        #   skpo,sppo (purl version of skpo), s2kpo, s2ppo, sk2po, sp2po
        raise NotImplementedError

    @staticmethod
    def _slip() -> Stitch_Definition:
        # Todo: Return (in one line) a Stitch Definition with no child_loops
        raise NotImplementedError

    @staticmethod
    def _yo() -> Stitch_Definition:
        # Todo: Return (in one line) will create a new loop with no parents
        raise NotImplementedError

    @staticmethod
    def _purl() -> Stitch_Definition:
        # Todo: Return (in one line) a Stitch Definition that will purl the next available loop
        raise NotImplementedError

    @staticmethod
    def _knit() -> Stitch_Definition:
        # Todo: Return (in one line) a Stitch Definition that will knit the next available loop
        raise NotImplementedError

    def __contains__(self, item: str):
        return item.lower() in self._symbol_table

    def __setitem__(self, key: str, value: Union[int, Stitch_Definition, Cable_Definition]):
        self._symbol_table[key.lower()] = value

    def __getitem__(self, item: str):
        return self._symbol_table[item.lower()]
