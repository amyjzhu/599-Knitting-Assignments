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
                                                                                          "yo": self._yo(), "slip": self._slip(),
                                                                                          "float": self._float()}
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

        # TODO: so we need how many are crossing and which direction.
        # how many left to right is how many at top...
        
        knit = Pull_Direction.BtF
        purl = Pull_Direction.FtB

        # do the interior 
        # left_sts = 1
        # right_sts = 1
        # lean = "L"
        # lean_dir = Stitch_Lean.Left

                    
       # make entries for a particular combination of left and right cables
       # and lean
       # i.e. for left cable n stitches wide and right cable m stitches wide, and lean L
       # make entries that knit all stitches, purl first cable, purl second cable, and purl all
        def add_entries(left_sts, right_sts, lean, lean_dir):
            # Which direction comes first in notation?
            if lean_dir == Stitch_Lean.Left:
                first = left_sts
                second = right_sts
                
            else:
                first = right_sts
                second = left_sts

        
            self[f'{lean}C{first}|{second}'] = Cable_Definition(left_crossing_loops= left_sts, \
                                                            right_crossing_loops= right_sts, \
                                                            left_crossing_pull_direction=knit, 
                                                            right_crossing_pull_direction=knit, 
                                                            cable_lean=lean_dir)

            # if left is the first direction, then first P applies to it
            left_purl = purl if lean_dir == Stitch_Lean.Left else knit
            # if right is first direction, first P applies to it
            right_purl = purl if lean_dir == Stitch_Lean.Right else knit

            self[f'{lean}C{first}P|{second}'] = Cable_Definition(left_crossing_loops= left_sts, \
                                                            right_crossing_loops= right_sts, \
                                                            left_crossing_pull_direction=left_purl, 
                                                            right_crossing_pull_direction=right_purl, 
                                                            cable_lean=lean_dir)

            # for P on the second group, just reverse them
            left_purl, right_purl = right_purl, left_purl
            self[f'{lean}C{first}|{second}P'] = Cable_Definition(left_crossing_loops= left_sts, \
                                                            right_crossing_loops= right_sts, \
                                                            left_crossing_pull_direction=left_purl, 
                                                            right_crossing_pull_direction=right_purl, 
                                                            cable_lean=lean_dir)

            self[f'{lean}C{first}P|{second}P'] = Cable_Definition(left_crossing_loops= left_sts, \
                                                            right_crossing_loops= right_sts, \
                                                            left_crossing_pull_direction=purl, 
                                                            right_crossing_pull_direction=purl, 
                                                            cable_lean=lean_dir)
        
        # Now loop over all combinations 
        for left_sts in range(1, 3):
            for right_sts in range(1, 3):
                for lean in ["L", "R"]:
                    if lean == "L":
                        lean_dir = Stitch_Lean.Left
                    else:
                        lean_dir = Stitch_Lean.Right

                    add_entries(left_sts, right_sts, lean, lean_dir)
    

    def _decreases(self):
        # Todo: add decrease symbols keyed to their definitions to the symbol table
        #  (i.e., self[{stitch_name}] = Stitch_Definition(...))
        #  You need to implement the following stitches: k2tog,k3tog, p2tog, p3tog,
        #   skpo,sppo (purl version of skpo), s2kpo, s2ppo, sk2po, sp2po
        
        knit = Pull_Direction.BtF
        purl = Pull_Direction.FtB

        self["k2tog"] = Stitch_Definition(pull_direction=knit, offset_to_parent_loops=[-1, 0])
        self["k3tog"] = Stitch_Definition(pull_direction=knit, offset_to_parent_loops=[-2, -1, 0])

        self["p2tog"] = Stitch_Definition(pull_direction=purl, offset_to_parent_loops=[-1, 0])
        self["p3tog"] = Stitch_Definition(pull_direction=purl, offset_to_parent_loops=[-2, -1, 0])

        self["skpo"] = Stitch_Definition(pull_direction=knit, offset_to_parent_loops=[0, 1])
        # left-leaning decrease
        self["s2kpo"] = Stitch_Definition(pull_direction=knit, offset_to_parent_loops=[0, 1, 2]) 
        # centred decrease
        self["sk2po"] = Stitch_Definition(pull_direction=knit, offset_to_parent_loops=[-1, 0, 1])

        # purl versions    
        self["sppo"] = Stitch_Definition(pull_direction=purl, offset_to_parent_loops=[0, 1])
        self["s2ppo"] = Stitch_Definition(pull_direction=purl, offset_to_parent_loops=[0, 1, 2]) 
        self["sp2po"] = Stitch_Definition(pull_direction=purl, offset_to_parent_loops=[-1, 0, 1])



    @staticmethod
    def _slip() -> Stitch_Definition:
        # Todo: Return (in one line) a Stitch Definition with no child_loops
        return Stitch_Definition(pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=None, child_loops=0)
        

    @staticmethod
    def _yo() -> Stitch_Definition:
        # Todo: Return (in one line) will create a new loop with no parents
        return Stitch_Definition(pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[], child_loops=1)

    @staticmethod
    def _purl() -> Stitch_Definition:
        # Todo: Return (in one line) a Stitch Definition that will purl the next available loop
        print("I am purling but how many?")
        return Stitch_Definition(pull_direction=Pull_Direction.FtB) # only distinguishing feature

    @staticmethod
    def _knit() -> Stitch_Definition:
        # Todo: Return (in one line) a Stitch Definition that will knit the next available loop
        return Stitch_Definition(pull_direction=Pull_Direction.BtF)
        
    @staticmethod
    def _float() -> Stitch_Definition:
        print("FLOATING")
        return Stitch_Definition(pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[], child_loops=0)

    def __contains__(self, item: str):
        return item.lower() in self._symbol_table

    def __setitem__(self, key: str, value: Union[int, Stitch_Definition, Cable_Definition]):
        self._symbol_table[key.lower()] = value

    def __getitem__(self, item: str):
        return self._symbol_table[item.lower()]
