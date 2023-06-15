# Generated by the Waxeye Parser Generator - version 0.8.0
# www.waxeye.org

from waxeye import Edge, State, FA, WaxeyeParser

class FormulaParser (WaxeyeParser):
    start = 0
    eof_check = True
    automata = [FA("start", [State([Edge(59, 1, False)], False),
            State([Edge(1, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("vChop_Expr", [State([Edge(2, 1, False)], False),
            State([Edge(48, 2, True)], True),
            State([Edge(1, 1, False)], False)], FA.PRUNE),
        FA("hChop_Expr", [State([Edge(3, 1, False)], False),
            State([Edge(49, 2, True)], True),
            State([Edge(2, 1, False)], False)], FA.PRUNE),
        FA("iff_Expr", [State([Edge(4, 1, False)], False),
            State([Edge(51, 2, True)], True),
            State([Edge(3, 1, False)], False)], FA.PRUNE),
        FA("implies_Expr", [State([Edge(5, 1, False)], False),
            State([Edge(50, 2, True)], True),
            State([Edge(4, 1, False)], False)], FA.PRUNE),
        FA("or_Expr", [State([Edge(6, 1, False)], False),
            State([Edge(52, 2, True)], True),
            State([Edge(5, 1, False)], False)], FA.PRUNE),
        FA("and_Expr", [State([Edge(7, 1, False)], False),
            State([Edge(53, 2, True)], True),
            State([Edge(6, 1, False)], False)], FA.PRUNE),
        FA("unaryFormula", [State([Edge(8, 1, False),
                Edge(9, 1, False),
                Edge(10, 1, False),
                Edge(11, 1, False)], False),
            State([], True)], FA.PRUNE),
        FA("not_Expr", [State([Edge(42, 1, True)], False),
            State([Edge(11, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("forall_Expr", [State([Edge(37, 1, True)], False),
            State([Edge(22, 2, False)], False),
            State([Edge(39, 3, True)], False),
            State([Edge(17, 4, False)], False),
            State([Edge(41, 5, True)], False),
            State([Edge(11, 6, False)], False),
            State([], True)], FA.LEFT),
        FA("exists_Expr", [State([Edge(38, 1, True)], False),
            State([Edge(22, 2, False)], False),
            State([Edge(39, 3, True)], False),
            State([Edge(17, 4, False)], False),
            State([Edge(41, 5, True)], False),
            State([Edge(11, 6, False)], False),
            State([], True)], FA.LEFT),
        FA("atom", [State([Edge(36, 1, False),
                Edge(35, 1, False),
                Edge(13, 1, False),
                Edge(14, 1, False),
                Edge(15, 1, False),
                Edge(40, 1, False),
                Edge(20, 1, False),
                Edge(21, 1, False),
                Edge(57, 2, False),
                Edge(12, 1, False)], False),
            State([], True),
            State([Edge(1, 3, False)], False),
            State([Edge(58, 1, False)], False)], FA.PRUNE),
        FA("somewhere_Expr", [State([Edge(55, 1, True)], False),
            State([Edge(1, 2, False)], False),
            State([Edge(56, 3, True)], False),
            State([], True)], FA.LEFT),
        FA("length_Comparisson", [State([Edge(33, 1, True)], False),
            State([Edge(16, 2, False)], False),
            State([Edge(19, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("height_Comparisson", [State([Edge(34, 1, True)], False),
            State([Edge(16, 2, False)], False),
            State([Edge(18, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("car_Comparisson", [State([Edge(30, 1, False),
                Edge(22, 1, False)], False),
            State([Edge(47, 2, True)], False),
            State([Edge(30, 3, False),
                Edge(22, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("comparator", [State([Edge(43, 1, False),
                Edge(44, 1, False),
                Edge(45, 1, False),
                Edge(46, 1, False),
                Edge(47, 1, False)], False),
            State([], True)], FA.PRUNE),
        FA("type", [State([Edge(27, 1, False),
                Edge(28, 1, False),
                Edge(29, 1, False)], False),
            State([], True)], FA.PRUNE),
        FA("int_Value", [State([Edge(22, 1, False),
                Edge(24, 1, False)], False),
            State([Edge(54, 2, False)], True),
            State([Edge(22, 1, False),
                Edge(24, 1, False)], False)], FA.PRUNE),
        FA("real_Value", [State([Edge(22, 1, False),
                Edge(25, 1, False)], False),
            State([Edge(54, 2, False)], True),
            State([Edge(22, 1, False),
                Edge(25, 1, False)], False)], FA.PRUNE),
        FA("re_Expr", [State([Edge(31, 1, True)], False),
            State([Edge(57, 2, False)], False),
            State([Edge(30, 3, False),
                Edge(22, 3, False)], False),
            State([Edge(58, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("cl_Expr", [State([Edge(32, 1, True)], False),
            State([Edge(57, 2, False)], False),
            State([Edge(30, 3, False),
                Edge(22, 3, False)], False),
            State([Edge(58, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("name", [State([Edge(61, 1, False)], False),
            State([Edge([(65, 90), (97, 122)], 2, False)], False),
            State([Edge(23, 2, False),
                Edge(59, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("name_Character", [State([Edge([(65, 90), (97, 122)], 1, False),
                Edge([(48, 57)], 1, False),
                Edge(["-", "_"], 1, False)], False),
            State([], True)], FA.PRUNE),
        FA("int", [State([Edge([(48, 57)], 1, False)], False),
            State([Edge([(48, 57)], 1, False),
                Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("float", [State([Edge([(48, 57)], 1, False)], False),
            State([Edge([(48, 57)], 1, False),
                Edge(".", 2, False),
                Edge(59, 4, False)], False),
            State([Edge([(48, 57)], 3, False)], False),
            State([Edge([(48, 57)], 3, False),
                Edge(59, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("keyword", [State([Edge(27, 1, False),
                Edge(28, 1, False),
                Edge(29, 1, False),
                Edge(30, 1, False),
                Edge(31, 1, False),
                Edge(32, 1, False),
                Edge(33, 1, False),
                Edge(34, 1, False),
                Edge(35, 1, False),
                Edge(36, 1, False),
                Edge(37, 1, False),
                Edge(38, 1, False),
                Edge(39, 1, False),
                Edge(40, 1, False)], False),
            State([], True)], FA.LEFT),
        FA("cARS", [State([Edge("c", 1, True)], False),
            State([Edge("a", 2, True)], False),
            State([Edge("r", 3, True)], False),
            State([Edge("s", 4, True)], False),
            State([Edge(62, 5, False)], False),
            State([Edge(59, 6, False)], False),
            State([], True)], FA.LEFT),
        FA("eXTS", [State([Edge("e", 1, True)], False),
            State([Edge("x", 2, True)], False),
            State([Edge("t", 3, True)], False),
            State([Edge("s", 4, True)], False),
            State([Edge(63, 5, False)], False),
            State([Edge(59, 6, False)], False),
            State([], True)], FA.LEFT),
        FA("lANES", [State([Edge("l", 1, True)], False),
            State([Edge("a", 2, True)], False),
            State([Edge("n", 3, True)], False),
            State([Edge("e", 4, True)], False),
            State([Edge("s", 5, True)], False),
            State([Edge(64, 6, False)], False),
            State([Edge(59, 7, False)], False),
            State([], True)], FA.LEFT),
        FA("eGO", [State([Edge("e", 1, True)], False),
            State([Edge("g", 2, True)], False),
            State([Edge("o", 3, True)], False),
            State([Edge(65, 4, False)], False),
            State([Edge(59, 5, False)], False),
            State([], True)], FA.LEFT),
        FA("rE", [State([Edge("r", 1, True)], False),
            State([Edge("e", 2, True)], False),
            State([Edge(66, 3, False)], False),
            State([Edge(59, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("cL", [State([Edge("c", 1, True)], False),
            State([Edge("l", 2, True)], False),
            State([Edge(67, 3, False)], False),
            State([Edge(59, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("lENGTH", [State([Edge("l", 1, True)], False),
            State([Edge("e", 2, True)], False),
            State([Edge("n", 3, True)], False),
            State([Edge("g", 4, True)], False),
            State([Edge("t", 5, True)], False),
            State([Edge("h", 6, True)], False),
            State([Edge(68, 7, False)], False),
            State([Edge(59, 8, False)], False),
            State([], True)], FA.LEFT),
        FA("hEIGHT", [State([Edge("h", 1, True)], False),
            State([Edge("e", 2, True)], False),
            State([Edge("i", 3, True)], False),
            State([Edge("g", 4, True)], False),
            State([Edge("h", 5, True)], False),
            State([Edge("t", 6, True)], False),
            State([Edge(69, 7, False)], False),
            State([Edge(59, 8, False)], False),
            State([], True)], FA.LEFT),
        FA("fALSE", [State([Edge("f", 1, True)], False),
            State([Edge("a", 2, True)], False),
            State([Edge("l", 3, True)], False),
            State([Edge("s", 4, True)], False),
            State([Edge("e", 5, True)], False),
            State([Edge(70, 6, False)], False),
            State([Edge(59, 7, False)], False),
            State([], True)], FA.LEFT),
        FA("tRUE", [State([Edge("t", 1, True)], False),
            State([Edge("r", 2, True)], False),
            State([Edge("u", 3, True)], False),
            State([Edge("e", 4, True)], False),
            State([Edge(71, 5, False)], False),
            State([Edge(59, 6, False)], False),
            State([], True)], FA.LEFT),
        FA("fORALL", [State([Edge("f", 1, True)], False),
            State([Edge("o", 2, True)], False),
            State([Edge("r", 3, True)], False),
            State([Edge("a", 4, True)], False),
            State([Edge("l", 5, True)], False),
            State([Edge("l", 6, True)], False),
            State([Edge(72, 7, False)], False),
            State([Edge(59, 8, False)], False),
            State([], True)], FA.LEFT),
        FA("eXISTS", [State([Edge("e", 1, True)], False),
            State([Edge("x", 2, True)], False),
            State([Edge("i", 3, True)], False),
            State([Edge("s", 4, True)], False),
            State([Edge("t", 5, True)], False),
            State([Edge("s", 6, True)], False),
            State([Edge(73, 7, False)], False),
            State([Edge(59, 8, False)], False),
            State([], True)], FA.LEFT),
        FA("iN", [State([Edge("i", 1, True)], False),
            State([Edge("n", 2, True)], False),
            State([Edge(74, 3, False)], False),
            State([Edge(59, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("fREE", [State([Edge("f", 1, True)], False),
            State([Edge("r", 2, True)], False),
            State([Edge("e", 3, True)], False),
            State([Edge("e", 4, True)], False),
            State([Edge(75, 5, False)], False),
            State([Edge(59, 6, False)], False),
            State([], True)], FA.LEFT),
        FA("dOT", [State([Edge(".", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("nOT", [State([Edge("!", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("gEQ", [State([Edge(">", 1, True)], False),
            State([Edge("=", 2, True)], False),
            State([Edge(59, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("lEQ", [State([Edge("<", 1, True)], False),
            State([Edge("=", 2, True)], False),
            State([Edge(59, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("lESS", [State([Edge("<", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("gREATER", [State([Edge(">", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("eQ", [State([Edge("=", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("vCHOP", [State([Edge("/", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("hCHOP", [State([Edge(";", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("iMPLIES", [State([Edge("-", 1, True)], False),
            State([Edge("-", 2, True)], False),
            State([Edge(">", 3, True)], False),
            State([Edge(59, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("iFF", [State([Edge("<", 1, True)], False),
            State([Edge("-", 2, True)], False),
            State([Edge(">", 3, True)], False),
            State([Edge(59, 4, False)], False),
            State([], True)], FA.LEFT),
        FA("oR", [State([Edge("|", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("aND", [State([Edge("&", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("pLUS", [State([Edge("+", 1, True)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.LEFT),
        FA("bSWHERE", [State([Edge("<", 1, True)], False),
            State([Edge("@", 2, True)], False),
            State([Edge(59, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("eSWHERE", [State([Edge("@", 1, True)], False),
            State([Edge(">", 2, True)], False),
            State([Edge(59, 3, False)], False),
            State([], True)], FA.LEFT),
        FA("lP", [State([Edge("(", 1, False)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.VOID),
        FA("rP", [State([Edge(")", 1, False)], False),
            State([Edge(59, 2, False)], False),
            State([], True)], FA.VOID),
        FA("space", [State([Edge([(9, 10), "\r", " "], 0, False),
                Edge(60, 0, False)], True)], FA.VOID),
        FA("comment", [State([Edge("/", 1, False)], False),
            State([Edge("*", 2, False)], False),
            State([Edge(76, 3, False),
                Edge("*", 4, False)], False),
            State([Edge(-1, 2, False)], False),
            State([Edge("/", 5, False)], False),
            State([], True)], FA.VOID),
        FA("", [State([Edge(26, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge(23, 1, False)], False),
            State([], True)], FA.NEG),
        FA("", [State([Edge("*", 1, False)], False),
            State([Edge("/", 2, False)], False),
            State([], True)], FA.NEG)]

    def __init__(self):
        WaxeyeParser.__init__(self, FormulaParser.start, FormulaParser.eof_check, FormulaParser.automata)

