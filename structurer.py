from __future__ import annotations
import json
import re
import typing


def handleType(root: Structurer, o: any, name: str = None) -> StructureDict or StructureList or StructureElement:
    if type(o) is dict:
        return StructureDict(root, o, name=name)
    elif type(o) is list:
        return StructureList(root, o, name=name)
    return StructureElement(o)


class Structurer:
    def __init__(self, root: any):
        self.dicts_objects = []
        self.root = handleType(self, root)

    def toTypedDict(self, indent: str = "    ") -> str:
        td = "import typing\n\n"

        if type(self.root) is not StructureDict:
            td += "# " + " Reference ".center(50, "*") + "\n"
            td += "# " + self.root.toTypedDict().center(50, " ") + "\n"
            td += "# " + "*" * 50 + "\n"
        classes = self.dicts_objects

        if classes:
            td += "\n# " + " Classes ".center(50, "*") + "\n\n"
            for _d in classes:
                td += _d.toTypedDict(indent=indent) + "\n\n"
            td += "# " + "-" * 50
        td += "\n"
        return td


class StructureElement:
    def __init__(self, obj):
        if obj is None:
            self.obj = "None"
        else:
            self.obj = type(obj).__name__

    def toTypedDictReference(self) -> str:
        return self.obj

    def toTypedDict(self) -> str:
        return self.toTypedDictReference()

    def __eq__(self, other: StructureElement) -> bool:
        assert type(other) is StructureElement
        return self.obj == other.obj


class StructureList:
    def __init__(self, root: Structurer, obj: list, name: str = None):
        assert type(obj) is list
        if len(obj) == 0:
            self.obj = StructureElement(None)
        else:
            self.obj = handleType(root, obj[0], name=name)

    def getName(self) -> str:
        return self.obj.toTypedDictReference()

    def toTypedDictReference(self) -> str:
        return self.getName()

    def toTypedDict(self) -> str:
        return F"typing.List[{self.obj.toTypedDictReference()}]"

    def __eq__(self, other: StructureList) -> bool:
        assert type(other) is StructureList
        return self.obj == other.obj


class StructureDict:
    @classmethod
    def getName(cls, existing: typing.List[StructureDict], name: str = None):
        def nameMaker(_name: str, _i: int = None):
            return F"""{"".join([x.capitalize() for x in re.split("[-_ ]+", _name)]) if _name is not None else 'GenericDict'}{_i if _i is not None else ''}"""

        name = nameMaker(name)
        if name in map(lambda x: x.name, existing):
            i = 1
            while nameMaker(name, i) in map(lambda x: x.name, existing):
                i += 1
            name = nameMaker(name, i)
        return name

    def __init__(self, root: Structurer, obj: dict, name: str = None):
        assert type(obj) is dict

        self.struct = dict()
        for k, v in obj.items():
            self.struct[k] = handleType(root, v, name=k)

        self.name = None
        try:
            index = root.dicts_objects.index(self)
            elt = root.dicts_objects[index]
            self.struct = elt.struct
            self.name = elt.name
        except ValueError:
            self.name = self.getName(root.dicts_objects, name)
            root.dicts_objects.append(self)

    def __repr__(self) -> str:
        return F"<StructureDict {self.name}>"

    def toTypedDictReference(self) -> str:
        return self.name

    def toTypedDict(self, indent: str = "    ") -> str:
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

    def __eq__(self, other: StructureDict) -> bool:
        assert type(other) is StructureDict
        keys1 = set(self.struct.keys())
        keys2 = set(other.struct.keys())
        if keys1 != keys2:
            return False
        for k, v in self.struct.items():
            if k not in other.struct:
                return False
            if v != other.struct[k]:
                return False

        return True


if __name__ == "__main__":
    with open("example.json") as f:
        exampledata = json.load(f)

    s = Structurer(exampledata)
    text = s.toTypedDict()
    with open("generated_example.py", "w+") as f:
        f.write(text)
    print(text)
