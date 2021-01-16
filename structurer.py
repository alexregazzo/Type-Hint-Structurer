import json
import re


class Structurer:
    dicts = []

    def __init__(self, root: any):
        if isinstance(root, Structurer):
            if type(root) is StructureDict:
                self.dicts.append(root)
        else:
            self.root = self.define_property(root)

    @classmethod
    def define_property(cls, o, name=None):
        if type(o) is dict:
            return StructureDict(o, name=name)
        elif type(o) is list:
            return StructureList(o, name=name)
        return StructureElement(o)

    def toTypedDict(self, indent="    ") -> str:
        td = "import typing\n\n"

        if type(self.root) is not StructureDict:
            td += "# " + " Reference ".center(50, "*") + "\n"
            td += "# " + self.root.toTypedDict().center(50, " ") + "\n"
            td += "# " + "*" * 50 + "\n"

        if self.dicts:
            td += "\n# " + " Classes ".center(50, "*") + "\n\n"
            for _d in self.dicts[::-1]:
                td += _d.toTypedDict(indent=indent) + "\n\n"
            td += "# " + "-" * 50
        td += "\n"
        return td


class StructureElement(Structurer):
    def __init__(self, obj):
        super().__init__(self)
        if obj is None:
            self.obj = "None"
        else:
            self.obj = type(obj).__name__

    def toTypedDictReference(self) -> str:
        return self.obj

    def toTypedDict(self, indent="    ") -> str:
        return self.toTypedDictReference()


class StructureList(Structurer):
    def __init__(self, obj, name=None):
        super().__init__(self)
        assert type(obj) is list
        if len(obj) == 0:
            self.obj = StructureElement(None)
        else:
            self.obj = self.define_property(obj[0], name=name)

    def getName(self) -> str:
        return self.obj.toTypedDictReference()

    def toTypedDictReference(self) -> str:
        return self.getName()

    def toTypedDict(self, indent="    "):
        return F"typing.List[{self.obj.toTypedDictReference()}]"


class StructureDict(Structurer):
    names = []

    @classmethod
    def getName(cls, name=None):
        def nameMaker(_name: str, _i: int = None):
            return F"""{"".join([x.capitalize() for x in re.split("[-_ ]+", _name)]) if _name is not None else 'GenericDict'}{_i if _i is not None else ''}"""

        name = nameMaker(name)
        if name in cls.names:
            i = 0
            while nameMaker(name, i) in cls.names:
                i += 1
            name = nameMaker(name, i)
        cls.names.append(name)
        return name

    def __init__(self, obj, name=None):
        super().__init__(self)
        assert type(obj) is dict
        self.struct = dict()
        for k, v in obj.items():
            self.struct[k] = self.define_property(v, name=k)
        self.name = self.getName(name)

    def __repr__(self):
        return F"<StructureDict {self.name}>"

    def toTypedDictReference(self) -> str:
        return self.name

    def toTypedDict(self, indent="    ") -> str:
        td = f"class {self.toTypedDictReference()}(typing.TypedDict):\n"
        for k, v in self.struct.items():
            td += F"{indent}{k}: "
            if type(v) is StructureElement:
                td += v.toTypedDict()
            elif type(v) is StructureList:
                td += F"typing.List[{v.toTypedDictReference()}]"
            else:
                td += v.toTypedDictReference()
            td += "\n"

        return td


if __name__ == "__main__":
    with open("example.json") as f:
        exampledata = json.load(f)

    s = Structurer(exampledata)
    text = s.toTypedDict()
    with open("generated_example.py", "w+") as f:
        f.write(text)
    print(text)
