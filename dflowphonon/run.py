from dflow import config, s3_config
from dflow.plugins import bohrium
from dflow.plugins.bohrium import TiefblueClient
config["host"] = "https://workflows.deepmodeling.com"
config["k8s_api_server"] = "https://workflows.deepmodeling.com"
bohrium.config["username"] = "2043899742@qq.com"
bohrium.config["password"] = "xiaomin123!"
bohrium.config["project_id"] = "11286"
s3_config["repo_key"] = "oss-bohrium"
s3_config["storage_client"] = TiefblueClient()

import json,pathlib,argparse
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

import subprocess, os, shutil, glob,dpdata
from pathlib import Path
from typing import List
from monty.serialization import loadfn
from dflow.plugins.dispatcher import DispatcherExecutor
from dpdata.periodic_table import Element
from VASP_flow import main_vasp
from ABACUS_flow import main_abacus
from DP_flow import main_dp

parser = argparse.ArgumentParser()
parser.add_argument("--vasp", help="Using vasp code to calculate force constants",
                    action="store_true")
parser.add_argument("--abacus", help="Using abacus code to calculate force constants",
                    action="store_true")
parser.add_argument("--dp", help="Using phonolammps code , dp potential to calculate force constants",
                    action="store_true")
args = parser.parse_args()
if args.vasp:
    main_vasp()
elif args.abacus:
    main_abacus()
elif args.dp:
    main_dp()
    
