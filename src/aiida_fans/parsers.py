"""Parser subclass for aiida-fans calculations."""

from pathlib import Path

from aiida.engine import ExitCode
from aiida.orm import CalcJobNode, Dict, SinglefileData
from aiida.parsers.parser import Parser
from h5py import Dataset, Group
from h5py import File as h5File


class FansParser(Parser):
    """Extracts data from FANS results."""

    def __init__(self, node: CalcJobNode):
        """Calls `super().__init__()` then defines `self.results_dict`."""
        super().__init__(node)
        self.results_dict = dict()

    def parse(self, **kwargs) -> ExitCode | None:
        """Parse outputs and store results as nodes."""
        output_path: Path = Path(kwargs["retrieved_temporary_folder"]) / self.node.get_option("output_filename")  # type: ignore
        if output_path.is_file():
            self.out("output", node=SinglefileData(output_path))
        else:
            return self.exit_codes.ERROR_MISSING_OUTPUT

        with h5File(output_path) as h5:
            results = h5[
                self.node.inputs.microstructure.data.dataset_name + "_results/" + self.node.get_option("results_prefix")
            ]
            results.visititems(self.parse_h5)

        if self.results_dict:
            self.out("results", Dict(self.results_dict))

    def parse_h5(self, name: str, object: Group | Dataset) -> None:
        """Callable for the .visititems method of h5py Groups."""
        if isinstance(object, Group):
            return
        if "average" in name:
            keys = name.split("/")
            res = self.results_dict
            data = list(object[:])
            self.nestle(res, keys, data)

    def nestle(self, bottom: dict, layers: list[str], top: list[float]) -> None:
        """Recursive function to generate a nested results dictionary."""
        layer = layers.pop(0)
        if len(layers) > 0:
            bottom.setdefault(layer, dict())
            self.nestle(bottom[layer], layers, top)
        else:
            bottom[layer] = top
