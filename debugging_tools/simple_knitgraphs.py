"""Simple knitgraph generators used primarily for debugging"""
from knit_graphs.Knit_Graph import Knit_Graph, Pull_Direction
from knit_graphs.Yarn import Yarn

def stockinette(width: int = 4, height: int = 4) -> Knit_Graph:
    """
    :param width: the number of stitches of the swatch
    :param height:  the number of courses of the swatch
    :return: a knitgraph of stockinette on one yarn of width stitches by height course
    """
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn", knitGraph, carrier_id=4)
    knitGraph.add_yarn(yarn)
    first_row = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_row.append(loop_id)
        knitGraph.add_loop(loop)

    prior_row = first_row
    for _ in range(1, height):
        next_row = []
        for parent_id in reversed(prior_row):
            child_id, child = yarn.add_loop_to_end()
            next_row.append(child_id)
            knitGraph.add_loop(child)
            knitGraph.connect_loops(parent_id, child_id)
        prior_row = next_row

    return knitGraph


def rib(width: int = 4, height: int = 4, rib_width: int = 1) -> Knit_Graph:
    """
    :param rib_width: determines how many columns of knits and purls are in a single rib.
    (i.e.) the first course of width=4 and rib_width=2 will be kkpp. Always start with knit columns
    :param width: a number greater than 0 to set the number of stitches in the swatch
    :param height: A number greater than 2 to set the number of courses in the swatch
    :return: A knit graph with a repeating columns of knits (back to front) then purls (front to back).
    """
    assert width > 0
    assert height > 1
    assert rib_width <= width

    knit_graph = Knit_Graph()
    yarn = Yarn("yarn", knit_graph)
    knit_graph.add_yarn(yarn)
    # make the first set of loops on the bottom (0th) course
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knit_graph.add_loop(loop)

    # the rib might end halfway though
    # so let's keep track of what stitches to end on
    # and whether this is a reverse row or not
    # I had an interesting idea for a mathy solution but it was hard to follow
    # so instead, make an array for the order
    rib_order_knit = []
    for s in reversed(range(0, width)):
        rib_order_knit.append((s // rib_width) % 2 == 0) # in the middle of knitting if we've done full rib, else half

    print(rib_order_knit)

    # make new course of loops and connect them to the last course
    prior_course = first_course
    
    # are we going backwards? if so, have to read pattern backwards
    currently_reversed = True
    
    for c in range(1, height):
        next_course = []
        for parent_id in reversed(prior_course):
            child_id, child = yarn.add_loop_to_end()
            next_course.append(child_id)
            knit_graph.add_loop(child)

            # what order am I in?            
            rib_order_index = parent_id - (width * (c - 1))

            # since we go back and forth, we sometimes work backwards
            if (currently_reversed):
                rib_order_index = (width - 1) - rib_order_index
            
            # what direction to fulfill the pattern?
            knitdir = Pull_Direction.BtF if rib_order_knit[rib_order_index] else Pull_Direction.FtB
            knit_graph.connect_loops(parent_id, child_id, pull_direction=knitdir)

        # switch sides
        currently_reversed = not currently_reversed
        prior_course = next_course

    return knit_graph


def seed(width: int = 4, height=4) -> Knit_Graph:
    """
    :param width: a number greater than 0 to set the number of stitches in the swatch
    :param height: A number greater than 0 to set the number of courses in the swatch
    :return: A knit graph with a checkered pattern of knit and purl stitches of width and height size.
    The first stitch should be a knit
    """
    assert width > 0
    assert height > 0    
    
    knit_graph = Knit_Graph()
    yarn = Yarn("yarn", knit_graph)
    knit_graph.add_yarn(yarn)

    # make the first set of loops on the bottom (0th) course
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knit_graph.add_loop(loop)

    # make new course of loops and connect them to the last course
    prior_course = first_course
    
    # keeping track of whether we start with knits or purls
    # if we start with knits, this is 1
    # It's not clear whether "first stitch is a knit"
    # means the first stitch we make or the first right-to-left stitch on the screen
    # I am assuming "first stitch we make" (due to seed_4x4.PNG), but can be adjusted for the latter
    # interpretation by checking parity of width (even means knit = False at start)
    knit = True
    for _ in range(1, height):
        next_course = []
        for parent_id in reversed(prior_course):
            child_id, child = yarn.add_loop_to_end()
            next_course.append(child_id)
            knit_graph.add_loop(child)
            # knit-purl-knit-purl policy always follows regardless of row
            # if we knit last time, purl next time
            if (knit):
                pull_dir = Pull_Direction.BtF
            else:
                pull_dir = Pull_Direction.FtB
            knit_graph.connect_loops(parent_id, child_id, pull_direction=pull_dir)
            # swap knit and purl
            knit = not knit
        
        prior_course = next_course

    return knit_graph


def twisted_stripes(width: int = 4, height=5, left_twists: bool = True) -> Knit_Graph:
    """
    :param left_twists: if True, make the left leaning stitches in front, otherwise right leaning stitches in front
    :param width: the number of stitches of the swatch
    :param height:  the number of courses of the swatch
    :return: A knitgraph with repeating pattern of twisted stitches surrounded by knit wales
    """
    assert width % 4 == 0, "Pattern is 4 loops wide"
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn", knitGraph)
    knitGraph.add_yarn(yarn)

    # Add the first course of loops
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knitGraph.add_loop(loop)

    def add_loop_and_knit(p_id, depth=0, parent_offset: int = 0):
        """
        adds a loop by knitting to the knitgraph
        :param parent_offset: Set the offset of the parent loop in the cable. offset = parent_index - child_index
        :param p_id: the parent loop's id
        :param depth: the crossing- depth to knit at
        """
        child_id, child = yarn.add_loop_to_end()
        next_course.append(child_id)
        knitGraph.add_loop(child)
        knitGraph.connect_loops(p_id, child_id, depth=depth, parent_offset=parent_offset)

    if left_twists:  # set the depth for the first loop in the twist (1 means it will cross in front of other stitches)
        twist_depth = 1
    else:
        twist_depth = -1

    # add new courses
    prior_course = first_course
    for course in range(1, height):
        next_course = []
        reversed_prior_course = [*reversed(prior_course)]
        for col, parent_id in enumerate(reversed_prior_course):
            if course % 2 == 0 or col % 4 == 0 or col % 4 == 3:  # knit on even rows and before and after twists
                add_loop_and_knit(parent_id)
            elif col % 4 == 1:
                next_parent_id = reversed_prior_course[col + 1]
                add_loop_and_knit(next_parent_id, depth=twist_depth, parent_offset=1)
                twist_depth = -1 * twist_depth  # switch depth for neighbor
            elif col % 4 == 2:
                next_parent_id = reversed_prior_course[col - 1]
                add_loop_and_knit(next_parent_id, depth=twist_depth, parent_offset=-1)
                twist_depth = -1 * twist_depth  # switch depth for next twist
        prior_course = next_course

    return knitGraph


def both_twists(height=20) -> Knit_Graph:
    """
    :param left_twists: if True, make the left leaning stitches in front, otherwise right leaning stitches in front
    :param width: the number of stitches of the swatch
    :param height:  the number of courses of the swatch
    :return: A knitgraph with repeating pattern of twisted stitches surrounded by knit wales
    """
    width = 10
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn", knitGraph)
    knitGraph.add_yarn(yarn)

    # Add the first course of loops
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knitGraph.add_loop(loop)

    def add_loop_and_knit(p_id, depth=0, parent_offset: int = 0):
        """
        adds a loop by knitting to the knitgraph
        :param parent_offset: Set the offset of the parent loop in the cable. offset = parent_index - child_index
        :param p_id: the parent loop's id
        :param depth: the crossing- depth to knit at
        """
        child_id, child = yarn.add_loop_to_end()
        next_course.append(child_id)
        knitGraph.add_loop(child)
        knitGraph.connect_loops(p_id, child_id, depth=depth, parent_offset=parent_offset)

    # add new courses
    prior_course = first_course
    for course in range(1, height):
        next_course = []
        reversed_prior_course = [*reversed(prior_course)]
        for col, parent_id in enumerate(reversed_prior_course):
            if course % 2 == 1 or col in {0, 1, 4, 5,8, 9}:  # knit on odd rows and borders or middle
                add_loop_and_knit(parent_id)
            elif col == 2:
                parent_id = reversed_prior_course[3]
                add_loop_and_knit(parent_id, depth=-1, parent_offset=-1)
            elif col == 3:
                parent_id = reversed_prior_course[2]
                add_loop_and_knit(parent_id, depth=1, parent_offset=1)
            elif col == 6:
                parent_id = reversed_prior_course[7]
                add_loop_and_knit(parent_id, depth=1, parent_offset=-1)
            elif col == 7:
                parent_id = reversed_prior_course[6]
                add_loop_and_knit(parent_id, depth=-1, parent_offset=1)
        prior_course = next_course

    return knitGraph


def lace(width: int = 4, height: int = 4):
    """
    :param width: the number of stitches of the swatch
    :param height:  the number of courses of the swatch
    :return: a knitgraph with k2togs and yarn-overs surrounded by knit wales
    """
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn", knitGraph)
    knitGraph.add_yarn(yarn)
    first_row = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_row.append(loop_id)
        knitGraph.add_loop(loop)

    def add_loop_and_knit(p_id, offset: int = 0):
        """
        Knits a loop into the graph
        :param p_id: the id of the parent loop being knit through
        :return: the id of the child loop created
        """
        c_id, c = yarn.add_loop_to_end()
        next_row.append(c_id)
        knitGraph.add_loop(c)
        knitGraph.connect_loops(p_id, c_id, pull_direction=Pull_Direction.BtF, parent_offset=offset)
        return c_id

    prior_row = first_row
    for row in range(1, height):
        next_row = []
        prior_parent_id = -1
        reversed_prior_row = [*reversed(prior_row)]
        for col, parent_id in enumerate(reversed_prior_row):
            if row % 2 == 0 or col % 4 == 0 or col % 4 == 3:  # knit on even rows and before and after twists
                add_loop_and_knit(parent_id)
            elif col % 4 == 1:
                child_id, child = yarn.add_loop_to_end()
                knitGraph.add_loop(child)
                next_row.append(child_id)  # yarn over
                prior_parent_id = parent_id
            elif col % 4 == 2:
                child_id = add_loop_and_knit(parent_id)
                knitGraph.connect_loops(prior_parent_id, child_id, parent_offset=-1)
        prior_row = next_row

    return knitGraph
