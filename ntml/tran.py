"""

ntml/tran.py

makes HTML code from AST

"""


from ntml.ntml_parser import *
from typing import *
import sys


def tran_props(props: dict) -> str:
    """
    Makes HTML in-tag attributes from NTML properties
    :param props: dictionary with properties
    :type props: dict
    """
    ret: str = ""

    for i in props.keys():
        try:
            if '"' not in props[i]:
                ret += " "+i+"=\""+eval(props[i])+"\""
            else:
                ret += " "+i+"=\""+props[i].replace('"', '')+"\""
        except SyntaxError:
            ret += " "+i+"=\""+props[i].replace('"', '')+"\""
        except NameError:
            ret += " "+i+"=\""+props[i].replace('"', '')+"\""
        except TypeError:
            ret += " "+i+"=\""+props[i].replace('"', '')+"\""
    
    return ret


rels: dict = {
    "style": "stylesheet",
    "favicon": "icon",
    "script": "script"
}

MEALS: dict = {
    "body":        {"tag": "body"},
    "bold":        {"tag": "b"},
    "b":           {"tag": "b"},
    "italic":      {"tag": "i"},
    "i":           {"tag": "i"},
    "underline":   {"tag": "u"},
    "u":           {"tag": "u"},
    "strikeout":   {"tag": "s"},
    "s":           {"tag": "s"},
    "block":       {"tag": "div"},
    "bl":          {"tag": "div"},
    "text":        {"tag": "p"},
    "t":           {"tag": "p"},
    "input":       {"tag": "input"},
    "inp":         {"tag": "input"},
    "h1":          {"tag": "h1"},
    "h2":          {"tag": "h2"},
    "h3":          {"tag": "h3"},
    "h4":          {"tag": "h4"},
    "ht1":         {"tag": "h1"},
    "ht2":         {"tag": "h2"},
    "ht3":         {"tag": "h3"},
    "ht4":         {"tag": "h4"},
    "link":        {"tag": "a"},
    "ln":          {"tag": "a"},
    "image":       {"tag": "image"},
    "img":         {"tag": "image"},
    "cd":          {"tag": "div"},
    "code":        {"tag": "div"},
    "form":        {"tag": "form"},
    "f":           {"tag": "form"},
    "table":       {"tag": "table"},
    "tab":         {"tag": "table"},
    "tr":          {"tag": "tr"},
    "td":          {"tag": "td"},
    "script":      {"tag": "script"},
    "scr":         {"tag": "script"},
    "btn":         {"tag": "button"},
    "button":      {"tag": "button"},
    "holder":      {"tag": "div"},
    "hld":         {"tag": "div"},
    "ulist":       {"tag": "ul"},
    "ul":          {"tag": "ul"},
    "olist":       {"tag": "ol"},
    "ol":          {"tag": "ol"},
    "item":        {"tag": "li"},
    "li":          {"tag": "li"},
    "select":      {"tag": "select"},
    "options":     {"tag": "optgroup"},
    "option":      {"tag": "option"},
    "canvas":      {"tag": "canvas"},
    "audio":       {"tag": "audio"},
    "video":       {"tag": "video"},
    "track":       {"tag": "track"},
    "details":     {"tag": "details"},
    "summary":     {"tag": "summary"},
    "sum":         {"tag": "summary"},
    "label":       {"tag": "label"},
    "lbl":         {"tag": "label"},
    "frame":       {"tag": "iframe"},
    "map":         {"tag": "map"},
    "area":        {"tag": "area"},
    "mark":        {"tag": "mark"},
    "noscript":    {"tag": "noscript"},
    "noscr":       {"tag": "noscript"},
    "object":      {"tag": "object"},
    "obj":         {"tag": "object"},
    "progressbar": {"tag": "progress"}
}


class Meta:
    """
    Class for storing meta data
    """
    key: str
    value: str

    def __init__(self, key: str, value: str) -> None:
        """
        Meta constructor
        :param key: Key to access a meta
        :type key: str
        :param value: Data we want to save
        :type value: str
        """
        self.key = key
        self.value = value
    
    def to_html(self) -> str:
        """
        Translates code of meta to HTML code
        """
        return f'<meta {self.key}=\"{self.value}\">'


class Equiv:
    """
    Class to store equiv meta data
    """
    key: str
    value: str

    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    
    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        return f'<meta http-equiv=\"{self.key}\" content=\"{self.value}\">'


class OgProp:
    """
    needs to store OG metadata
    """
    key: str
    value: str

    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    
    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        return f'<meta property=\"og:{self.key}\" content=\"{self.value}\">'


class Doctype:
    """
    needs to store DOCTYPE
    """
    ntml: str
    html: str

    def __init__(self, ntml: str = "ntml 0.2, patch 3", html: str = "HTML") -> None:
        self.ntml = ntml
        self.html = html

    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        return f"<!DOCTYPE {self.html}>\n<!-- This file was autogenerated by {self.ntml} -->\n"


class Import:
    """
    needs to store import data
    """
    sem: str
    kind: str
    path: str

    def __init__(self, kind, sem, path) -> None:
        self.sem = sem
        self.kind = kind
        self.path = path

    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        if self.sem == "script":
            return f"<script src=\"{self.path}\" type=\"{self.kind}\"></script>\n"
        return f"<link rel=\"{rels[self.sem]}\" href=\"{self.path}\" type=\"{self.kind}\">\n"


class Title:
    """
    needs to store title of the page
    """
    text: str

    def __init__(self, text: str = "") -> None:
        self.text = text
    
    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        return "<title>"+self.text+"</title>\n"


class SimpleTagOpen:
    """
    needs to store simple opening tags
    """
    kind: str
    props: str

    def __init__(self, kind: str, props: Optional[dict] = None):
        self.kind = kind
        self.props = (tran_props(props[0]) + " " + " ".join(props[1])) if props else ""
    
    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        #if self.kind == "body":
        #    return f"<html {self.props}><body>\n    "
        return f"<{self.kind}{self.props}>\n    "
    

class SimpleTagClose:
    """
    needs to store simple closing tags
    """
    kind: str

    def __init__(self, kind: str) -> None:
        self.kind = kind

    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        return f"</{self.kind}>\n" + ("\n</html>" if self.kind == "body" else "")


class Tran:
    """
    class implementing translation NTML page to HTML
    """
    tree: list[Node | list | Any]
    data: dict
    imports: list[Import]
    cache: str
    doctype: Doctype
    autospace: list[bool]

    def __init__(self, tree, fp: str = "", initdt: Optional[dict] = None, meals = None) -> None:
        self.fp = fp
        self.tree: list[Node | list | Any] = tree
        self.adress = 0
        self.imports = []
        self.cache = ""
        self.doctype = Doctype()
        self.data: dict = initdt or {
            "meta": [
                Meta("charset", "UTF-8")]
        }
        self.autospace = [True]
        self.meals = MEALS.copy()
        if meals is not None:
            self.meals |= meals.copy()

    def to_html(self) -> str:
        """
        Converts to HTML
        @return: str
        """
        return self.doctype.to_html() + \
            "<head  xmlns=\"\">\n        "+"\n        ".join(tuple(i.to_html() for i in self.data["meta"])) + \
            "        " + "        ".join(tuple(i.to_html() for i in self.imports)) + "    </head>\n\n" + \
            self.cache.replace("\n", "\n    ").strip()
    
    def walk_tree(self):
        """
        Caches HTML data for use `Tran.to_html` later
        """
        self.cache = self.walk_subtree(self.tree)
    
    def walk_subtree(self, node: Optional[Node | list] = None):
        
        """
        Implements recursive HTML caching
        @param node: Optional[Node | list]
        @return: str
        """
        node = node or []
        # print(node)
        if type(node) == list:
            ret = ""
            for i in node:
                ret += self.walk_subtree(i)
            return ret
        
        elif type(node) == Node:

            if node.kind == "doctype":
                self.doctype = Doctype("ntml "+node.data["version"])

                return ""
            
            elif node.kind == "import":
                self.imports.append(Import(node.data["type"], node.data["semantic"], node.data["path"]))
                return ""
            
            elif node.kind == "title":
                self.data["meta"].append(Title(node.data["text"][1:][:-1]))

                return ""
            
            elif node.kind == "tag":
                data = node.data
                data["props"] = data["props"] if data["props"] is not None else ({}, [])

                tkind = data["type"].strip()
                tprops = data["props"]
                if "props" in list(self.meals[tkind]):
                    tprops = (self.meals[tkind]["props"][0].copy(), data["props"][1])
                    btprops = (self.meals[tkind]["props"][0].copy(), data["props"][1])
                    tprops[0].update(data["props"][0])
                    for i in btprops[0].keys():
                        if i in data["props"][0].keys():
                            tprops[0][i] = btprops[0][i] + ' ' + data["props"][0][i]
                        else:
                            tprops[0][i] = btprops[0][i]

                tbody = data["body"]

                if tkind in "code cd".split():
                    return tbody

                elif tkind in "hld holder".split():
                    if tbody:
                        el, es = node.pos
                        nl, ns = node.end_pos
                        print("\nError while parsing file %s," % self.fp)
                        print("At line %d, column %d:" % (nl, ns))
                        with open(self.fp, "rt") as f:
                            print("│   " + (ln := f.read().split("\n")[nl - 1]).strip())
                        ns -= len(ln) - len(ln.strip())
                        print("│   " + " " * (es - len(ln) - len(ln.strip())) +
                              "~" * (ns - es + len(ln) - len(ln.strip()) - 1) + "▲")
                        print("└───" + "─" * (ns - 1) + "┘")
                        print(f"{tkind} should not have a body\n")
                        sys.exit()
                    if not tprops:
                        _, es = node.pos
                        nl, ns = node.end_pos
                        print("\nError while parsing file %s," % self.fp)
                        print("At line %d, column %d:" % (nl, ns))
                        with open(self.fp, "rt") as f:
                            print("│   " + (ln := f.read().split("\n")[nl - 1]).strip())
                        ns -= len(ln) - len(ln.strip())
                        print("│   " + " " * (ns - 1) + "▲")
                        print("└───" + "─" * (ns - 1) + "┘")
                        print(f"{tkind} needs a properties\n")
                        sys.exit()

                elif tkind != "script":
                    if tkind in "img image".split():
                        if tbody is not None or tprops is None:
                            el, es = node.pos
                            nl, ns = node.end_pos
                            print("\nError while parsing file %s," % self.fp)
                            print("At line %d, column %d:" % (nl, ns))
                            with open(self.fp, "rt") as f:
                                print("│   " + (ln := f.read().split("\n")[nl - 1]).strip())
                            ns -= len(ln) - len(ln.strip())
                            print("│   " + " " * (es - len(ln) - len(ln.strip())) +
                                  "~" * (ns - es + len(ln) - len(ln.strip()) - 1) + "▲")
                            print("└───" + "─" * (ns - 1) + "┘")
                            print(f"{tkind} should not have a body\n")
                            sys.exit()
                    else:
                        if tbody is None:
                            el, es = node.pos
                            nl, ns = node.end_pos
                            print("\nError while parsing file %s," % self.fp)
                            print("At line %d, column %d:" % (nl, ns))
                            with open(self.fp, "rt") as f:
                                print("│   " + (ln := f.read().split("\n")[nl - 1]).strip())
                            ns -= len(ln) - len(ln.strip())
                            print("│   " + " " * (es - len(ln) - len(ln.strip())) +
                                  "~" * (ns - es + len(ln) - len(ln.strip()) - 1) + "▲")
                            print("└───" + "─" * (ns - 1) + "┘")
                            print(f"{tkind} needs a body\n")
                            sys.exit()

                if tkind in "code cdr".split():
                    self.autospace.append(False)
                else:
                    self.autospace.append(True)

                if tkind in "script scr".split():
                    self.autospace.pop()
                    del tprops[0]["lang"]
                    ret = SimpleTagOpen(self.meals[tkind]["tag"], tprops).to_html()
                    if tbody and "href" not in tprops[0]:
                        ret += tbody + SimpleTagClose(self.meals[tkind]["tag"]).to_html()
                    return ret

                if not tbody:
                    if tkind in "hld holder".split():
                        r = SimpleTagOpen(self.meals[tkind]["tag"],
                                          tprops).to_html()[:-5]+SimpleTagClose(self.meals[tkind]["tag"]).to_html()
                    else:
                        r = SimpleTagOpen(self.meals[tkind]["tag"], tprops).to_html()
                elif tkind in "table tab".split():
                    r = SimpleTagOpen("table", {}).to_html()+SimpleTagOpen("tbody", tprops).to_html() + \
                        self.walk_subtree(tbody).strip().replace("\n", "\n    ")+SimpleTagClose("tbody").to_html() + \
                        SimpleTagClose("table").to_html()
                else:
                    r = SimpleTagOpen(self.meals[tkind]["tag"], tprops).to_html() + \
                        self.walk_subtree(tbody).strip().replace("\n", "\n    ") + \
                        SimpleTagClose(self.meals[tkind]["tag"]).to_html()
                    # print(r)
                self.autospace.pop()
                return r
            
            elif node.kind == "comment":
                return "<!--"+node.data["text"]+"-->\n"
            
            elif node.kind == "html":
                return node.data["value"]
        
        else:

            r = str(node) if type(node) != str else node
            if self.autospace[-1]:
                r = ("" if r in "([{$*/&|^-+=,.:;%?!)]}\n" else " ")+r.strip()+(" " if r in ",.:;%?!)]}" else "")
                r = r.replace(" , ", ",").replace(" . ", ".").replace(" : ", ":").\
                    replace(" ; ", ";").replace(" % ", "%").replace(" ! ", "!").replace(" ) ", ")").\
                    replace(" ] ", "]").replace(" } ", "}").replace(" !", "!")
            return r

        return ""
