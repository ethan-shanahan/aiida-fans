"""Parsers provided by aiida_fans."""

from pathlib import Path

from aiida.engine import ExitCode
from aiida.orm import SinglefileData
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

FANSCalculation = CalculationFactory("fans")


class FANSParser(Parser):
    """Extracts valuable data from FANS results."""

    def parse(self, **kwargs) -> ExitCode:
        """Parse outputs, store results in database.

        Returns:
            ExitCode: non-zero exit code, if parsing fails
        """
        retrieved_temporary_folder = Path(kwargs["retrieved_temporary_folder"])
        output_filename = self.node.get_option("output_filename")

        # Check that output_filename is valid
        if (type(output_filename) is not str) or (output_filename == ""):
            return self.exit_codes.ERROR_INVALID_OUTPUT

        # Check that folder content is as expected.
        files_retrieved = set(self.retrieved.list_object_names())
        files_expected = set()#{output_filename}
        if not files_expected <= files_retrieved:
            self.logger.error(f"Found files '{files_retrieved}', expected to find '{files_expected}'")
            return self.exit_codes.ERROR_MISSING_OUTPUT

        # Add output HDF5 file to repository.
        output_path = retrieved_temporary_folder / output_filename
        self.logger.info(f"Parsing '{output_path}'")
        with output_path.open("rb") as handle:
            output_node = SinglefileData(file=handle)
        self.out("results", output_node)

        return ExitCode(0)
