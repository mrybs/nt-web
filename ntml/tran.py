from ntml.ntml_parser import *
from typing import *
import sys


def tran_props(props: dict):
    ret: str = ""

    for i in props.keys():
        ret += " "+i+"=\""+eval(props[i])+"\""
    
    return ret


rels: dict = {
    "style": "stylesheet",
    "favicon": "icon",
    "script": "script"
}

meals: dict = {
    "body": "body",
    "bold": "b",
    "b": "b",
    "italic": "i",
    "i": "i",
    "underline": "u",
    "u": "u",
    "strikeout": "s",
    "s": "s",
    "block": "div",
    "bl": "div",
    "text": "p",
    "t": "p",
    "input": "input",
    "inp": "input",
    "h1": "h1",
    "h2": "h2",
    "h3": "h3",
    "h4": "h4",
    "ht1": "h1",
    "ht2": "h2",
    "ht3": "h3",
    "ht4": "h4",
    "link": "a",
    "ln": "a",
    "image": "image",
    "img": "image",
    "cd": "div",
    "code": "div",
    "form": "form",
    "f": "form",
    "tr": "tr",
    "td": "td",
    "script": "script",
    "scr": "script",
    "btn": "button",
    "button": "button"
}


class Meta:
    key: str
    value: str

    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    
    def to_html(self):
        return f'<meta {self.key}=\"{self.value}\">'


class Equiv:
    key: str
    value: str

    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    
    def to_html(self):
        return f'<meta http-equiv=\"{self.key}\" content=\"{self.value}\">'


class OgProp:
    key: str
    value: str

    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    
    def to_html(self):
        return f'<meta property=\"og:{self.key}\" content=\"{self.value}\">'


class Doctype:
    ntml: str
    html: str

    def __init__(self, ntml: str = "ntml 0.2, patch 3", html: str = "HTML") -> None:
        self.ntml = ntml
        self.html = html

    def to_html(self):
        return f"<!DOCTYPE {self.html}>\n<!-- This file was autogenerated by {self.ntml} -->"


class Import:
    sem: str
    kind: str
    path: str

    def __init__(self, kind, sem, path) -> None:
        self.sem = sem
        self.kind = kind
        self.path = path

    def to_html(self):
        return f"<link rel=\"{rels[self.sem]}\" href=\"{self.path}\" type=\"{self.kind}\">\n"


class Title:
    text: str

    def __init__(self, text: str = "") -> None:
        self.text = text
    
    def to_html(self):
        return "<title>"+self.text+"</title>\n"


class SimpleTagOpen:
    kind: str
    props: str

    def __init__(self, kind: str, props: Optional[dict] = None):
        self.kind = kind
        self.props = tran_props(props) if props else ""
    
    def to_html(self):
        return f"<{self.kind}{self.props}>\n    "
    

class SimpleTagClose:
    kind: str

    def __init__(self, kind: str) -> None:
        self.kind = kind

    def to_html(self):
        return f"</{self.kind}>\n"


class Tran:
    tree: list[Node | list | Any]
    data: dict
    imports: list[Import]
    cache: str
    doctype: Doctype
    autospace: list[bool]

    def __init__(self, tree, initdt: Optional[dict] = None) -> None:
        self.tree: list[Node | list | Any] = tree
        self.adress = 0
        self.imports = []
        self.cache = ""
        self.doctype = Doctype()
        self.data: dict = initdt or {
            "meta": [
                Meta("content-type", "text/html"),
                Meta("charset", "UTF-8")]
        }
        self.autospace = [True]

    def to_html(self):
        return self.doctype.to_html() + \
            "\n<html>\n    <head>\n        "+"\n        ".join(tuple(i.to_html() for i in self.data["meta"])) + \
            "        " + "        ".join(tuple(i.to_html() for i in self.imports)) + "    </head>\n\n" +\
            self.cache.replace("\n", "\n    ").strip()+"\n</html>"
    
    def walk_tree(self):
        self.cache = self.walk_subtree(self.tree)
    
    def walk_subtree(self, node: Optional[Node | list] = None):
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

                tkind = data["type"].strip()
                tprops = data["props"]
                tbody = data["body"]

                if tkind != "script":
                    if tkind in "img image".split():
                        if tbody is not None or tprops is None:
                            print(f"error: `{tkind}` should not have body")
                            sys.exit()
                    else:
                        if tbody is None:
                            print(f"error at {node.pos}: `{tkind}` needs a body")
                            sys.exit()

                if tkind in "code cd script scr".split():
                    self.autospace.append(False)
                else:
                    self.autospace.append(True)

                if not tbody:
                    r = SimpleTagOpen(meals[tkind], tprops).to_html()
                elif tkind in "table tab".split():
                    r = SimpleTagOpen("table", {}).to_html()+SimpleTagOpen("tbody", tprops).to_html() + \
                        self.walk_subtree(tbody).strip().replace("\n", "\n    ")+SimpleTagClose("tbody").to_html() + \
                        SimpleTagClose("table").to_html()
                else:
                    r = SimpleTagOpen(meals[tkind], tprops).to_html() + \
                        self.walk_subtree(tbody).strip().replace("\n", "\n    ")+SimpleTagClose(meals[tkind]).to_html()
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
