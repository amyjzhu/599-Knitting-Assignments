from debugging_tools.knit_graph_viz import visualize_knitGraph

from knitspeak_compiler.knitspeak_compiler import Knitspeak_Compiler
from knitting_machine.knitgraph_to_knitout import Knitout_Generator



def test_stst():
    pattern = "all rs rows k. all ws rows p."
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(5, 5, pattern)
    # visualize_knitGraph(knit_graph, "stst.html")

def test_skipped():
    pattern = "1st row [k] 2, float, [k] 2. 2nd row [p] 2, float, [p] 2. 3rd row [k] 2, yo, [k] to end. 4th row p. 5th row [k] to end."
    compiler = Knitspeak_Compiler()
    # 4 -> 4 + float.... eee
    knit_graph = compiler.compile(5, 5, pattern, skipped=[2])
    visualize_knitGraph(knit_graph, "skipped.html")
    generator = Knitout_Generator(knit_graph)
    generator.write_instructions("test_skipped-from-ks.k")

def test_skipped_4():
    pattern = "all rs rows [k] 2, float, [k] 2. all ws rows [p] 2, float, [p] 2."
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(5, 4, pattern, skipped=[2]) # this is probably the worst way to specify this lol
    visualize_knitGraph(knit_graph, "skipped.html")
    generator = Knitout_Generator(knit_graph)
    generator.write_instructions("test_skipped-from-ks-4.k")

def test_skipped_3():
    pattern = "1st row [k] 2, float, [k] 2. all ws rows p. 3rd row [k] 2, yo, [k] to end. 5th row [k] to end."
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(5, 5, pattern)
    visualize_knitGraph(knit_graph, "skipped.html")
    generator = Knitout_Generator(knit_graph)
    generator.write_instructions("test_skipped-from-ks.k")

def test_skipped_2():
    pattern = "1st row k, float, [k] to end. all ws rows p. 3rd row k, yo, [k] to end. 5th row [k] to end."
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(4, 4, pattern)
    visualize_knitGraph(knit_graph, "skipped2.html")

def test_rib():
    rib_width = 2
    pattern = f"all rs rows k rib={rib_width}, p rib. all ws rows k rib, p rib."
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(4, 4, pattern)
    visualize_knitGraph(knit_graph, "rib.html")


def test_cable():
    pattern = r"""
        1st row k, lc2|2, k, rc2|2, [k] to end.
        all ws rows p.
        3rd row k 2, lc2|1, k, rc1|2, [k] to end.
        5th row k 3, lc1|1, k, rc1|1, [k] to end.
    """
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(11, 6, pattern)
    visualize_knitGraph(knit_graph, "cables.html")
    # generator = Knitout_Generator(knit_graph)
    # generator.write_instructions("cables.k")

def test_cable_float():
    pattern = r"""
        all rs rows k 3, float, lc2|1, float, rc2|1, float, k 3.
        all ws rows p 3, float, p 3, float, p 3, float, p 3.
    """
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(15, 8, pattern, skipped=[3, 7, 11])
    visualize_knitGraph(knit_graph, "cables-float.html")
    generator = Knitout_Generator(knit_graph)
    generator.write_instructions("test_cable_float.k")

def test_cable_float_2():
    # pattern = r"""
    #     all rs row k 3, float, lc1|1, float, rc1|1, float, k 3.
    #     all ws rows p 3, float, p 2, float, p 2, float, p 3.
    # """
    pattern = r"""
        all rs rows k 3, k, lc1|1, k, rc1|1, k, k 3.
        all ws rows p.
    """
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(13, 8, pattern, )#skipped=[3, 6, 9])
    # visualize_knitGraph(knit_graph, "cables-float-2.html")
    generator = Knitout_Generator(knit_graph)
    generator.write_instructions("test_cable_float_2.k")


def test_lace():
    pattern = r"""
        all rs rows k, k2tog, yo 2, sk2po, yo 2, skpo, k. 
        all ws rows p 2, k, p 3, k, p 2.
    """
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(9, 6, pattern)
    # visualize_knitGraph(knit_graph, "lace.html")


def test_write_slipped_rib():
    rib_width = 1
    pattern = f"all rs rows k rib={rib_width}, [k rib, p rib] to last rib sts, k rib. all ws rows k rib, [slip rib, k rib] to last rib sts, p rib."
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(6, 3, pattern)
    visualize_knitGraph(knit_graph, "slipped_rib.html")


def test_leaf_float_lace():
    pattern = r"""1st row float, p, k 2, p, float, k, float, p, k 2, p, float, k 5, yo, s2kpo, yo, k 5, float, p, k 2, p, float.
        2nd row float, p, k 2, p, float, p, float, p, k 2, p, float, k 13, float, p, k 2, p, float.
        3rd row float, p, k 2, p, float, yo, k, yo, float, p, k 2, p, float, skpo, k 9, k2tog, float, p, k 2, p, float.
        4th row float, p, k 2, p, float, k 3, float, p, k 2, p, float, k 11, float, p, k 2, p, float.
        5th row float, p, k 2, p, float, k, yo, k, yo, k, float, p, k 2, p, float, skpo, k 7, k2tog, float, p, k 2, p, float.
        6th row float, p, k 2, p, float, k 5, float, p, k 2, p, float, k 9, float, p, k 2, p, float.
        7th row float, p, k 2, p, float, k 2, yo, k, yo, k 2, float, p, k 2, p, float, skpo, k 5, k2tog, float, p, k 2, p, float.
        8th row float, p, k 2, p, float, k 7, float, p, k 2, p, float, k 7, float, p, k 2, p, float.
        9th row float, p, k 2, p, float, k 3, yo, k, yo, k 3, float, p, k 2, p, float, skpo, k 3, k2tog, float, p, k 2, p, float.
        10th row float, p, k 2, p, float, k 9, float, p, k 2, p, float, k 5, float, p, k 2, p, float.
        11th row float, p, k 2, p, float, k 4, yo, k, yo, k 4, float, p, k 2, p, float, skpo, k, k2tog, float, p, k 2, p, float.
        12th row float, p, k 2, p, float, k 11, float, p, k 2, p, float, k 3, float, p, k 2, p, float.
        13th row float, p, k 2, p, float, k 5, yo, k, yo, k 5, float, p, k 2, p, float, s2kpo, float, p, k 2, p, float.
        14th row float, p, k 2, p, float, k 13, float, p, k 2, p, float, yo, k, yo, float, p, k 2, p, float.
        15th row float, p, k 2, p, float, skpo, k 9, k2tog, float, p, k 2, p, float, yo, k, yo, float, p, k 2, p, float.
        16th row float, p, k 2, p, float, k 11, float, p, k 2, p, float, k 3, float, p, k 2, p, float.
        17th row float, p, k 2, p, float, skpo, k 7, k2tog, float, p, k 2, p, float, k, yo, k, yo, k, float, p, k 2, p, float.
        18th row float, p, k 2, p, float, k 9, float, p, k 2, p, float, k 5, float, p, k 2, p, float.
        19th row float, p, k 2, p, float, skpo, k 5, k2tog, float, p, k 2, p, float, k 2, yo, k, yo, k 2, float, p, k 2, p, float.
        20th row float, p, k 2, p, float, k 7, float, p, k 2, p, float, k 7, float, p, k 2, p, float.
        21st row float, p, k 2, p, float, skpo, k 3, k2tog, float, p, k 2, p, float, k 3, yo, k, yo, k 3, float, p, k 2, p, float.
        22nd row float, p, k 2, p, float, k 5, float, p, k 2, p, float, k 9, float, p, k 2, p, float.
        23rd row float, p, k 2, p, float, skpo, k, k2tog, float, p, k 2, p, float, k 4, yo, k, yo, k 4, float, p, k 2, p, float.
        24th row float, p, k 2, p, float, k 3, float, p, k 2, p, float, k 11, float, p, k 2, p, float.
        25th row float, p, k 2, p, float, s2kpo, float, p, k 2, p, float, k 5, yo, k, yo, k 5, float, p, k 2, p, float."""
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(22, 25, pattern)
    visualize_knitGraph(knit_graph, "leaf-float.html")


def test_leaf_k_lace():
    pattern = r"""1st row [k] to end.
        2nd row k 3, k, p, k 2, p, k, k, k, p, k 2, p, k, k 13, k, p, k 2, p, k, k 3.
        3rd row k 3, k, p, k 2, p, k, k2tog, k 9, skpo, k, p, k 2, p, k, yo, k, yo, k, p, k 2, p, k, k 3.
        4th row k 3, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3.
        5th row k 3, k, p, k 2, p, k, k2tog, k 7, skpo, k, p, k 2, p, k, k, yo, k, yo, k, k, p, k 2, p, k, k 3.
        6th row k 3, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 3.
        7th row k 3, k, p, k 2, p, k, k2tog, k 5, skpo, k, p, k 2, p, k, k 2, yo, k, yo, k 2, k, p, k 2, p, k, k 3.
        8th row k 3, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 3.
        9th row k 3, k, p, k 2, p, k, k2tog, k 3, skpo, k, p, k 2, p, k, k 3, yo, k, yo, k 3, k, p, k 2, p, k, k 3.
        10th row k 3, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 3.
        11th row k 3, k, p, k 2, p, k, k2tog, k, skpo, k, p, k 2, p, k, k 4, yo, k, yo, k 4, k, p, k 2, p, k, k 3.
        12th row k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 3.
        13th row k 3, k, p, k 2, p, k, s2kpo, k, p, k 2, p, k, k 5, yo, k, yo, k 5, k, p, k 2, p, k, k 3.
        14th row k 3, k, p, k 2, p, k, k, k, p, k 2, p, k, k2tog, k 9, skpo, k, p, k 2, p, k, k 3.
        15th row k 3, k, p, k 2, p, k, k2tog, k 9, skpo, k, p, k 2, p, k, yo, k, yo, k, p, k 2, p, k, k 3.
        16th row k 3, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3.
        17th row k 3, k, p, k 2, p, k, k2tog, k 7, skpo, k, p, k 2, p, k, k, yo, k, yo, k, k, p, k 2, p, k, k 3.
        18th row k 3, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 3.
        19th row k 3, k, p, k 2, p, k, k2tog, k 5, skpo, k, p, k 2, p, k, k 2, yo, k, yo, k 2, k, p, k 2, p, k, k 3.
        20th row k 3, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 3.
        21st row k 3, k, p, k 2, p, k, k2tog, k 3, skpo, k, p, k 2, p, k, k 3, yo, k, yo, k 3, k, p, k 2, p, k, k 3.
        22nd row k 3, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 3.
        23rd row k 3, k, p, k 2, p, k, k2tog, k, skpo, k, p, k 2, p, k, k 4, yo, k, yo, k 4, k, p, k 2, p, k, k 3.
        24th row k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 3.
        25th row k 3, k, p, k 2, p, k, s2kpo, k, p, k 2, p, k, k 5, yo, k, yo, k 5, k, p, k 2, p, k, k 3."""
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(38, 25, pattern)
    visualize_knitGraph(knit_graph, "leaf-k.html")

def _test_leaf_k_lace():
    pattern = r"""1st row [k] to end.
        2nd row k 3, k, p, k 2, p, k, k, k, p, k 2, p, k, k 13, k, p, k 2, p, k, k 3.
        3rd row k 3, k, p, k 2, p, k, k2tog, yo, k 9, yo, skpo, k, p, k 2, p, k, k, k, p, k 2, p, k, k 3.
        4th row k 3, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3.
        5th row k 3, k, p, k 2, p, k, k2tog, yo, k 7, yo, skpo, k, p, k 2, p, k, k, k, k, k, p, k 2, p, k, k 3.
        6th row k 3, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 3.
        7th row k 3, k, p, k 2, p, k, k2tog, yo, k 5, yo, skpo, k, p, k 2, p, k, k 2, k, k 2, k, p, k 2, p, k, k 3.
        8th row k 3, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 3.
        9th row k 3, k, p, k 2, p, k, k2tog, yo, k 3, yo, skpo, k, p, k 2, p, k, k 3, k, k 3, k, p, k 2, p, k, k 3.
        10th row k 3, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 3.
        11th row k 3, k, p, k 2, p, k, k2tog, yo, k, yo, skpo, k, p, k 2, p, k, k 4, k, k 4, k, p, k 2, p, k, k 3.
        12th row k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 3.
        13th row k 3, k, p, k 2, p, k, yo, s2kpo, yo, k, p, k 2, p, k, k 5, k, k 5, k, p, k 2, p, k, k 3.
        14th row k 3, k, p, k 2, p, k, k, k, p, k 2, p, k, k2tog, yo, k 9, skpo, k, p, k 2, p, k, k 3.
        15th row k 3, k, p, k 2, p, k, k2tog, yo, k 9, yo, skpo, k, p, k 2, p, k, k, k, p, k 2, p, k, k 3.
        16th row k 3, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3.
        17th row k 3, k, p, k 2, p, k, k2tog, yo, k 7, yo, skpo, k, p, k 2, p, k, k, k, k, k, p, k 2, p, k, k 3.
        18th row k 3, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 3.
        19th row k 3, k, p, k 2, p, k, k2tog, yo, k 5, yo, skpo, k, p, k 2, p, k, k 2, k, k 2, k, p, k 2, p, k, k 3.
        20th row k 3, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 7, k, p, k 2, p, k, k 3.
        21st row k 3, k, p, k 2, p, k, k2tog, yo, k 3, yo, skpo, k, p, k 2, p, k, k 3, k, k 3, k, p, k 2, p, k, k 3.
        22nd row k 3, k, p, k 2, p, k, k 9, k, p, k 2, p, k, k 5, k, p, k 2, p, k, k 3.
        23rd row k 3, k, p, k 2, p, k, k2tog, yo, k, yo, skpo, k, p, k 2, p, k, k 4, k, k 4, k, p, k 2, p, k, k 3.
        24th row k 3, k, p, k 2, p, k, k 11, k, p, k 2, p, k, k 3, k, p, k 2, p, k, k 3.
        25th row k 3, k, p, k 2, p, k, yo, s2kpo, yo, k, p, k 2, p, k, k 5, k, k 5, k, p, k 2, p, k, k 3."""
    compiler = Knitspeak_Compiler()
    knit_graph = compiler.compile(38, 25, pattern)
    visualize_knitGraph(knit_graph, "leaf-k.html")

if __name__ == "__main__":
    # test_stst()
    # test_rib()
    # test_write_slipped_rib()
    # test_cable()
    
    # test_cable_float()
    # test_cable_float_2()
    
    # test_skipped_4()    
    # test_skipped_2()
    # test_leaf_float_lace()

    # test_lace()
    # test_skipped()
    # test_leaf_k_lace()

    
