# Adding Microstructure Data

A FANS calculation requires a microstructure dataset. You must create a node in your AiiDA profile that corresponds to such a microstructure. An example microstructure file is included in the accompanying tutorial which you can download with,

```sh
wget https://github.com/DataAnalyticsEngineering/AiiDA-FANS/raw/refs/heads/main/tutorial/ms-example.h5
```

Alternatively, you can visit the [FANS repository](https://github.com/DataAnalyticsEngineering/FANS) for more information and sample microstructures.

Since realistic microstructure files tend to be extremely large, saving such files in an AiiDA profile has some significant drawbacks. As such, we strongly recommend you put the microstructure file on the same machine as where you intend to run FANS. You may place it inside the working directory of the AiiDA computer you created, within a subdirectory called "microstructures/".

Once you have a microstructure file, you must create a `MicrostructureData` node like so:

```python
from aiida import load_profile
from aiida.orm import load_computer
from aiida.plugins import DataFactory

load_profile()

MICROSTRUCTURE_PATH = "/path/to/microstructures/ms-example.h5"
DATASET_NAME = "/dset_0/image"
COMPUTER_LABEL = "localhost"

MicrostructureData = DataFactory("fans.microstructure")
MicrostructureData(
    MICROSTRUCTURE_PATH,
    DATASET_NAME,
    computer=load_computer(label=COMPUTER_LABEL),
    label="microstructure.data"
).store()
```

You can write this in a python script and run it, or use AiiDA's interactive shell with `verdi shell`. If you use the interactive shell, you can omit `load_profile` and `import DataFactory` as AiiDA will automatically loads the default profile and imports some useful tools. Remember to change `MICROSTRUCTURE_PATH`, `DATASET_NAME`, and `COMPUTER_LABEL` to their appropriate values. After storing the node, you can check the nodes on your profile with `verdi node list` and expose details of a particular node with `verdi node show <pk>`.

To reuse this node when executing `FansCalculation` jobs, you can use `load_node(label="microstructure.data")` as long as only one node exists with the provided label. If you intend on using multiple files and/or multiple groups within individual files, assign each node a distinct and identifiable label.
