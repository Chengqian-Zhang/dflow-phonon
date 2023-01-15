import seekpath,os,dpdata

def band_path_from_POSCAR():
    os.system("phonopy --symmetry")
    with open("PPOSCAR","r") as f:
        lines = f.readlines()
    cell = [[float(lines[j].split()[i]) for i in range(0,3)] for j in range(2,5)]
    positions = [[float(lines[j].split()[i]) for i in range(0,3)] for j in range(lines.index("Direct\n")+1,len(lines))]
    numbers = list(range(1,len(positions)+1))
    structure = (cell,positions,numbers)
    kpath_info = seekpath.get_path(structure)
    kpath = kpath_info["point_coords"]
    for i,j in kpath.items():
        print(i,j)

def band_path_from_STRU():
    dpdata.System("STRU",fmt="abacus/stru").to(file_name="POSCAR",fmt="vasp/poscar")
    band_path_from_POSCAR()

def create_band_path():
    if os.path.isfile("POSCAR"):
        band_path_from_POSCAR()
    elif os.path.isfile("STRU"):
        band_path_from_STRU()
