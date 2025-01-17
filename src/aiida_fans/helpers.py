"""Tools and utilities required by aiida_fans."""

import json

from aiida.orm import ArrayData, Dict, Float, Int, List, SinglefileData, Str


class InputEncoder(json.JSONEncoder):
    """Prepares a dictionary of calcjob inputs for json representation."""

    def default(self, obj):
        """Converts aiida datatypes to their python counterparts."""
        match obj:
            case Str() | Int() | Float():
                return obj.value
            case List():
                return obj.get_list()
            case Dict():
                return obj.get_dict()
            case ArrayData():
                return [a[1].tolist() for a in obj.get_iterarrays()]  #! Caution: may be disordered
            case SinglefileData():
                return obj.filename
            case _:
                # Let the base class default method raise the TypeError
                return super().default(obj)
