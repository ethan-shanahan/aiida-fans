"""CalcJob subclasses for aiida-fans calculations."""

from json import dump

from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.common.folders import Folder
from aiida.engine import CalcJob
from aiida.engine.processes.process_spec import CalcJobProcessSpec
from aiida.orm import Dict, Float, Int, List, SinglefileData, Str
from h5py import File as h5File

from aiida_fans.data import MicrostructureData
from aiida_fans.helpers import make_input_dict


class FansCalculation(CalcJob):
    """Calculations using FANS."""

    @classmethod
    def define(cls, spec: CalcJobProcessSpec) -> None:
        """Define inputs, outputs, and exit codes of the calculation."""
        super().define(spec)

        # Default Metadata
        spec.inputs["metadata"]["label"].default = "FANS"
        ## Processing Power
        spec.inputs["metadata"]["options"]["withmpi"].default = True
        spec.inputs["metadata"]["options"]["resources"].default = {"num_machines": 1, "num_mpiprocs_per_machine": 4}
        ## Filenames
        spec.inputs["metadata"]["options"]["input_filename"].default = "input.json"
        spec.inputs["metadata"]["options"]["output_filename"].default = "output.h5"
        ## Parser
        spec.inputs["metadata"]["options"]["parser_name"].default = "fans"

        # Custom Metadata
        spec.input("metadata.options.fragment_microstructure", valid_type=bool, default=False)
        spec.input("metadata.options.results_prefix", valid_type=str, default="")
        spec.input("metadata.options.results", valid_type=list, default=[])

        # Input Ports
        ## Microstructure Definition
        spec.input_namespace("microstructure")
        spec.input("microstructure.data", valid_type=MicrostructureData)
        spec.input("microstructure.L", valid_type=List)
        ## Problem Type and Material Model
        spec.input("problem_type", valid_type=Str)
        spec.input("strain_type", valid_type=Str)
        spec.input("materials", valid_type=List)
        ## Solver Settings
        spec.input("FE_type", valid_type=Str)
        spec.input("method", valid_type=Str)
        spec.input("n_it", valid_type=Int)
        spec.input_namespace("error_parameters")
        spec.input("error_parameters.measure", valid_type=Str)
        spec.input("error_parameters.type", valid_type=Str)
        spec.input("error_parameters.tolerance", valid_type=Float)
        ## Macroscale Loading Conditions
        spec.input_namespace("macroscale_loading", dynamic=True, valid_type=Dict)

        # Output Ports
        spec.output("output", valid_type=SinglefileData)
        spec.output("results", valid_type=Dict, required=False)

        # Exit Codes
        spec.exit_code(400, "PLACEHOLDER", "This is an error code, yet to be implemented.")

    def prepare_for_submission(self, folder: Folder) -> CalcInfo:
        """Prepare the calculation for submission."""
        input_dict = make_input_dict(self)
        if self.options.fragment_microstructure:
            input_dict["microstructure"]["filepath"] = "microstructure.h5"
            dataset_name: str = self.inputs.microstructure.data.dataset_name
            with folder.open("microstructure.h5", "bw") as f_dest:
                with h5File(f_dest, "w") as h5_dest:
                    with open(self.inputs.microstructure.data.file_path, mode="rb") as f_src:
                        with h5File(f_src, "r") as h5_src:
                            h5_src.copy(dataset_name, h5_dest, name=dataset_name)
        with folder.open(self.options.input_filename, "w", "utf8") as json:
            dump(input_dict, json, indent=4)

        # Specifying the code info:
        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.label + ".log"
        codeinfo.stderr_name = self.metadata.label + ".err"
        codeinfo.cmdline_params = [self.options.input_filename, self.options.output_filename]

        # Specifying the calc info:
        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = []
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = [codeinfo.stdout_name, codeinfo.stderr_name]
        calcinfo.retrieve_temporary_list = [self.options.output_filename]

        return calcinfo
