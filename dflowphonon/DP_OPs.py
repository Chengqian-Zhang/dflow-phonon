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

import subprocess, os, shutil, glob,dpdata
from pathlib import Path
from typing import List
from dflow.plugins.bohrium import BohriumContext, BohriumExecutor
from dpdata.periodic_table import Element
from monty.serialization import loadfn

from dflow.python import upload_packages
upload_packages.append(__file__)

def element_list(type_map):
    type_map_reverse = {k: v for v, k in type_map.items()}
    type_map_list = []
    tmp_list = list(type_map_reverse.keys())
    tmp_list.sort()
    for ii in tmp_list:
        type_map_list.append(type_map_reverse[ii])
    return type_map_list

class PhononMakeDP(OP):
    """
    class for making calculation tasks
    """
    def __init__(self):
        pass

    @classmethod
    def get_input_sign(cls):
        return OPIOSign({
            'input': Artifact(Path)
        })
 
    @classmethod
    def get_output_sign(cls):
        return OPIOSign({
            'output' : Artifact(Path),
        })

    @OP.exec_sign_check
    def execute(
            self,
            op_in: OPIO,
    ) -> OPIO:
        cwd = os.getcwd()

        os.chdir(op_in["input"])
        work_d = os.getcwd()

        parameter = loadfn("param.json")["properties"]
        inter_param_prop = loadfn("param.json")["interaction"]
        parameter['primitive'] = parameter.get('primitive', False)
        parameter['approach'] =parameter.get('approach', "linear")
        band_path = parameter['band_path']
        supercell_matrix = parameter['supercell_matrix']
        primitive = parameter['primitive']
        approach = parameter['approach']
        type_map = inter_param_prop["type_map"]
        type_map_list = element_list(type_map)
        MESH = parameter.get('MESH',None)
        PRIMITIVE_AXES = parameter.get('PRIMITIVE_AXES',None)
        BAND_POINTS = parameter.get('BAND_POINTS',None)
        BAND_CONNECTION = parameter.get('BAND_CONNECTION',True)

        if primitive:
            subprocess.call('phonopy --symmetry',shell=True)
            subprocess.call('cp PPOSCAR POSCAR',shell=True)
            shutil.copyfile("PPOSCAR","POSCAR-unitcell")
        else:
            shutil.copyfile("POSCAR","POSCAR-unitcell")
        
        with open("POSCAR","r") as fp:
            lines = fp.read().split('\n')
            ele_list = lines[5].split()
        
        output_task = os.path.join(work_d,'task.000000')
        os.makedirs(output_task,exist_ok=True)
        os.chdir(output_task)
        os.symlink(os.path.join(work_d,"POSCAR-unitcell"),"POSCAR")
        os.symlink(os.path.join(work_d,"frozen_model.pb"),"frozen_model.pb")
        with open("POSCAR",'r') as fp :
            lines = fp.read().split('\n')
            ele_list = lines[5].split()

        ## band.conf
        ret = ""
        ret += "ATOM_NAME ="
        for ii in ele_list:
            ret += " %s"%(ii)
        ret += "\n"
        ret += "DIM = %s %s %s\n"%(supercell_matrix[0],supercell_matrix[1],supercell_matrix[2])
        if MESH:
                ret += "MESH = %s %s %s\n"%(MESH[0],MESH[1],MESH[2])
        if PRIMITIVE_AXES:
                ret += "PRIMITIVE_AXES = %s\n"%(PRIMITIVE_AXES)
        ret += "BAND = %s\n"%(band_path)
        if BAND_POINTS:
            ret += "BAND_POINTS = %s\n"%(BAND_POINTS)
        if BAND_CONNECTION:
            ret += "BAND_CONNECTION = %s\n"%(BAND_CONNECTION)
        ret += "FORCE_CONSTANTS=READ\n"
        with open("band.conf","a") as fp:
            fp.write(ret) 

        ##in.lammps
        ret = ""
        ret += "clear\n"
        ret += "units   metal\n"
        ret += "dimension       3\n"
        ret += "boundary        p p p\n"
        ret += "atom_style      atomic\n"
        ret += "box         tilt large\n"
        ret += "read_data   conf.lmp\n"
        ntypes = len(type_map_list)
        for ii in range(ntypes):
            ret += "mass            %d %f\n" % (ii + 1, Element(type_map_list[ii]).mass)
        ret += "neigh_modify    every 1 delay 0 check no\n"
        ret += "pair_style      deepmd frozen_model.pb\n"
        ret += "pair_coeff      * *\n"
        with open("in.lammps","a") as f:
            f.write(ret)
        
        #conf.lmp
        ls = dpdata.System("POSCAR",type_map=type_map_list)
        ls.to(fmt="lmp",file_name="conf.lmp") 
        
        os.chdir(cwd)
        op_out = OPIO({
            "output" : op_in["input"],
        })
        return op_out

class DP(OP):
    """
    class for calculation
    """
    def __init__(self,infomode=1):
        self.infomode = infomode
    
    @classmethod
    def get_input_sign(cls):
        return OPIOSign({
            'input_dp': Artifact(Path),
        })
    
    @classmethod
    def get_output_sign(cls):
        return OPIOSign({
            'output_dp': Artifact(Path)                                                                                                                                         
        })
    
    @OP.exec_sign_check
    def execute(self, op_in: OPIO) -> OPIO:
        cwd = os.getcwd()
        os.chdir(op_in["input_dp"])
        parameter = loadfn("param.json")["properties"]
        supercell_matrix = parameter['supercell_matrix']

        os.chdir(os.path.join(op_in["input_dp"],"task.000000"))
        cmd = "phonolammps in.lammps -c POSCAR --dim %s %s %s "%(supercell_matrix[0],supercell_matrix[1],supercell_matrix[2])
        subprocess.call(cmd, shell=True)
        os.chdir(cwd)
        op_out = OPIO({
            "output_dp": op_in["input_dp"]
        })
        return op_out

class PhononPostDP(OP):
    """
    class for analyse calculation results
    """
    def __init__(self):
        pass
    
    @classmethod
    def get_input_sign(cls):
        return OPIOSign({
            'input_post_dp': Artifact(Path)
        })
    
    @classmethod
    def get_output_sign(cls):
        return OPIOSign({
            'output_post_dp': Artifact(Path)                                                                                                                                          
        })
    
    @OP.exec_sign_check
    def execute(self, op_in: OPIO) -> OPIO:
        os.chdir(op_in["input_post_dp"])
        os.chdir("task.000000")

        parameter = loadfn("../param.json")["properties"]
        supercell_matrix = parameter['supercell_matrix']
        
        if os.path.isfile('FORCE_CONSTANTS'):
            os.system('phonopy --dim="%s %s %s" -c POSCAR band.conf'%(supercell_matrix[0],supercell_matrix[1],supercell_matrix[2]))
            os.system('phonopy-bandplot --gnuplot band.yaml > band.dat')
            shutil.copyfile("band.dat","../band.dat")
        else:
            print('FORCE_CONSTANTS No such file')

        op_out = OPIO({
            "output_post_dp": op_in["input_post_dp"]
        })
        return op_out
