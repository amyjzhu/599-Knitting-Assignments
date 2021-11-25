"""Compiler code for converting knitspeak AST to knitgraph"""
from typing import List, Dict, Union, Tuple, Set

from knit_graphs.Knit_Graph import Knit_Graph
from knit_graphs.Yarn import Yarn
from knitspeak_compiler.knitspeak_interpreter.knitspeak_interpreter import KnitSpeak_Interpreter
from knitspeak_compiler.knitspeak_interpreter.cable_definitions import Cable_Definition
from knitspeak_compiler.knitspeak_interpreter.closures import Num_Closure, Iterator_Closure
from knitspeak_compiler.knitspeak_interpreter.stitch_definitions import Stitch_Definition


class Knitspeak_Compiler:
    """
    A class used to compile knit graphs from knitspeak
    """

    def __init__(self):
        self._parser = KnitSpeak_Interpreter()
        self.parse_results: List[Dict[str, Union[List[int, Num_Closure, Iterator_Closure], List[tuple]]]] = []
        self.course_ids_to_operations: Dict[int, List[tuple]] = {}
        self.knit_graph = Knit_Graph()
        self.yarn = Yarn("yarn", self.knit_graph)
        self.knit_graph.add_yarn(self.yarn)
        self.last_course_loop_ids: List[int] = []
        self.cur_course_loop_ids: List[int] = []
        self.cur_course_skipped_loops: List[int] = []
        self.last_course_skipped_loops: List[int] = []
        self.current_row = 0 
        self.loop_ids_consumed_by_current_course: Set[int] = set()

    def _increment_current_row(self):
        """
        Increments the current row by 1 and manages its state in the symbol table
        """
        self.current_row += 1
        self._parser.parser.symbolTable["current_row"] = self.current_row

    @property
    def _working_ws(self) -> bool:
        """
        :return: true if currently compiling a wrong-side row
        """
        return self.current_row % 2 == 0

    def compile(self, starting_width: int, row_count: int, pattern: str, patternIsFile: bool = False, skipped: List[int] = []) -> Knit_Graph:
        """
        Populates the knit_graph based on the compiled instructions. May throw errors from compilation
        :param row_count: the number of rows to knit before completing, pattern may repeat or be incomplete
        :param starting_width: the number of loops used to create the 0th course
        :param pattern: the pattern as a string or in a file
        :param patternIsFile: True if pattern is provided in a file
        :return: the resulting compiled knit graph
        """
        self.parse_results = self._parser.parse(pattern, patternIsFile)
        self._organize_courses()
        self.populate_0th_course(starting_width, skipped)
        while self.current_row < row_count:
            for course_id in sorted(self.course_ids_to_operations):
                self._increment_current_row()
                assert self.current_row % course_id == 0
                course_instructions = self.course_ids_to_operations[course_id]
                while len(self.loop_ids_consumed_by_current_course) < len(self.last_course_loop_ids):
                    print("====")
                    print("self.loop_ids_consumed_by_current_course ", self.loop_ids_consumed_by_current_course)
                    print("self.last_course_loop_ids", self.last_course_loop_ids)
                    print("====")
                    for instruction in course_instructions:
                        print(instruction)
                        self._process_instruction(instruction)
                        if len(self.loop_ids_consumed_by_current_course) == len(self.last_course_loop_ids):
                            break
                self.last_course_loop_ids = self.cur_course_loop_ids
                self.last_course_skipped_loops = self.cur_course_skipped_loops
                print("!!!AND!!!")
                print(self.last_course_loop_ids)
                self.cur_course_loop_ids = []
                self.cur_course_skipped_loops = []
                self.loop_ids_consumed_by_current_course = set()
                if self.current_row == row_count:
                    break
        return self.knit_graph

    def populate_0th_course(self, starting_width: int, skipped: List[int] = []):
        """
        Populates the first course of the knitgraph with starting_width loops.
        Adds loop_ids in yarn-wise order to self.last_course_loop_ids
        :param starting_width: the number of loops to create
        """
        for i in range(0, starting_width):
            # THIS IS THE WORST LMAO CAUSING ALL MY ISSUES!!!!!!!!!!
            # why would you do thisssssssssssssssssssss
            # if we start with a float, we need a way to remove one of these...
            # need to figure out what... ahhhh
            if skipped.__contains__(i):
                _, (loop_id, loop) = self.yarn.add_skip_loops(0)
                self.last_course_skipped_loops.append(loop_id)

            else:
                loop_id, loop = self.yarn.add_loop_to_end()
                # One of the assumptions means I must do this, but... it feels so dirty
                # self.last_course_loop_ids.append(loop_id)
            self.knit_graph.add_loop(loop)
            self.last_course_loop_ids.append(loop_id)


    def _organize_courses(self):
        """
        takes the parser results and organizes the course instructions by their course ids.
        raises two possible errors
         If a course is defined more than once, raise an error documenting the course_id
         If a course between 1 and the maximum course is not defined, raise an error documenting the course_id
        Note that all closures in these ids are executed before the row operations (may cause implementation confusion)
        """
        for instructions in self.parse_results:
            course_ids = instructions["courseIds"]
            course_instructions = instructions["stitch-operations"]
            for course_id in course_ids:
                if isinstance(course_id, Num_Closure):
                    course_id = course_id.to_int()  # converts any variable numbers to their current state
                    assert course_id not in self.course_ids_to_operations, f"KnitSpeak Error: Course {course_id} is defined more than once"
                    self.course_ids_to_operations[course_id] = course_instructions
                elif isinstance(course_id, Iterator_Closure):  # closes iteration over variable numbers
                    sub_courses = course_id.to_int_list()
                    for sub_id in sub_courses:
                        assert sub_id not in self.course_ids_to_operations, f"KnitSpeak Error: Course {sub_id} is defined more than once"
                        self.course_ids_to_operations[sub_id] = course_instructions
                else:  # course_id is integer
                    assert course_id not in self.course_ids_to_operations, f"KnitSpeak Error: Course {course_id} is defined more than once"
                    self.course_ids_to_operations[course_id] = course_instructions

        max_course = max(*self.course_ids_to_operations)
        if "all_rs" in self._parser.parser.symbolTable:
            course_instructions = self.course_ids_to_operations[1]
            for course_id in range(3, max_course + 1, 2):
                if course_id not in self.course_ids_to_operations:
                    self.course_ids_to_operations[course_id] = course_instructions
                else:
                    print(f"KnitSpeak Warning: course {course_id} overrides rs-instructions")
        if "all_ws" in self._parser.parser.symbolTable:
            course_instructions = self.course_ids_to_operations[2]
            for course_id in range(4, max_course + 1, 2):
                if course_id not in self.course_ids_to_operations:
                    self.course_ids_to_operations[course_id] = course_instructions
                else:
                    print(f"KnitSpeak Warning: course {course_id} overrides ws-instructions")

        for course_id in range(1, max_course + 1):
            assert course_id in self.course_ids_to_operations, f"KnitSpeak Error: Course {course_id} is undefined"

        if max_course % 2 == 1 and "all_ws" in self._parser.parser.symbolTable:  # ends on rs row
            self.course_ids_to_operations[max_course + 1] = self.course_ids_to_operations[2]

    def _process_instruction(self, instruction: Tuple[Union[tuple, Stitch_Definition, Cable_Definition, list],
                                                      Tuple[bool, int]]):
        """
        :param instruction: A tuple with the knitting instructions and information about how to repeat them
        instruction[0] can be a stitch definition, cable definition, or a list of instruction tuples
        instruction[1] is a tuple with a boolean and an int.
         If the boolean is true, then the integer represents the number of times to repeat the instructions
         If the boolean is false, then the integer represents the number of loops left after executing the instructions
        :return:
        """
        action = instruction[0]
        is_stitch = isinstance(action, Stitch_Definition)
        is_cable = isinstance(action, Cable_Definition)
        is_list = type(action) is list
        static_repeats = instruction[1][0]
        repeats = 1
        if static_repeats:
            repeats = instruction[1][1]
            if isinstance(repeats, Num_Closure):
                repeats = repeats.to_int()
        remaining_loops = 0
        if not static_repeats:
            remaining_loops = instruction[1][1]
            if isinstance(remaining_loops, Num_Closure):
                remaining_loops = remaining_loops.to_int()

        def execute_instructions():
            """
            Executes the action according to its type
            """
            if is_stitch:
                self._process_stitch(action)
            elif is_cable:
                self._process_cable(action)
            elif is_list:
                self._process_list(action)
            else:
                self._process_instruction(action)

        if not static_repeats:  # need to iterate until remaining loops is left
            while (len(self.last_course_loop_ids) - len(self.loop_ids_consumed_by_current_course)) > remaining_loops:
                print("AGH")
                print(self.last_course_loop_ids)
                print(self.loop_ids_consumed_by_current_course)
                print("AGHHH")
                execute_instructions()
            assert remaining_loops == (len(self.last_course_loop_ids) - len(self.loop_ids_consumed_by_current_course))
        else:
            for _ in range(0, repeats):
                execute_instructions()

    def _process_stitch(self, stitch_def: Stitch_Definition, flipped_by_cable=False):
        """
        Uses a stitch definition and compiler state to generate a new loop and connect it to the prior course.
        May throw two compiler errors.
         if there is no loop at the parent offsets of the stitch, then throw an error reporting the missing index
         if a parent loop has already been consumed, then throw an error reporting the misused parent loop
        :param flipped_by_cable: if True, implies that this stitch came from a cable and has been flipped appropriately
        :param stitch_def: the stitch definition used to connect the new loop
        """
        if self._working_ws and not flipped_by_cable:  # flips stitches following hand-knitting conventions
            stitch_def = stitch_def.copy_and_flip()
        course_index = len(self.cur_course_loop_ids)
        print("current ", self.cur_course_loop_ids)
        print("last", self.last_course_loop_ids)
        # it's possible that the parent is a float, but that shouldn't be the case 
        # problem is that a float is never consumed. 
        # so we need to check float "children" and yo "children"
        prior_course_index = (len(self.last_course_loop_ids) - 1) - course_index

        assert(prior_course_index >= 0)

        if stitch_def.child_loops == 0 and stitch_def.offset_to_parent_loops == []:
            # it's a skipped stitch/float
            loops, (loop_id, loop) = self.yarn.add_skip_loops(extra_skips=0)
            for int_loop_id, int_loop in loops: 
                # TODO: render this unnecessary 
                # potential_parent = self.last_course_loop_ids[prior_course_index]
                # if loop_id == 7:
                #     self.last_course_loop_ids.remove(potential_parent)
                #     print("EEEEE")

                self.knit_graph.add_loop(int_loop)
                print("Adding ", int_loop_id)
                # TODO: should i do something extra here? with checking parents
            
            # IT's not a consumable loop!
            self.cur_course_loop_ids.append(loop_id)
            self.cur_course_skipped_loops.append(loop_id)
            # I should remove this because checks against the consumed loops... or should I? it's unusable
            self.knit_graph.add_loop(loop)
            print("Adding ", loop_id)
            print("IN SKIP")
            
            # it's possible our parent is a float. In that case, make sure it's consumed.
            parent_loop = self.last_course_loop_ids[prior_course_index]
            if self.last_course_skipped_loops.__contains__(parent_loop):
                # "consume" the parent
                self.loop_ids_consumed_by_current_course.add(parent_loop)


        elif stitch_def.child_loops == 1:
            # Todo: Implement processing the stitch into the knitgraph
            #  add a new loop to the end of  self.yarn and add it to the self.knitgraph
            #  iterate over the stitch's parent offsets in their stack order
            #   the index of the parent_loop in self.last_course_loop_ids will be the prior_course_index plus the offset
            #   mark the parent_loop as "consumed" by putting it in the loop_ids_consumed_by_current_course set
            #   then connect that parent loop to the new child_loop given the stitch information in the stitch_def
            #  add the newly created loop to the end of self.cur_course_loop_ids

            # add new loop to end of yarn and to knitgraph
            loop_id, loop = self.yarn.add_loop_to_end()
            self.knit_graph.add_loop(loop)

            if stitch_def.offset_to_parent_loops == []:
                # in a yarnover, we also want to check for parent floats
                # it's possible our parent is a float. In that case, make sure it's consumed.
                parent_loop = self.last_course_loop_ids[prior_course_index]
                if self.last_course_skipped_loops.__contains__(parent_loop):
                    # "consume" the parent
                    self.loop_ids_consumed_by_current_course.add(parent_loop)


            # enumerate over parents
            for stack, parent in enumerate(stitch_def.offset_to_parent_loops):
                print("loop ids consumed by current course", self.loop_ids_consumed_by_current_course)
                parent_loop = self.last_course_loop_ids[prior_course_index + parent]
                print(parent_loop, " by ", loop_id)
                print("last course loop ids", self.last_course_loop_ids)
                print("current course loop ids", self.cur_course_loop_ids)
                print(prior_course_index)
                if parent_loop is None:
                    raise IndexError("There is no such parent loop at index " % prior_course_index + parent)
                if self.loop_ids_consumed_by_current_course.__contains__(parent_loop):
                    raise ValueError("Parent loop has already been consumed")

                self.loop_ids_consumed_by_current_course.add(parent_loop)

                # now determine what we need to make a new connection 
                self.knit_graph.connect_loops(parent_loop, loop_id, pull_direction = stitch_def.pull_direction, \
                    stack_position = stack, depth = stitch_def.cabling_depth, parent_offset = parent)

            # add to current course loops
            self.cur_course_loop_ids.append(loop_id)

        else:  # slip statement
            assert len(stitch_def.offset_to_parent_loops) == 1, "Cannot slip multiple loops"
            for stack_position, parent_offset in enumerate(stitch_def.offset_to_parent_loops):
                parent_index = (len(self.last_course_loop_ids) - 1) - course_index + parent_offset
                assert 0 <= parent_index < len(self.last_course_loop_ids), f"Knitspeak Error: Cannot find a loop at index {parent_index}"
                parent_loop_id = self.last_course_loop_ids[parent_index]
                assert parent_loop_id not in self.loop_ids_consumed_by_current_course, \
                    f"Knitspeak Error: Loop {parent_loop_id} has already been used"
                self.loop_ids_consumed_by_current_course.add(parent_loop_id)
                self.cur_course_loop_ids.append(parent_loop_id)

    def _process_cable(self, cable_def: Cable_Definition):
        """
        Uses a cable definition and compiler state to generate and connect a cable
        :param cable_def: the cable definition used to connect the cable into the knitgraph
        """
        if self._working_ws:  # flips cable by hand-knitting convention
            cable_def = cable_def.copy_and_flip()
        stitch_definitions = cable_def.stitch_definitions()
        for stitch_definition in stitch_definitions:
            self._process_stitch(stitch_definition, flipped_by_cable=True)

    def _process_list(self, action: List[tuple]):
        """
        Processes actions in a list of actions
        :param action: the list of actions
        """
        for sub_action in action:
            self._process_instruction(sub_action)
