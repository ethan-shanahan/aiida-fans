# Running FANS

In this section, we will briefly demonstrate how to use the plugin's special utilities to easily run a FANS calculation. For general information on the usage of AiiDA you should refer to the [AiiDA documentation](https://aiida-core.readthedocs.io/), and for the usage of FANS refer to its [repository](https://github.com/DataAnalyticsEngineering/FANS).

## The Challenging Standard Workflow

This plugin offers some utilities to help smooth the AiiDA user experience. Namely, the `utils.execute_fans` function which allows you to provide the inputs for a job as a dictionary of mostly pythonic values. This utility will parse these inputs and automatically use any appropriate existing nodes it finds in your profile before making new nodes where necessary. This is the biggest difference between the standard AiiDA usage pattern and what we offer with Utilities. Ordinarily, it is very easy to end up unintentionally creating duplicate input nodes, resulting in a bloated and disconnected graph of work, without navigating the cumbersome query functions. Utilities aims to free us of this inconvenience. It opperates under the assumption that if a duplicate node *would* be created, then the existing node should be fetched and used instead. This is a very powerful philosophy when stringently adhered to, but breaks down if ignored.

For example, consider the material model input parameter,

```json
"FE_type": "HEX8"
```

In the AiiDA database (i.e. graph), this corresponds to a node of type `Str` with the value `"HEX8"`, and optionally we can label it with `"FE_type"`. When we run a `FansCalculation` job it must receive a `Str` node for the *FE_type* input. If a pythonic `str` is provided instead, AiiDA automatically converts it to an AiiDA `Str` and stores the node in the database. Doing it this way, if you run five simulations using hexahedral elements (HEX8), you will end up with five identical unlabeled `Str` nodes in your database, each pointing to a different `CalcJob` node. Clearly, the better option would be to have one `Str` node point to five `CalcJob` nodes. This could be done by providing each invocation of the `FansCalculation` job with the same node. So you either have to memorise the primary key of the `Str` node valued `"HEX8"`, or construct a query to fetch it. In this case, the query appears simple enough,

```python
QueryBuilder()
.append(cls=Str, tag="node")
.add_filter("node", {"value": {"==": "HEX8"}})
.all(flat=True)
```

but there are dangers herein since if another input parameter happens to have the same value, they would both be fetched. To get around this, you would need to have the foresight to label each node appropriately. Additionally, different data types have different query interfaces, making the overall user experience a challenging one.

## Using Utilities Instead

Introducing the `utils.execute_fans` function. With this function, you can provide the input parameters of FANS as basic pythonic values in a dictionary (with some nuances). Here is what a script to run FANS might look like,

```python
from aiida import load_profile
from aiida.orm import load_code, load_node
from aiida_fans.utils import run_fans

load_profile()

################################################################################

inputs = {
    "code": load_code("FANS"),  # Code node goes here.
    # Microstructure definition
    "microstructure": {
        "data": load_node(label="microstructure.data"),  # MS node goes here.
        "L": [1.0, 1.0, 1.0],
    },
    # Problem type and material model
    "problem_type": "mechanical",
    "matmodel": "LinearElasticIsotropic",
    "strain_type": "small",
    "material_properties": {
        "bulk_modulus": [62.5000, 222.222],
        "shear_modulus": [28.8462, 166.6667],
    },
    # Solver settings
    "FE_type": "HEX8",
    "method": "cg",
    "error_parameters": {
        "measure": "Linfinity",
        "type": "absolute",
        "tolerance": 1e-10,
    },
    "n_it": 100,
    # Macroscale loading conditions
    "macroscale_loading": [[[0.001, -0.002, 0.003, 0.0015, -0.0025, 0.001]]],
}

################################################################################

run_fans(inputs=inputs)
```

Note that the `inputs` dictionary closely resembles the input json required by FANS, with two exceptions. These are: the addition of the `"code": load_code("FANS")` entry which is an additional requirement of running any AiiDA `CalcJob`, and the `"microstructure": {"filepath": "path/to/ms.h5", "datasetname": "/path/to/group", ...` entry which has changed to `"microstructure": {"data": load_node(label="microstructure.data"), ...` according to the section on [Adding Microstructure Data](adding-microstructure-data.md). The final function call to `run_fans` is analogous to the AiiDA `run` function, and there exists a corresponding `submit_fans` function too.

The utilities function will first check each non-node entry in the dictionary and try to find an existing node whose value matches that which was provided and whose label matches the dictionary key of that input (using dot notation for embedded dictionaries). Additionally, if there exists a calculation whose inputs perfectly match the inputs provided, confirmation to proceed will be sought.
