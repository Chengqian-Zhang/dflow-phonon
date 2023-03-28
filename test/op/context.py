import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import dflowphonon

def write_poscar():
    ret_POSCAR='''generated by phonopy
   1.0
     4.0435066112408995    0.0000000000000000    0.0000000000000000
     0.0000000000000000    4.0435066112408995    0.0000000000000000
     0.0000000000000000    0.0000000000000000    4.0435066112408995
Al
   4
Direct
  0.0000000000000000  0.0000000000000000  0.0000000000000000
  0.0000000000000000  0.5000000000000000  0.5000000000000000
  0.5000000000000000  0.0000000000000000  0.5000000000000000
  0.5000000000000000  0.5000000000000000  0.0000000000000000
    '''
    with open("POSCAR","a") as f:
        f.write(ret_POSCAR)

def write_param(type):
    if(type == "dfpt"):
        ret='''{
    "interaction": {
        "type":          "vasp"
    },
    "properties": {
         "type":         "phonon",
         "band_path": "0.5000 0.5000 0.5000  0.0000 0.0000 0.0000  0.5000 0.0000 0.5000  0.5000 0.2500 0.7500",
         "supercell_matrix":[2,2,2],
         "PRIMITIVE_AXES": "0 1/2 1/2  1/2 0 1/2  1/2 1/2 0"
    }
}
        '''
    elif(type == "displacement"):
        ret='''{
    "interaction": {
        "type":          "vasp"
    },
    "properties": {
         "type":         "phonon",
         "band_path": "0.5000 0.5000 0.5000  0.0000 0.0000 0.0000  0.5000 0.0000 0.5000  0.5000 0.2500 0.7500",
         "supercell_matrix":[2,2,2],
         "approach":"displacement",
         "PRIMITIVE_AXES": "0 1/2 1/2  1/2 0 1/2  1/2 1/2 0"
    }
}
        '''
    elif(type == 'dp'):
        ret='''{
    "interaction": {
        "type": "dp",
        "model":         "frozen_model.pb",
        "type_map":     {"Mg":0,"Al": 1,"Cu":2}
    },
    "properties": {
         "type":         "phonon",
         "band_path": "0.5000 0.5000 0.5000  0.0000 0.0000 0.0000  0.5000 0.0000 0.5000  0.5000 0.2500 0.7500",
         "supercell_matrix":[2,2,2],
         "PRIMITIVE_AXES": "0 1/2 1/2  1/2 0 1/2  1/2 1/2 0"
    }
}
        '''
    with open("param.json","a") as f:
        f.write(ret)

def get_num_elements(conf_file):
    with open(conf_file) as f:
        lines = f.readlines()
        for line in lines:
            if "atom types" in line:
                return int(line.split()[0])