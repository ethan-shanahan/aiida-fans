"""
Calculations provided by aiida_faux.
"""

from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.common.folders import Folder
from aiida.engine import CalcJob
from aiida.engine.processes.process_spec import CalcJobProcessSpec
from aiida.orm import Str, Int, Float, List, Dict, ArrayData


def material_properties_validator(x:Dict, note:str) -> str | None:
    pass # TODO
    return note if 0 else None

def macroscale_loading_validator(x:ArrayData, note:str) -> str | None:
    pass # TODO
    return note if 0 else None

def results_validator(x:List, note:str) -> str | None:
    valid = {"stress_average", "strain_average", "absolute_error", "phase_stress_average", "phase_strain_average", "microstructure", "displacement", "stress", "strain"}
    return note if x.get_list() > valid else None


class FANSCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the FANS executable.
    """

    @classmethod
    def define(cls, spec: CalcJobProcessSpec) -> None:
        """
        Define inputs, outputs, and exit_codes of the calculation.
        """
        super().define(spec)

        # New Ports:
        spec.input("")
        spec.output("")

        # Exit Codes:
        spec.exit_code(400, "", "")
    
    def prepare_for_submission(self, folder: Folder) -> CalcInfo:
        """Creates the input file required by the calculation.

        Args:
            folder (Folder): where the plugin should temporarily place all files needed by the calculation

        Returns:
            CalcInfo: the data to be passed to the ExecManager
        """

        # Generating the input file.
        pass
        with folder.open("", "w", "utf8") as handle:
            handle.write("")
        
        # Specifying code info.
        codeinfo = CodeInfo()

        # Specifying calc info.
        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]

        return calcinfo
