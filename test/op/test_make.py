import dpdata,os
from context import dflowphonon,write_param,write_poscar,get_num_elements
import unittest, json, shutil
from mock import mock,patch,call
from dflow.python import (
    OP,
    OPIO,
    OPIOSign,
    Artifact,
    TransientError,
)
from pathlib import Path
from dflowphonon.VASP_OPs import PhononMakeVASP
from dflowphonon.DP_OPs import PhononMakeDP

class TestPhononMakeVASPdfpt(unittest.TestCase):
    def setUp(self):
        cwd = os.getcwd()
        self.path = cwd
        self.dfpt_dir = Path('vasp_dfpt')
        os.makedirs(self.dfpt_dir)
        os.chdir(self.dfpt_dir)
        write_param("dfpt")
        write_poscar()
        os.chdir(cwd)
    
    def tearDown(self):
        shutil.rmtree("vasp_dfpt")

    def test_success(self):
        op = PhononMakeVASP()
        out = op.execute(
            OPIO({
                'input' : self.dfpt_dir
            }))
        self.assertTrue(Path('vasp_dfpt').is_dir())
        self.assertTrue(os.path.exists(os.path.join(self.dfpt_dir,"POSCAR-001")))
        self.assertTrue(os.path.exists(os.path.join(self.dfpt_dir,"task.000000","band.conf")))
        self.assertEqual(out['njobs'],1)
        self.assertEqual(out['jobs'],[Path(os.path.join(self.path,self.dfpt_dir,"task.000000"))])

class TestPhononMakeVASPdisplacement(unittest.TestCase):
    def setUp(self):
        cwd = os.getcwd()
        self.path = cwd
        self.dis_dir = Path('vasp_displacement')
        os.makedirs(self.dis_dir)
        os.chdir(self.dis_dir)
        write_param("displacement")
        write_poscar()
        os.chdir(cwd)
    
    def tearDown(self):
        shutil.rmtree("vasp_displacement")

    def test_success(self):
        op = PhononMakeVASP()
        out = op.execute(
            OPIO({
                'input' : self.dis_dir
            }))
        self.assertTrue(Path('vasp_displacement').is_dir())
        self.assertTrue(os.path.exists(os.path.join(self.dis_dir,"POSCAR-001")))
        self.assertTrue(os.path.exists(os.path.join(self.dis_dir,"task.000000","band.conf")))
        self.assertEqual(out['njobs'],1)
        self.assertEqual(out['jobs'],[Path(os.path.join(self.path,self.dis_dir,"task.000000"))])

class TestPhononMakeDP(unittest.TestCase):
    def setUp(self):
        cwd = os.getcwd()
        self.path = cwd
        self.dp_dir = Path('dp')
        os.makedirs(self.dp_dir)
        os.chdir(self.dp_dir)
        write_param("dp")
        write_poscar()
        os.chdir(cwd)

    def tearDown(self):
        shutil.rmtree("dp")
   
    def test_success(self):
        op = PhononMakeDP()
        out = op.execute(
            OPIO({
                'input' : self.dp_dir
            }))
        self.assertTrue(Path('dp').is_dir())
        self.assertTrue(os.path.exists(os.path.join(self.dp_dir,"task.000000","band.conf")))
        self.assertTrue(os.path.exists(os.path.join(self.dp_dir,"task.000000","conf.lmp")))
        self.assertTrue(os.path.exists(os.path.join(self.dp_dir,"task.000000","in.lammps")))
        num_elements = get_num_elements(os.path.join(self.dp_dir,"task.000000","conf.lmp"))
        self.assertEqual(num_elements,3)