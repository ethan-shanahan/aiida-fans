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
        spec.input_namespace("microstructure", help=(note:="The microstructure definition."))
        spec.input.microstructure("filename",       valid_type=Str,     validator=lambda x: None, help=(note:="This specifies the path to the HDF5 file that contains the microstructure data."))
        spec.input.microstructure("datasetname",    valid_type=Str,     validator=lambda x: None, help=(note:="This is the path within the HDF5 file to the specific dataset that represents the microstructure."))
        spec.input.microstructure("L",              valid_type=List,    validator=lambda x: note if len(x) != 3 else None, help=(note:="Microstructure length defines the physical dimensions of the microstructure in the x, y, and z directions."))
        spec.input("problem_type",          valid_type=Str,         validator=lambda x: note if x not in {"thermal", "mechanical"} else None, help=(note:="This defines the type of physical problem you are solving. Common options include `thermal` problems and `mechanical` problems."))
        spec.input("matmodel",              valid_type=Str,         validator=lambda x: note if x not in {"LinearThermalIsotropic", "LinearElasticIsotropic", "PseudoPlasticLinearHardening", "PseudoPlasticNonLinearHardening"} else None, help=(note:="This specifies the material model to be used in the simulation."))
        spec.input("material_properties",   valid_type=Dict,        validator=lambda x: material_properties_validator(x, note), help=(note:="This provides the necessary material parameters for the chosen material model."))
        spec.input("method",                valid_type=Str,         validator=lambda x: note if x not in {"gc", "fp"} else None, help=(note:="This indicates the numerical method to be used for solving the system of equations. `cg` stands for the Conjugate Gradient method, and `fp` stands for the Fixed Point method."))
        spec.input_namespace("error_parameters", help=(note:="This section defines the error parameters for the solver. Error control is applied on the finite element nodal residual of the problem."))
        spec.input.error_parameters("measure",      valid_type=Str,     validator=lambda x: note if x not in {"Linfinity", "L1", "L2"} else None, help=(note:="Specifies the norm used to measure the error. Options include `Linfinity`, `L1`, or `L2`."))
        spec.input.error_parameters("type",         valid_type=Str,     validator=lambda x: note if x not in {"absolute", "relative"} else None, help=(note:="Defines the type of error measurement. Options are `absolute` or `relative`."))
        spec.input.error_parameters("tolerance",    valid_type=Float,   validator=lambda x: None, help=(note:="Sets the tolerance level for the solver, defining the convergence criterion based on the chosen error measure. The solver iterates until the solution meets this tolerance."))
        spec.input("n_it",                  valid_type=Int,         validator=lambda x: None, help=(note:="Specifies the maximum number of iterations allowed for the FANS solver."))
        spec.input("macroscale_loading",    valid_type=ArrayData,   validator=lambda x: macroscale_loading_validator(x, note), help=(note:="This defines the external loading applied to the microstructure. It is an array of arrays, where each sub-array represents a loading condition applied to the system. The format of the loading array depends on the problem type"))
        spec.input("results",               valid_type=List,        validator=lambda x: results_validator(x, note), help=(note:="This array lists the quantities that should be stored into the results HDF5 file during the simulation."))
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
