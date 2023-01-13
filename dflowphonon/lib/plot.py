import matplotlib.pyplot as plt

x_axis = []
y_axis = []

def plot_band_structure():
    with open("band.dat","r") as f:
        lines = f.readlines()
    kpath = list(map(float,lines[1].split()[1:]))
    band_points = [list(map(float,line.split())) for line in lines[2:]]
    for single_point in band_points:
        try:
            x_axis.append(single_point[0])
            y_axis.append(single_point[1])
        except:
            pass
    plt.scatter(x_axis,y_axis)
    plt.xticks([kpoint for kpoint in kpath])
    plt.title("Phonon Band Structure")
    plt.xlabel("Wave vector")
    plt.ylabel("Frequency(THz)")
    plt.savefig("phonon_band_structure.png")
    plt.show()
