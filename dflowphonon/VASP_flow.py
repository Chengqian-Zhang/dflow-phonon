import json,pathlib
from typing import List
from dflow import (
    Workflow,
    Step,
    argo_range,
    SlurmRemoteExecutor,
    upload_artifact,
    download_artifact,
    InputArtifact,
    OutputArtifact,
    ShellOPTemplate
)
from dflow.python import (
    PythonOPTemplate,
    OP,
    OPIO,
    OPIOSign,
    Artifact,
    Slices,
    upload_packages
)
import time
import subprocess, os, shutil, glob
from pathlib import Path
from typing import List
from dflow.plugins.dispatcher import DispatcherExecutor
from monty.serialization import loadfn
from monty.serialization import loadfn
from dflow.python import upload_packages
upload_packages.append(__file__)
from dflowphonon.VASP_OPs import PhononMakeVASP,VASP,PhononPostVASP

def main_vasp():
    global_param = loadfn("global.json")
    work_dir = global_param.get("work_dir",None)
    email = global_param.get("email",None)
    password = global_param.get("password",None)
    program_id = global_param.get("program_id",None)
    phonopy_image_name = global_param.get("phonopy_image_name",None)
    vasp_image_name = global_param.get("vasp_image_name",None)
    abacus_image_name = global_param.get("abacus_image_name",None)
    phonolammps_image_name = global_param.get("phonolammps_image_name",None)
    cpu_scass_type = global_param.get("cpu_scass_type",None)
    gpu_scass_type = global_param.get("gpu_scass_type",None)

    dispatcher_executor_cpu = DispatcherExecutor(
        machine_dict={
            "batch_type": "Bohrium",
            "context_type": "Bohrium",
            "remote_profile": {
                "input_data": {
                    "job_type": "container",
                    "platform": "ali",
                    "scass_type": cpu_scass_type,
                },
            },
        },
    )

    dispatcher_executor_gpu = DispatcherExecutor(
        machine_dict={
            "batch_type": "Bohrium",
            "context_type": "Bohrium",
            "remote_profile": {
                "input_data": {
                    "job_type": "container",
                    "platform": "ali",
                    "scass_type": gpu_scass_type,
                },
            },
        },
    )

    cwd = os.getcwd()
    #work_dir = os.path.join(cwd,work_dir)
    work_dir = cwd
    wf = Workflow(name = "phonon")

    phononmake = Step(
        name="Phononmake", 
        template=PythonOPTemplate(PhononMakeVASP,image=phonopy_image_name,command=["python3"]),
        artifacts={"input":upload_artifact(work_dir)},
        )
    wf.add(phononmake)
   
    vasp = PythonOPTemplate(VASP,slices=Slices("{{item}}", input_artifact=["input_dfpt"],output_artifact=["output_dfpt"]),image=vasp_image_name,command=["python3"])
    vasp_cal = Step("VASP-Cal",template=vasp,artifacts={"input_dfpt":phononmake.outputs.artifacts["jobs"]},with_param=argo_range(phononmake.outputs.parameters["njobs"]),key="VASP-Cal-{{item}}",executor=dispatcher_executor_cpu)   
    wf.add(vasp_cal)

    phononpost = Step(
        name="Phononpost", 
        template=PythonOPTemplate(PhononPostVASP,image=phonopy_image_name,command=["python3"]),
        artifacts={"input_post":vasp_cal.outputs.artifacts["output_dfpt"]},
        parameters={"path":cwd}
        )
    wf.add(phononpost)

    wf.submit()

    while wf.query_status() in ["Pending","Running"]:
        time.sleep(4)
    assert(wf.query_status() == 'Succeeded')
    step = wf.query_step(name="Phononpost")[0]
    download_artifact(step.outputs.artifacts["output_post"])