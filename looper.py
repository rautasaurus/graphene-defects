import os.path, glob
from tqdm import tqdm
from vac import Vac

current_dir = os.path.dirname(os.path.abspath(__file__))
define_depth = glob.glob(current_dir + '/*/*')
dirs = list(filter(lambda f: os.path.isdir(f), define_depth))

perc_dropout = int(input("Enter percentage atoms to drop: "))

for dir in tqdm(dirs):
    vac_obj = Vac(dir, perc_dropout)
    vac_obj.vac()