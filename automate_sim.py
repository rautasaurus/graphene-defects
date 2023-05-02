from ansys.mapdl.core import launch_mapdl
import os.path, glob, csv
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
define_depth = glob.glob(current_dir + '/*/*')
dirs = list(filter(lambda f: os.path.isdir(f), define_depth))

nat_freqs = dict()
for i in range(3):
    for dir in tqdm(dirs[i*8:(i+1)*8]):
        slash_idx = dir[:-13].rfind('\\')
        mapdl = launch_mapdl()
        mapdl.prep7()
        mapdl.et(1, "BEAM188")
        mapdl.mp("EX", 1, 548.75)  #  Elastic modulus
        mapdl.mp("PRXY", 1, 0.3)  #  Poisson's ratio
        mapdl.mp("DENS", 1, 2.267e-27)  #  Density

        mapdl.sectype(1, "BEAM", "CSOLID")
        mapdl.secoffset("CENT")
        beam_info = mapdl.secdata(0.7331)

        atom_data = nodes_data = elements_data = ""
        with open(dir+'/atom_vac.txt') as fp:
            atom_data = fp.read()
        with open(dir+'/nodes_vac.txt') as fp:
            nodes_data = fp.read()
        with open(dir+'/elements_vac.txt') as fp:
            elements_data = fp.read()
        mapdl.input_strings(atom_data)
        mapdl.input_strings(nodes_data)
        mapdl.input_strings(elements_data)

        mapdl.lesize("ALL", ndiv='7')
        mapdl.dofsel('S', 'UX', 'UY', 'UZ', 'ROTX', 'ROTY', 'ROTZ')
        mapdl.nsel('S', 'LOC', 'Y', -1, 1.4)
        mapdl.d(node='ALL', lab='ALL', value='0')

        mapdl.finish()

        mapdl.run("/SOLU")
        try:
            mapdl.modal_analysis(method="LANB", nmode='12', freqb='0', freqe='0', mxpand='12')
            mapdl.post1()
            mapdl.set(1, 1)
            nat_freqs[dir[slash_idx+1:]] = mapdl.post_processing.freq
        except:
            nat_freqs[dir[slash_idx+1:]] = "Error"
        mapdl.exit()

    with open('nat_freqs.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in nat_freqs.items():
            writer.writerow([key, value])
    print(nat_freqs)
