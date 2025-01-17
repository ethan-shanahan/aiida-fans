"""Parsers provided by aiida_fans."""

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
        output_filename = self.node.get_option("output_filename")

        # Check that folder content is as expected.
        files_retrieved = set(self.retrieved.list_object_names())
        files_expected = {output_filename}
        if not files_expected <= files_retrieved:
            self.logger.error(f"Found files '{files_retrieved}', expected to find '{files_expected}'")
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # Track the output file.
        self.logger.info(f"Parsing '{output_filename}'")
        with self.retrieved.open(output_filename, "rb") as handle:
            output_node = SinglefileData(file=handle)
        self.out("results", output_node)

        return ExitCode(0)
