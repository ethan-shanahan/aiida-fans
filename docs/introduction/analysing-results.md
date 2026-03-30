# Analysing Results

You can review the nodes present in your profile at any time with `verdi node list`. You can also specify various attributes of the nodes you wish to highlight with the `--project` option.

```sh
verdi node list --project id label node_type
```

Once you have run at least one simulation, you will notice a `CalcJobNode`, labelled "FANS" by default. This represents the execution of a FANS process. You may want to visualise a portion of the graph connected to this node.

```sh
verdi node graph generate <pk of CalcJobNode> --identifier label
```

The pdf this creates arranges the input nodes on top, the calculation node in the middle, and the output nodes below.

## Output Nodes

To quickly interact with a specific nodes, you can enter the `verdi shell`. This automatically loads the default profile and imports some useful AiiDA functions like `load_node()`. You can use this function by passing the primary key (id) of the node you want to inspect and binding it to a variable.

### 1. `RemoteData`

This node refers to the specific working directory of the process. It is a subdirectory of the working directory you provided when specifying the computer. It is capable of establishing a connection to remote machine to provide access to the original data. For example, you can use this connection to list the objects within the assigned directory:

```python
remote_data.get_remote_path()
remote_data.listdir()
```

### 2. `FolderData`

Similar to the `RemoteData`, this node represents a directory-like object, but unlike the `RemoteData`, this node stores the contents of the directory in the AiiDA repository. With this type of node, you can navigate the directory, add or remove files and folders, and get the contents of files. The plugin stores a FolderData node containing the standard output and standard error files of FANS and the AiiDA scheduler. This is how you can print the standard output of FANS:

```python
folder_data.list_object_names()
print(folder_data.get_object_content("FANS.log"))
```

### 3. `SinglefileData`

The `SinglefileData` node is much like the `FolderData` node, but, as the name suggests, is for a single file rather than a whole directory. The plugin saves the resulting output hdf5 file from FANS as a `SinglefileData` node. The following code snippet is similar to how the plugin's parser extracts the results:

```python
singlefile_data.filename()
with h5py.File(singlefile_data.as_path()) as h5:
    results = h5[datasetname + "_results/" + results_prefix]
    results.visititems()

```

### 4. `Dict`

The final output node is a `Dict` node. This is analogous to the pythonic `dict` datatype. This dictionary contains the results that were specified by the input metadata. To access the raw python dictionary you must call the `get_dict()` method.

```python
results_dict.get_dict()
> {'load0': {'time_step0': {
    'strain_average': [
        0.00099999999999999,
       -0.002,
        0.003,
        0.0015,
       -0.0024999999999999,
        0.00099999999999998
    ],
   'stress_average': [
        0.23715475595413,
       -0.11002462781142,
        0.46722627941269,
        0.17110034475143,
       -0.28500501234689,
        0.1134596385013
    ]
  }}}
```

## Querying the Data

The AiiDA ^^database^^ is responsible for storing the provenance graph and is the primary way you interact with the data. For a guide on how to use AiiDA's query system, please refer to the [finding and querying how-to](https://aiida.readthedocs.io/projects/aiida-core/en/stable/howto/query.html#how-to-query). This offers valuable information on the current state of the `QueryBuilder` and points to more advanced topics also.
