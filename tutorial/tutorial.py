import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium", app_title="AiiDA-FANS Tutorial")

with app.setup:
    import marimo as mo
    from pathlib import Path
    from aiida.common import NotExistent
    from aiida.common import MultipleObjectsError
    from aiida.orm import load_computer
    from aiida.plugins import DataFactory


    def term(lines: list[str], minimum_height: int = 0):
        return mo.Html(
            f"""
            <pre style="
                background-color: #1e1e1e; 
                color: #00ff00; 
                padding: 15px; 
                border-radius: 5px; 
                font-family: 'Courier New', monospace;
                line-height: 1.5;
            ">{"\n".join([lines[i] if i < len(lines) else " " for i in range(max(len(lines), minimum_height))])}</pre>
            """
        )


@app.cell
def _():
    nav_menu = mo.nav_menu(
        {
            "#aiida-setup": "AiiDA Setup",
            "#fans-rundown": "FANS Rundown",
            "#submitting-jobs": "Submitting Jobs",
            "#analysing-the-results": "Analysing the Results",
            "Links": {
                "https://github.com/DataAnalyticsEngineering/AiiDA-FANS": "AiiDA-FANS",
                "https://github.com/DataAnalyticsEngineering/FANS": "FANS",
                "https://www.aiida.net/": "AiiDA",
                "https://marimo.io/": "marimo",
            },
        }
    )

    _tip = mo.md("""
    **Requirements:**

    The rest of this tutorial assumes you have read the attached README and have installed the requirements described therein. Although not foolproof, if the following commands exit without error, then AiiDA, AiiDA-FANS, and FANS are probably installed correctly.

    ```sh
    verdi plugin list aiida.calculations fans
    ```
    ```sh
    FANS --version
    ```

    Notice that we assume FANS is located on your PATH (or at least it is in your active environment). While this is not necessary in general, the tutorial will continue under this assumption.
    """).callout("warn")

    mo.md(rf"""{nav_menu}

    ---

    # AiiDA-FANS Tutorial

    The goal of this tutorial is to give you an idea of how to utilise the `aiida-fans` plugin as well as an introduction to `AiiDA` and `FANS`. By the end of this tutorial, you should know how to:

    - Setup your AiiDA profile, computer, and code.
    - Define FANS options and prepare a parameter space study. 
    - Write a `submit.py` script to run your jobs.
    - Query and read the results.

    {_tip}
    """)
    return


@app.cell
def _():
    _note = mo.md(r"""
    **Note:** _not your first profile..._

    This section assumes you have not already set up an appropriate profile, computer, and code for using AiiDA and FANS. If you have already done this, you may wish to skip to the next section.

    However, this tutorial is designed to work with a blank profile specifically.
    """).callout("info")

    mo.md(rf"""
    ## AiiDA Setup

    Before we can truly begin, we must set up AiiDA on your machine. This means three things.

    1. Create a Profile
    2. Specify a Computer
    3. Define a Code

    AiiDA has multiple user interfaces but their CLI, `verdi`, is particularly well suited to these three steps since they need to be performed only rarely. Therefore, you will need access to the terminal to proceed.

    {_note}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 1. Create a Profile

    By default, AiiDA stores app data at the user level. Even when AiiDA is installed in a virtual environment, it will still read and write to `.aiida` in your home directory. However, AiiDA provides users with a way to seperate their data into "profiles". Let's create a profile for this tutorial.
    """)
    return


@app.cell
def _():
    profile_settings = (
        mo.hstack(
            [
                mo.vstack(
                    [
                        "Profile Name:",
                        "First Name:",
                        "Last Name:",
                        "Email:",
                        "Institution:",
                    ],
                    align="start",
                    heights="equal",
                    gap=0.8,
                ),
                mo.vstack(
                    [
                        "{profile_name}",
                        "{first_name}",
                        "{last_name}",
                        "{email}",
                        "{institution}",
                    ],
                    align="start",
                    heights="equal",
                    gap=0.5,
                ),
            ],
            justify="center",
            align="stretch",
            gap=1.0,
            widths=[1.0, 2.0],
        )
        .batch(
            profile_name=mo.ui.text("aiida-fans-tutorial"),
            first_name=mo.ui.text("Max"),
            last_name=mo.ui.text("Mustermann"),
            email=mo.ui.text("example@nomail.com"),
            institution=mo.ui.text("MIB"),
        )
        .form(show_clear_button=True, clear_button_label="Reset", bordered=True)
    )

    mo.vstack(
        [
            mo.md(
                "**Fill in the details below to generate your custom profile configuration.**"
            ),
            profile_settings,
        ],
        align="center",
    )
    return (profile_settings,)


@app.cell
def _(profile_settings):
    mo.stop(
        profile_settings.value is None,
        mo.status.spinner(title="Awaiting input above ...", remove_on_exit=False),
    )

    profile_config = rf"""profile: {profile_settings.value["profile_name"]}
    first_name: {profile_settings.value["first_name"]}
    last_name: {profile_settings.value["last_name"]}
    email: {profile_settings.value["email"]}
    institution: {profile_settings.value["institution"]}
    use_rabbitmq: false
    set_as_default: true
    non_interactive: true
    """

    with open("configure_profile.yaml", "w") as _f:
        _f.write(profile_config)

    mo.md(f"""
    With the values you input above, a `configure_profile.yaml` has been automatically written to the working directory. It contains the following data:

    ```yaml
    {profile_config}
    ```
    """).callout(kind="success")
    return


@app.cell(hide_code=True)
def _(profile_settings):
    mo.md(rf"""
    To create your new profile from this file run:

    ```
    verdi profile setup core.sqlite_dos --config configure_profile.yaml
    ```

    Using these commands, you should see your new profile listed (alone if this is your first profile) and a report on it also:

    ```
    verdi profile list
    verdi profile show {"<profile_name>" if profile_settings.value is None else profile_settings.value["profile_name"]}
    ```
    """)
    return


@app.cell
def _(profile_settings):
    mo.md(rf"""
    **Note:** _on default profiles..._

    We have made the new profile our default profile. This means that any further calls to `verdi` will implicitly use the {"<profile_name>" if profile_settings.value is None else profile_settings.value["profile_name"]} profile. You can change the profile on a per-call basis with the `-p/--profile` option. To change the default profile use:

    ```
    verdi profile set-default <profile_name>
    ```
    """).callout(kind="info")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 2. Specify a Computer

    Before you proceed, ensure that your local computer satisfies the following requirements:

    - it runs a Unix-like operating system (Linux distros and MacOS should work fine)
    - it has `bash` installed

    AiiDA does not assume what computer you wish to run jobs on, so even if you are only using your local machine, you must tell it as much. That is what we will do here; specify the localhost computer.
    """)
    return


@app.cell
def _():
    computer_settings = (
        mo.hstack(
            [
                mo.vstack(
                    [
                        "Computer Label:",
                        "MPI processes:",
                        "Description:",
                    ],
                    align="start",
                    heights=[1.0, 1.0, 3.0],
                    gap=0.0,
                ),
                mo.vstack(
                    [
                        "{label}",
                        "{mpiprocs}",
                        "{description}",
                    ],
                    align="start",
                    gap=0.5,
                ),
            ],
            justify="center",
            align="stretch",
            widths=[1.0, 2.0],
            gap=2.0,
        )
        .batch(
            label=mo.ui.text("localhost"),
            mpiprocs=mo.ui.text("4"),
            description=mo.ui.text_area("This is my local machine."),
        )
        .form(show_clear_button=True, clear_button_label="Reset", bordered=True)
    )

    mo.vstack(
        [
            mo.md(
                "**Fill in the details below to generate your custom computer configuration.**"
            ),
            computer_settings,
        ],
        align="center",
    )
    return (computer_settings,)


@app.cell
def _(computer_settings):
    mo.stop(
        computer_settings.value is None,
        mo.status.spinner(title="Awaiting input above ...", remove_on_exit=False),
    )

    computer_config = (
        rf"""label: {computer_settings.value["label"]}
    description: {computer_settings.value["description"]}
    hostname: localhost
    transport: core.local
    scheduler: core.direct
    shebang: #!/bin/bash
    work_dir: {Path.cwd()}/.aiida_run"""
        + r"""
    mpirun_command: mpiexec -n {tot_num_mpiprocs}"""
        + rf"""
    mpiprocs_per_machine: {computer_settings.value["mpiprocs"]}
    default_memory_per_machine: null
    use_double_quotes: false
    prepend_text: ' '
    append_text: ' '
    non_interactive: true
    """
    )

    with open("configure_computer.yaml", "w") as _f:
        _f.write(computer_config)

    mo.md(f"""
    With the values you input above, a `configure_computer.yaml` has been automatically written to the working directory. It contains the following data:

    ```yaml
    {computer_config}
    ```
    """).callout(kind="success")
    return


@app.cell(hide_code=True)
def _(computer_settings):
    mo.md(rf"""
    To specify your new computer from this file run:

    ```
    verdi computer setup --config configure_computer.yaml
    ```

    Then you must configure the computer with the following command:

    ```
    verdi computer configure core.local {"<computer_label>" if computer_settings.value is None else computer_settings.value["label"]}
    ```

    The default options should be suitable.

    Upon successfully configuring your computer, you should test that AiiDA can connect to the machine:

    ```
    verdi computer test {"<computer_label>" if computer_settings.value is None else computer_settings.value["label"]}
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 3. Define a Code

    The final step to setup AiiDA is to define the "code" you wish to utilise. Here, the "code" refers to FANS. This step is important as it tells AiiDA how to execute FANS and which plugin should handle its jobs. AiiDA provides many ways of handling the "code" of your project. Since we installed FANS in the environment, we can simply make use of it there.
    """)
    return


@app.cell
def _():
    code_settings = (
        mo.hstack(
            [
                mo.vstack(
                    [
                        mo.vstack(
                            [
                                "Code Label:",
                                # "Code Executable:",
                                "Description:",
                            ],
                            align="start",
                            heights="equal",
                            gap=0.8,
                        ),
                        "Environment Activation Script:",
                    ],
                    align="start",
                    heights="equal",
                    gap=5.55,
                ),
                mo.vstack(
                    [
                        "{label}",
                        # "{executable}",
                        "{description}",
                        "{environment}",
                    ],
                    align="start",
                    heights="equal",
                    gap=0.5,
                ),
            ],
            justify="center",
            align="stretch",
            widths=[1.5, 2.0],
            gap=2.0,
        )
        .batch(
            label=mo.ui.text("FANS"),
            executable=mo.ui.text("FANS"),
            description=mo.ui.text_area("The FANS executable."),
            environment=mo.ui.text_area("pixi shell -e tutorial"),
        )
        .form(show_clear_button=True, clear_button_label="Reset", bordered=True)
    )

    mo.vstack(
        [
            mo.md(
                "**Fill in the details below to generate your custom code configuration.**"
            ),
            code_settings,
        ],
        align="center",
    )
    return (code_settings,)


@app.cell
def _(code_settings, computer_settings):
    mo.stop(
        code_settings.value is None or computer_settings.value is None,
        mo.status.spinner(title="Awaiting input above ...", remove_on_exit=False),
    )

    code_config = rf"""label: {code_settings.value["label"]}
    description: {code_settings.value["description"]}
    default_calc_job_plugin: fans
    use_double_quotes: false
    with_mpi: true
    computer: {computer_settings.value["label"]}
    filepath_executable: FANS
    prepend_text: |
    {"\n".join([f"    {ln}" for ln in code_settings.value["environment"].split("\n")])}
    append_text: ' '
    non_interactive: true
    """

    with open("configure_code.yaml", "w") as _f:
        _f.write(code_config)

    mo.md(f"""
    With the values you input above, a `configure_code.yaml` has been automatically written to the working directory. It contains the following data:

    ```yaml
    {code_config}
    ```
    """).callout(kind="success")
    return


@app.cell(hide_code=True)
def _(code_settings):
    mo.md(rf"""
    To define your new code from this file run:

    ```
    verdi code create core.code.installed --config configure_code.yaml
    ```

    If that completed successfully, you can show the details of your new code and verify that AiiDA can connect to it using these commands:

    ```
    verdi code show {"<code_label>" if code_settings.value is None else code_settings.value["label"]}
    verdi code test {"<code_label>" if code_settings.value is None else code_settings.value["label"]}
    ```
    """)
    return


@app.cell
def _():
    mo.md(r"""
    **Note:** _your first node..._

    You should also note that the code is saved by AiiDA as a node, and thus we have created our first node. Any calculation jobs we perform will be connected to this code node in the provenance graph.

    To list all the nodes stored in your profile, run:

    ```
    verdi node list
    ```
    """).callout(kind="info")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## FANS Rundown

    FANS requires a JSON input file. The input file can be thought of in 5 sections, each specifying the various problem parameters as well as runtime settings. Each setting also notes the appropriate AiiDA datatype. This is the type of node that you must give AiiDA when running jobs, as we will see later.

    ### Microstructure Definition

    ```json
    "microstructure": {
        "filename": "microstructures/sphere32.h5",
        "datasetname": "/sphere/32x32x32/ms",
        "L": [1.0, 1.0, 1.0]
    }
    ```

    - `filename`: This specifies the path to the HDF5 file that contains the microstructure data.
    - `datasetname`: This is the path within the HDF5 file to the specific dataset that represents the microstructure.
    - `L`: Microstructure length defines the physical dimensions of the microstructure in the x, y, and z directions. (AiiDA type: `List`)

    ### Problem Type and Material Model

    ```json
    "problem_type": "mechanical",
    "strain_type": "small",
    "materials": [
        {
            "phases": [0],
            "matmodel": "LinearElasticIsotropic",
            "material_properties": {
                "bulk_modulus": [222.222],
                "shear_modulus": [166.6667]
            }
        }
    ]
    ```

    - `problem_type`: This defines the type of physical problem you are solving. Options include "thermal" problems and "mechanical" problems. (AiiDA type: `Str`)
    - `strain_type`: This indicates whether the problem is formulated using infinitesimal (small) strain or finite (large) strain theory.
    - `materials`: An array of material groups, where each group assigns one or more phases to a specific material model. See the official FANS documentation for more detail.

    ### Solver Settings

    ```json
    "FE_type": "HEX8",
    "method": "cg",
    "error_parameters":{
                         "measure": "Linfinity",
                         "type": "absolute",
                         "tolerance": 1e-10
                       },
    "n_it": 100,
    ```

    - `FE_type: This specifies the type of finite element to be used. Common options include: `HEX8`, `BBAR`, and `HEX8R`. (AiiDA type: `Str`)
    - `method`: This indicates the numerical method to be used for solving the system of equations. `cg` stands for the Conjugate Gradient method, and `fp` stands for the Fixed Point method. (AiiDA type: `Str`)
    - `error_parameters`: This section defines the error parameters for the solver. Error control is applied on the finite element nodal residual of the problem.
        - `measure`: Specifies the norm used to measure the error. Options include `Linfinity`, `L1`, or `L2`. (AiiDA type: `Str`)
        - `type`: Defines the type of error measurement. Options are `absolute` or `relative`. (AiiDA type: `Str`)
        - `tolerance`: Sets the tolerance level for the solver, defining the convergence criterion based on the chosen error measure. The solver iterates until the solution meets this tolerance. (AiiDA type: `Float`)
    - `n_it`: Specifies the maximum number of iterations allowed for the FANS solver. (AiiDA type: `Int`)


    ### Macroscale Loading Conditions

    ```json
    "macroscale_loading":   [
                                [
                                    [0.004, -0.002, -0.002, 0, 0, 0],
                                    [0.008, -0.004, -0.004, 0, 0, 0],
                                    [0.012, -0.006, -0.006, 0, 0, 0],
                                    [0.016, -0.008, -0.008, 0, 0, 0],
                                ],
                                [
                                    [0, 0, 0, 0.002, 0, 0],
                                    [0, 0, 0, 0.004, 0, 0],
                                    [0, 0, 0, 0.006, 0, 0],
                                    [0, 0, 0, 0.008, 0, 0],
                                ]
                            ]
    ```

    - `macroscale_loading`: This defines the external loading applied to the microstructure. It is an array of arrays, where each sub-array represents a loading condition applied to the system. The format of the loading array depends on the problem type. See the official FANS documentation for more details.

    ### Results Specification

    ```json
    "results": [
        "stress", "strain",
        "stress_average", "strain_average",
        "phase_stress_average", "phase_strain_average",
        "displacement", "displacement_fluctuation",
        "absolute_error",
        "microstructure",
    ]
    ```

    - `results`: This array lists the quantities that should be stored into the results HDF5 file during the simulation. Each string in the array corresponds to a specific result. See the official FANS documentation for more details.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Submitting Jobs

    Now that AiiDA is suitably prepared and we're familiar with the FANS parameter specifications, it's time to get to work. We will make use of the plugin's `utils` subpackage to conveniently and reliably construct our input parameters and execute FANS.
    """)
    return


@app.cell(hide_code=True)
def _(computer_settings):
    mo.md(rf"""
    ### Including the Microstructure

    Before stepping into the common workflow, we will perform one more step which is to make AiiDA aware of our microstructure data. We will use AiiDA's interactive shell and the plugin's custom data type to create a new node in the database.

    Start an interactive shell with the default AiiDA profile.

    ```sh
    verdi shell
    ```

    Use `DataFactory` to load the plugin's custom data type, then create and store the new node.

    ```python
    MicrostructureData = DataFactory('fans.microstructure')
    MicrostructureData(
        file_path='{str(Path("tutorial_microstructure.h5").absolute())}',
        dataset_name='/dset_0/image',
        computer=load_computer(label='{"localhost" if computer_settings.value is None else computer_settings.value["label"]}'),
        label='microstructure.data'
    ).store()
    ```

    Once the node is stored in the database, you can leave the interactive shell.

    ```python
    exit()
    ```
    """)
    return


@app.cell
def _():
    mo.md(rf"""
    **Note:** _on node reuse..._

    To reuse this node when executing FansCalculation jobs, you can use `load_node(label='microstructure.data')` as long as only one node exists with the provided label. If you intend on using multiple files and/or multiple groups within individual files, assign each node a distinct and identifiable label.
    """).callout("info")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### The `submit.py` Script

    Although nothing is stopping you from executing jobs in the terminal, it is common practice to write a `submit.py` script so that you can clearly map out your inputs and handle other menial tasks, especially for jobs with very many input parameters. We will walk through the process of writing this script step-by-step. You can then take that knowledge, and the final script, to rewrite/modify elsewhere.

    We begin by importing some necessary components and loading the default profile.

    ```py
    from aiida import load_profile
    from aiida.orm import load_code, load_node

    from aiida_fans.utils import run_fans

    load_profile()
    ```
    """)
    return


@app.cell
def _():
    # import_button = mo.ui.run_button(label="RUN")
    return


@app.cell
def _():
    # mo.stop(
    #     not import_button.value,
    #     output=import_button.style(text_align="center").callout(kind="neutral"),
    # )  # run on click

    # try:
    #     from aiida import load_profile
    #     from aiida.orm import load_code, load_node

    #     from aiida_fans.utils import run_fans

    #     load_profile()


    # except ImportError:
    #     mo.stop(
    #         True,
    #         output=mo.md("**Imports failed to load properly!**")
    #         .style(text_align="center")
    #         .callout(kind="danger"),
    #     )

    # except ProfileConfigurationError:
    #     mo.stop(
    #         True,
    #         output=mo.md("**Profile failed to load properly!**")
    #         .style(text_align="center")
    #         .callout(kind="danger"),
    #     )

    # mo.md("**Success!**").style(text_align="center").callout(kind="success")
    return


@app.cell(hide_code=True)
def _(code_settings):
    mo.md(rf"""
    Next, we will construct the input dictionary. This will look very similar to the json input file, described [above](#fans-rundown), but with a few key differences.

    ```python
    inputs = {{
        "code": load_code(label="{"FANS" if code_settings.value is None else code_settings.value["label"]}"),
        "microstructure": {{
            "data": load_node(label="microstructure.data"),
            "L": [1.0, 1.0, 1.0]
        }},
        "problem_type": "mechanical",
        "strain_type": "small",
        "materials": [
            {{
                "phases": [0],
                "matmodel": "LinearElasticIsotropic",
                "material_properties": {{"bulk_modulus": [222.222], "shear_modulus": [166.6667]}}
            }}
        ],
        "FE_type": "HEX8",
        "method": "cg",
        "n_it": 100,
        "error_parameters": {{"measure": "Linfinity", "type": "absolute", "tolerance": 1e-10}},
        "macroscale_loading": [
            {{
                "strain_indices": [2, 3, 4, 5],
                "stress_indices": [0, 1],
                "strain": [[0.005, 0.0, 0.0, 0.0], [0.010, 0.0, 0.0, 0.0]],
                "stress": [[0.0, 0.0], [0.0, 0.0]]
            }}
        ],
        "metadata": {{
            "options": {{
                "results_prefix": "my_results",
                "results": [
                    "stress_average",
                    "strain_average"
                ]
            }}
        }}
    }}
    ```

    **Differences:**

    1. `"code":` This is an additional input that AiiDA requires. You must load the code node you defined [above](#define-a-code). This can be done with the built-in `load_code` function by passing it the label you used earlier.
    2. `"microstructure": {{"data": ...}}` This input replaces two inputs from the FANS input json, `"microstructure": {{"filepath": ..., "datasetname": ...`. For this input, you must load the `MicrostructureData` node you created [above](#including-the-microstructure) using the built-in `load_node` function and passing it the label you used earlier. This architectural change was made to maintain the integrity of AiiDA's data provenance.
    3. `"metadata": {{"options": {{"results_prefix": ..., "results": ...}}` The `"results_prefix"` and `"results"` input parameters have been relocated to better suit AiiDA architecture. Since these are essentially optional parameters that have no bearing on the actual calculations FANS performs, they are appropriate parameters for AiiDA's `"metadata"` input. Learn more about what the `"metadata"` input is for, such as labelling your calculations and initiating dry runs, on the AiiDA documentation.
    """)
    return


@app.cell
def _():
    # load_inputs_button = mo.ui.run_button(label="RUN")
    return


@app.cell
def _():
    # mo.stop(
    #     not load_inputs_button.value,
    #     output=load_inputs_button.style(text_align="center").callout(
    #         kind="neutral"
    #     ),
    # )  # run on click

    # # check load_code first
    # try:
    #     loaded_code = load_code(
    #         label="FANS"
    #         if code_settings.value is None
    #         else code_settings.value["label"]
    #     )

    # except NotExistent:
    #     mo.stop(
    #         True,
    #         output=mo.md(
    #             f"**No code with the provided label exists!** {load_inputs_button}"
    #         )
    #         .style(text_align="center")
    #         .callout(kind="danger"),
    #     )

    # except MultipleObjectsError:
    #     mo.stop(
    #         True,
    #         output=mo.md(
    #             f"**Multiple codes with the provided label exists!** {load_inputs_button}"
    #         )
    #         .style(text_align="center")
    #         .callout(kind="danger"),
    #     )

    # # check load_node second
    # try:
    #     loaded_data = load_node(label="microstructure.data")

    # except NotExistent:
    #     mo.stop(
    #         True,
    #         output=mo.md(
    #             f"**No MicrostructureData node with the provided label exists!** {load_inputs_button}"
    #         )
    #         .style(text_align="center")
    #         .callout(kind="danger"),
    #     )

    # except MultipleObjectsError:
    #     mo.stop(
    #         True,
    #         output=mo.md(
    #             f"**Multiple MicrostructureData nodes with the provided label exists!** {load_inputs_button}"
    #         )
    #         .style(text_align="center")
    #         .callout(kind="danger"),
    #     )


    # inputs = {
    #     "code": loaded_code,
    #     "microstructure": {"data": loaded_data, "L": [1.0, 1.0, 1.0]},
    #     "problem_type": "mechanical",
    #     "strain_type": "small",
    #     "materials": [
    #         {
    #             "phases": [0],
    #             "matmodel": "LinearElasticIsotropic",
    #             "material_properties": {
    #                 "bulk_modulus": [222.222],
    #                 "shear_modulus": [166.6667],
    #             },
    #         }
    #     ],
    #     "FE_type": "HEX8",
    #     "method": "cg",
    #     "n_it": 100,
    #     "error_parameters": {
    #         "measure": "Linfinity",
    #         "type": "absolute",
    #         "tolerance": 1e-10,
    #     },
    #     "macroscale_loading": [
    #         {
    #             "strain_indices": [2, 3, 4, 5],
    #             "stress_indices": [0, 1],
    #             "strain": [[0.005, 0.0, 0.0, 0.0], [0.010, 0.0, 0.0, 0.0]],
    #             "stress": [[0.0, 0.0], [0.0, 0.0]],
    #         }
    #     ],
    #     "metadata": {
    #         "options": {
    #             "results_prefix": "my_results",
    #             "results": ["stress_average", "strain_average"],
    #         }
    #     },
    # }

    # mo.md("**Success!**").style(text_align="center").callout(kind="success")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Now that the inputs dictionary has been prepared, it is time to launch the calculation job. As previously stated, will be using `run_fans` from the `aiida_fans.utils` subpackage. All we need to do is pass in the inputs dictionary.

    ```python
    run_fans(inputs)
    ```

    The `run_fans` funciton (and the related `submit_fans` function) performs a few extra tasks before calling `aiida.engine.run` (or `aiida.engine.submit`, respectively). It checks each non-node entry in the dictionary and tries to find an existing node whose value matches that which was provided and whose label matches the dictionary key of that input (using dot notation for embedded dictionaries). Additionally, if there exists a calculation whose inputs perfectly match the inputs provided, confirmation to proceed will be sought.

    These routine duties go a long way towards making your life easier when working with AiiDA.
    """)
    return


@app.cell
def _():
    # run_fans_button = mo.ui.run_button(label="RUN")
    return


@app.cell
def _():
    # mo.stop(
    #     not run_fans_button.value,
    #     output=run_fans_button.style(text_align="center").callout(kind="neutral"),
    # )  # run on click

    # from aiida.tools import delete_nodes
    # delete_nodes(range(3, 20), dry_run=False)

    # try:
    #     run_fans(inputs)

    # except Exception as e:
    #     mo.stop(
    #         True,
    #         output=mo.md(
    #             f"**Error:** {e} : {load_inputs_button}"
    #         )
    #         .style(text_align="center")
    #         .callout(kind="danger"),
    #     )


    # mo.md("**Success!**").style(text_align="center").callout(kind="success")
    return


@app.cell
def _():
    write_script_button = mo.ui.run_button(label="WRITE")
    return (write_script_button,)


@app.cell
def _(code_settings, write_script_button):
    mo.stop(
        not write_script_button.value,
        output=mo.md(
            rf"Write the `submit.py` script to the working directory: {write_script_button}"
        )
        .style(text_align="center")
        .callout(kind="neutral"),
    )  # run on click

    script_file = Path("submit.py")
    script = rf"""from aiida import load_profile
    from aiida.orm import load_code, load_node

    from aiida_fans.utils import run_fans

    load_profile()

    #############################################################################################

    inputs = {{
        "code": load_code(label="{"FANS" if code_settings.value is None else code_settings.value["label"]}"),
        "microstructure": {{
            "data": load_node(label="microstructure.data"),
            "L": [1.0, 1.0, 1.0]
        }},
        "problem_type": "mechanical",
        "strain_type": "small",
        "materials": [
            {{
                "phases": [0,1],
                "matmodel": "LinearElasticIsotropic",
                "material_properties": {{
                    "bulk_modulus": [62.5000, 222.222],
                    "shear_modulus": [28.8462, 166.6667]
                }}
            }}
        ],
        "FE_type": "HEX8",
        "method": "cg",
        "n_it": 100,
        "error_parameters": {{"measure": "Linfinity", "type": "absolute", "tolerance": 1e-10}},
        "macroscale_loading": [
            {{
                "strain_indices": [2, 3, 4, 5],
                "stress_indices": [0, 1],
                "strain": [[0.005, 0.0, 0.0, 0.0], [0.010, 0.0, 0.0, 0.0]],
                "stress": [[0.0, 0.0], [0.0, 0.0]]
            }}
        ],
        "metadata": {{
            "options": {{
                "results_prefix": "my_results",
                "results": [
                    "stress_average",
                    "strain_average"
                ]
            }}
        }}
    }}

    #############################################################################################

    run_fans(inputs)
    """

    try:
        script_file.write_text(script)

    except Exception as e:
        script_file.unlink(missing_ok=True)
        mo.stop(
            True,
            output=mo.md(f"**Error:** {e} : {write_script_button}")
            .style(text_align="center")
            .callout(kind="danger"),
        )


    mo.md("**Success!**").style(text_align="center").callout(kind="success")
    return


@app.cell(hide_code=True)
def _():
    mo.md(rf"""
    You will find the complete script in the tutorial directory: `{Path("submit.py").absolute()}`

    Now, simply run the script.
    """)
    return


@app.cell
def _():
    mo.md(r"""
    **Note:** _more nodes..._

    Your profile should now be stocked with a whole range of new nodes, the input nodes. FANS may take a moment to finish, but while it's working, use another terminal to check out the database.

    To list all the nodes stored in your profile, and display some important identifiers, run:

    ```
    verdi node list --project id label node_type
    ```

    To display even more details about a specific node, try running the following on the new `CalcJobNode` representing the FANS calculation:

    ```sh
    verdi node show <pk>
    ```

    *Hint: if you've followed along exactly, the `CalcJobNode`'s primary key (pk) should be 14.*

    If you catch the process while it is still running, you should see that the `state` property is "`Waiting`". Once FANS has completed its calculations and AiiDA has processed its results, the `state` property should read "`Finished [0]`". 
    """).callout(kind="info")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    MOOOOOOORREEEEEEEEE
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Analysing the Results

    Once our calculations are complete, you can use can use a few ways to inspect the output or otherwise handle the data.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 1. Using the CLI

    The plugin's parser is capable of extracting certain results from the `output.h5` file produced by FANS. If the strain and stress averages were requested, then a `results` node should be accessible. The verdi CLI tool has a quick way of showing the attributes (the stored values) of individual nodes. Run this command, providing the primary key of the results node (probably 18):

    ```sh
    verdi node attributes <pk>
    ```

    You should see the strain average and stress average vectors for both time steps of the loading conditions we specified.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 2. Using Scripting

    This approach is useful for conglomerating various nodes by comparison to some metric. First, let's import some important components:

    ```python
    from aiida import load_profile
    from aiida.orm import QueryBuilder, CalcJobNode

    load_profile()
    ```
    """)
    return


@app.cell
def _():
    import_query_button = mo.ui.run_button(label="RUN")
    return (import_query_button,)


@app.cell
def _(ProfileConfigurationError, import_query_button):
    mo.stop(
        not import_query_button.value,
        output=import_query_button.style(text_align="center").callout(
            kind="neutral"
        ),
    )  # run on click

    try:
        from aiida import load_profile
        from aiida.orm import QueryBuilder, CalcJobNode

        load_profile()

    except ImportError:
        mo.stop(
            True,
            output=mo.md(
                f"**Imports failed to load properly!** {import_query_button}"
            )
            .style(text_align="center")
            .callout(kind="danger"),
        )

    except ProfileConfigurationError:
        mo.stop(
            True,
            output=mo.md(
                f"**Profile failed to load properly!** {import_query_button}"
            )
            .style(text_align="center")
            .callout(kind="danger"),
        )

    mo.md("**Success!**").style(text_align="center").callout(kind="success")
    return CalcJobNode, QueryBuilder


@app.cell
def _():
    mo.md(r"""
    Next, let's perform a simple query to fetch all the nodes of type `CalcJobNode`. This is the AiiDA data type given to nodes that represent the exectution of an individual job. Here are the three parts that go into such a query:

    1. `QueryBuilder()`: Initializes the query engine which acts as the interface to search and filter through the AiiDA database.
    2. `.append(CalcJobNode)`: Adds a requirement to the query to search for all nodes that are instances of a `CalcJobNode`.
    3. `.all(flat=True)`: Executes the query and returns all matching results in a single, flattened list rather than a nested list of lists.

    Altogether:

    ```python
    QueryBuilder().append(CalcJobNode).all(flat=True)
    ```
    """)
    return


@app.cell
def _():
    simple_query_button = mo.ui.run_button(label="RUN")
    return (simple_query_button,)


@app.cell
def _(CalcJobNode, QueryBuilder, simple_query_button):
    mo.stop(
        not simple_query_button.value,
        output=mo.vstack(
            [
                simple_query_button.style(text_align="center").callout(
                    kind="neutral"
                ),
                term(["OUTPUT..."], 2),
            ]
        ),
    )  # run on click

    try:
        simple_query = QueryBuilder().append(CalcJobNode).all(flat=True)

    except Exception as e:
        mo.stop(
            True,
            output=mo.vstack(
                [
                    mo.md(f"**Error: {e}** {simple_query_button}")
                    .style(text_align="center")
                    .callout(kind="danger"),
                    term(["OUTPUT..."], 2),
                ]
            ),
        )


    mo.vstack(
        [
            mo.md(f"**Success!** {simple_query_button}")
            .style(text_align="center")
            .callout(kind="success"),
            term([f"> {sq}" for sq in simple_query], 2),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(rf"""
    Finally, let's perform a slightly more advanced query that illustrates how you can leverage the SQL database to conglomerate swathes of nodes matching any criteria you like. With this query we aim to gather the list of all CalcJobNodes who use a certain microstructure dataset. To be exact, a microstructure dataset that fits this description:

    ```python
    MicrostructureData(
        "{str(Path("tutorial_microstructure.h5").absolute())}",
        "/dset_0/image",
    )
    ```

    This will be done much in the same way as the previous query, except this time we will chain it together with another `.append()` call. The new `.append()` queries for nodes of the type `MicrostructureData` and filters them based off the `file_path` and `dataset_name` attributes. The `tag` parameter allows us to request, in the following `.append()`, nodes of type `CalcJobNode` with specific incoming nodes.

    ```python
    MicrostructureData = DataFactory('fans.microstructure')
    QueryBuilder(
    ).append(
        MicrostructureData,
        filters={{
            "attributes.remote_path": "{str(Path("tutorial_microstructure.h5").absolute())}",
            "attributes.dataset_name": "/dset_0/image",
        }},
        tag="ms"
    ).append(
        CalcJobNode,
        with_incoming="ms"
    ).all(flat=True)
    ```
    """)
    return


@app.cell
def _():
    complex_query_button = mo.ui.run_button(label="RUN")
    return (complex_query_button,)


@app.cell
def _(CalcJobNode, QueryBuilder, complex_query_button):
    mo.stop(
        not complex_query_button.value,
        output=mo.vstack(
            [
                complex_query_button.style(text_align="center").callout(
                    kind="neutral"
                ),
                term(["OUTPUT..."], 2),
            ]
        ),
    )  # run on click

    try:
        MicrostructureData = DataFactory("fans.microstructure")
        complex_query = (
            QueryBuilder()
            .append(
                MicrostructureData,
                filters={
                    "attributes.file_path": str(
                        Path("tutorial_microstructure.h5").absolute()
                    ),
                    "attributes.dataset_name": "/dset_0/image",
                },
                tag="ms",
            )
            .append(CalcJobNode, with_incoming="ms")
            .all(flat=True)
        )

    except Exception as e:
        mo.stop(
            True,
            output=mo.vstack(
                [
                    mo.md(f"**Error: {e}** {complex_query_button}")
                    .style(text_align="center")
                    .callout(kind="danger"),
                    term(["OUTPUT..."], 2),
                ]
            ),
        )

    mo.vstack(
        [
            mo.md(f"**Success!** {complex_query_button}")
            .style(text_align="center")
            .callout(kind="success"),
            term([f"> {cq}" for cq in complex_query], 2),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### 3. Using Graphs

    The last piece of advice we will mention here is about how to visualise the graph of your database. The `verdi` CLI tool supplies a command to generate graph data in a few forms. For example, you could request that it outputs the graph in the DOT language format, and use your own tools to visualise, manipulate, and interrogate the data. By default, `verdi` will immediately create a `.pdf` file showing the graph connected to a root node you specify. Try running this command on a `CalcJobNode` we have produced.

    ```sh
    verdi node graph generate --show <pk>
    ```

    If the file doesn't open automatically, you should be able to find it in your working directory, titled "`<pk>.dot.pdf`".
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Appendix
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A. `fetch()`

    This is a helper function to simplify the querying of individual nodes when the label and value are known.
    """)
    return


@app.cell
def _(Dict, Float, Int, List, QueryBuilder, Str):
    def fetch(label: str, value):
        """Helper function to return a node whose label and value are known.

        Returns an error if more or less than 1 suitable node is found.
        """
        match value:
            case str():
                datatype = Str
            case int():
                datatype = Int
            case float():
                datatype = Float
            case list():
                datatype = List
            case dict():
                datatype = Dict
            case _:
                raise NotImplementedError

        bone = (
            QueryBuilder()
            .append(
                datatype,
                filters={datatype.fields.label: label, "attributes.value": value}
                if datatype is not List
                else {datatype.fields.label: label, "attributes.list": value},
            )
            .all(flat=True)
        )

        if len(bone) != 1:
            raise RuntimeError

        return bone.pop()


    mo.show_code()
    return


if __name__ == "__main__":
    app.run()
