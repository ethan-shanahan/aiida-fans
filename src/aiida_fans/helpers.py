"""Tools required by aiida-fans."""

from typing import Any

from aiida.engine import CalcJob
from numpy import allclose, ndarray


def make_input_dict(job: CalcJob) -> dict[str, Any]:
    """Prepares a dictionary that maps to an input.json from calcjob inputs."""
    return {
        ## Microstructure definition
        "microstructure": {
            "filepath": job.inputs.microstructure.file.get_remote_path(),
            "datasetname": job.inputs.microstructure.datasetname.value,
            "L": job.inputs.microstructure.L.get_list(),
        },
        ## Problem type and material model
        "problem_type": job.inputs.problem_type.value,
        "strain_type": job.inputs.strain_type.value,
        "materials": job.inputs.materials.get_list(),
        ## Solver settings
        "FE_type": job.inputs.FE_type.value,
        "method": job.inputs.method.value,
        "n_it": job.inputs.n_it.value,
        "error_parameters": {
            "measure": job.inputs.error_parameters.measure.value,
            "type": job.inputs.error_parameters.type.value,
            "tolerance": job.inputs.error_parameters.tolerance.value,
        },
        ## Macroscale loading conditions
        "macroscale_loading": [load.value for load in job.inputs.macroscale_loading.values()],
        ## Results specification (Optional)
        "results_prefix": job.inputs.metadata.options.results_prefix,
        "results": job.inputs.metadata.options.results,
    }


def arraydata_equal(first: dict[str, ndarray], second: dict[str, ndarray]) -> bool:
    """Return whether two dicts of arrays are roughly equal."""
    if first.keys() != second.keys():
        return False
    return all(allclose(first[key], second[key]) for key in first)
