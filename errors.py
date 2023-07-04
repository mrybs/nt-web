from colorama import Fore as fg, Back as bg, Style as st, init


init()


def restyle(data: str) -> str:
    """

    function restyle

    data (str): source string
    rvalue (str): re-styled string

    Makes parse error messages prettier

    """
    data = data.replace("Tcomment", "comment declaration")
    data = data.replace("Tdoctype", "keyword \"doctype\"")
    data = data.replace("Tntml", "keyword \"ntml\"")
    data = data.replace("Timport", "keyword \"import\"")
    data = data.replace("Ttitle", "keyword \"title\"")
    data = data.replace("Ttagname", "tag name")
    data = data.replace("Tverfloat", "version declaration")
    data = data.replace("Tescape", "escape sequence")
    data = data.replace("Tany", "any other content")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tfloat", "float")
    data = data.replace("Tint", "integer")
    data = data.replace("Tstr", "string")
    data = data.replace("Sdoctype", "doctype declaration")
    data = data.replace("Sbody", "tag body")
    data = data.replace("Sexpr", "expression")
    data = data.replace("Sassign", "assignment")
    data = data.replace("Sprops", "tag properties")
    data = data.replace("Stag", "tag declaration")
    data = data.replace("Stitle", "title declaration")
    data = data.replace("Simport", "import declaration")
    data = data.split(" but found ", 1)[0]
    if " or " in data:
        rdata = data.split(" or ")
        data = ", ".join(rdata[:-1])
        data += " or "+rdata[-1]
    return data


def print_parse_error(pos, file, dt):
    D = 2
    print()
    nl, ns = pos
    print("Error while parsing file %s," % file)
    print("At line "+st.BRIGHT+str(nl)+st.NORMAL+", column "+st.BRIGHT+str(ns)+st.NORMAL+":")
    with open(file, "rt") as f:
        fd = f.read()
        ln = fg.YELLOW+"│   "+fg.RESET + fd.split("\n")[nl - 1].strip()
        sd = len(fd.split("\n")[nl - 1]) - len(fd.split("\n")[nl - 1].strip()) + 2
        ln = ln[:ns+sd]+fg.RED+ln[ns+sd]+fg.RESET+ln[ns+sd+1:]
        print(ln)
    print(fg.YELLOW+"│   "+fg.RESET + " " * (ns - sd + 2) + fg.YELLOW+"▲")
    print("╰───" + "─" * (ns - sd + 2) + "╯"+fg.RESET)
    print(restyle(dt.split("=> ", 1)[1]))
    print()