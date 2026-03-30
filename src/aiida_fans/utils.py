"""Utilities provided by aiida_fans."""

from typing import Any, Literal

from aiida.engine import run, submit
from aiida.orm import CalcJobNode, Data, Node, QueryBuilder
from aiida.plugins import CalculationFactory, DataFactory
from numpy import ndarray

from aiida_fans.helpers import arraydata_equal


def aiida_type(value: Any) -> type[Data]:
    """Find the corresponding AiiDA datatype for a variable with pythonic type.

    Args:
        value (Any): a python variable

    Raises:
        NotImplementedError: only certain mappings are supported

    Returns:
        type[Data]: an AiiDA data type
    """
    match value:
        case str():
            return DataFactory("core.str")  # Str
        case int():
            return DataFactory("core.int")  # Int
        case float():
            return DataFactory("core.float")  # Float
        case list():
            return DataFactory("core.list")  # List
        case dict():
            if all(map(lambda t: isinstance(t, ndarray), value.values())):
                return DataFactory("core.array")  # ArrayData
            else:
                return DataFactory("core.dict")  # Dict
        case _:
            raise NotImplementedError(f"Received an input of value:  {value}    with type:  {type(value)}")


def fetch(label: str, value: Any) -> list[Node]:
    """Return a list of nodes matching the label and value provided.

    Args:
        label (str): the label of the node to fetch
        value (Any): the value of the node to fetch

    Returns:
        list[Node]: the list of nodes matching the give criteria
    """
    datatype = aiida_type(value)
    nodes = (
        QueryBuilder()
        .append(cls=datatype, tag="n")
        .add_filter("n", {"label": label})
        .add_filter("n", {"attributes": {"==": datatype(value).base.attributes.all}})
        .all(flat=True)
    )

    if datatype != DataFactory("core.array"):
        return nodes  # type: ignore
    else:
        array_nodes = []
        for array_node in nodes:
            array_value = {
                k: v
                for k, v in [
                    (name, array_node.get_array(name))
                    for name in array_node.get_arraynames()  # type: ignore
                ]
            }
            if arraydata_equal(value, array_value):
                array_nodes.append(array_node)
        return array_nodes


def generate(label: str, value: Any) -> Node:
    """Return a single node with the label and value provided.

    Uses an existing node when possible, but otherwise creates one instead.

    Args:
        label (str): the label of the node to generate
        value (Any): the pythonic value of the node to generate

    Raises:
        RuntimeError: panic if more than one node is found matching the criteria

    Returns:
        Node: a stored node with label and value
    """
    bone = fetch(label, value)
    if len(bone) == 0:
        return aiida_type(value)(value, label=label).store()
    elif len(bone) == 1:
        return bone.pop()
    else:
        raise RuntimeError


def convert(ins: dict[str, Any], path: list[str] = []):
    """Takes a dictionary of inputs and converts the values to their respective Nodes.

    Args:
        ins (dict[str, Any]): a dictionary of inputs
        path (list[str], optional): a list of predecessor keys for nested dictionaries. Defaults to [].
    """
    for k, v in ins.items():
        if k == "metadata" or isinstance(v, Node):
            continue
        elif k in ["microstructure", "error_parameters"]:
            convert(v, path=[*path, k])
        elif k == "macroscale_loading":
            ins[k] = {str(i): generate(k, load) for i, load in enumerate(v)}
        else:
            ins[k] = generate(".".join([*path, k]), v)


def compile_query(ins: dict[str, Any], qb: QueryBuilder) -> None:
    """Interate over the converted input dictionary and append to the QueryBuilder for each node.

    Args:
        ins (dict[str,Any]): a dictionary of converted inputs
        qb (QueryBuilder): a CalcJobNode QueryBuilder with tag='calc'
    """
    for k, v in ins.items():
        if k == "metadata":
            continue
        elif k in ["microstructure", "error_parameters"] and isinstance(v, dict):
            compile_query(v, qb)
        elif k == "macroscale_loading" and isinstance(v, dict):
            for load in v.values():
                qb.append(cls=type(load), with_outgoing="calc", filters={"pk": load.pk})
        else:
            qb.append(cls=type(v), with_outgoing="calc", filters={"pk": v.pk})


def execute_fans(mode: Literal["submit", "run"], inputs: dict[str, Any]):
    """This utility function simplifies the process of executing aiida-fans jobs.

    The only nodes you must provide are the `code` and `microstructure` inputs.
    Other inputs can be given as standard python variables. Your repository will
    be automatically scanned for equivalent nodes. These will be used whenever
    possible, otherwise new nodes will be created.

    The `strategy` specifies which microstructure distribution method you wish to use.
    It defaults to "Fragmented".

    You must load an AiiDA profile yourself before using this function.

    **Args:**
        **mode** *(Literal["Submit", "Run"])*
        **inputs** *(dict[str, Any])*
        **strategy** *(Literal["Fragmented", "Stashed"]), optional*

    ---

    **Example:**
    ```
    from aiida import load_profile
    from aiida.orm import load_code, load_node
    from aiida_fans.utils import execute_fans
    load_profile()
    inputs = {
        "code": load_code("fans"),
        "microstructure": load_node(label="microstructure"),
        ...
        "metadata": {
            "label": "an example calculation"
        }
    }
    execute_fans("Submit", inputs, "Stashed")
    ```
    """
    calcjob = CalculationFactory("fans")

    # fetch the inputs if possible or otherwise create them
    convert(inputs)

    # check if identical calculation already exists
    qb = QueryBuilder().append(cls=CalcJobNode, tag="calc", project="id")
    compile_query(inputs, qb)
    results = qb.all(flat=True)
    if (count := len(results)) != 0:
        print(f"It seems this calculation has already been performed {count} time{'s' if count > 1 else ''}. {results}")
        confirmation = input("Are you sure you want to rerun it? [y/N] ").strip().lower() in ["y", "yes"]
    else:
        confirmation = True

    if confirmation:
        match mode:
            case "run":
                run(calcjob, inputs)  # type: ignore
            case "submit":
                submit(calcjob, inputs)  # type: ignore


def submit_fans(inputs: dict[str, Any]):
    """See `execute_fans` for implementation and usage details."""
    execute_fans("submit", inputs)


def run_fans(inputs: dict[str, Any]):
    """See `execute_fans` for implementation and usage details."""
    execute_fans("run", inputs)
