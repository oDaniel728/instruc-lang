
class SyntaxKeywords():
    NEW = "new";
    USE = "use";
    END = "end";
    RET = "ret";
    REQ = "req";
    STACK = "stack";
    LABEL = "def";

    LOAD = "load";
    KILL = "kill";
    CALL = "call";
    REQACESSOR = "@";

class SyntaxRulePatterns():
    LABEL_NAME = r"[a-zA-Z_\@][a-zA-Z0-9_]*";
    STACK_NAME = r"(?:[a-zA-Z0-9_\$]+)|(?:\.\.)|\.";
    STACK_INDEX = r"(?:\d+)|\-";
    STACK_ITEM_SELECTION = fr"({STACK_NAME}):({STACK_INDEX})";
    STACK_OPT_ITEM_SELECTION = fr"({STACK_NAME})(?::({STACK_INDEX}))?";
    OPT_STACK_ITEM_SELECTION = fr"({STACK_NAME})?:({STACK_INDEX})";
    METHOD_NAME = r"\w+\@\w+";

class SyntaxRegularExpressionPatterns():
    DEFINE_LABEL = fr"{SyntaxKeywords.NEW}\s+{SyntaxKeywords.LABEL}\s+({SyntaxRulePatterns.LABEL_NAME})";
    USE_LABEL = fr"{SyntaxKeywords.USE}\s+{SyntaxKeywords.LABEL}\s+({SyntaxRulePatterns.LABEL_NAME})";
    END_LABEL = fr"{SyntaxKeywords.END}\s+{SyntaxKeywords.LABEL}";

    DEFINE_STACK = fr"{SyntaxKeywords.NEW}\s+{SyntaxKeywords.STACK}\s+({SyntaxRulePatterns.STACK_NAME})";
    USE_STACK = fr"{SyntaxKeywords.USE}\s+{SyntaxKeywords.STACK}\s+({SyntaxRulePatterns.STACK_NAME})";
    END_STACK = fr"{SyntaxKeywords.END}\s+{SyntaxKeywords.STACK}\s+((?:{SyntaxRulePatterns.STACK_NAME})|\*)";

    RETURN = fr"{SyntaxKeywords.RET}\s+(.+)";

    LOAD = fr"^{SyntaxKeywords.LOAD}\s+(\d+)$";
    KILL = fr"^{SyntaxKeywords.KILL}\s+(\d+)$";
    KILLI = fr"^{SyntaxKeywords.KILL}\s+i\s+(\d+)$";
    CALL  = fr"{SyntaxKeywords.CALL}\s+({SyntaxRulePatterns.METHOD_NAME})";

    # libformat = lib@method
    LIBFORMAT = fr"(\w+){SyntaxKeywords.REQACESSOR}(\w+)";

    REQUIREMENT = fr"{SyntaxKeywords.REQ}\s+(\w+)";
