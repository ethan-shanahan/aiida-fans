import json

from aiida.orm import Str, Int, Float, List, Dict, ArrayData, SinglefileData


class InputEncoder(json.JSONEncoder):
    def default(self, obj):
        match obj:
            case Str() | Int() | Float():
                return obj.value
            case List():
                return obj.get_list()
            case Dict():
                return obj.get_dict()
            case ArrayData():
                return [a[1].tolist() for a in obj.get_iterarrays()]
            case SinglefileData():
                return obj.filename

        # Let the base class default method raise the TypeError
        return super().default(obj)
