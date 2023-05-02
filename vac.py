import pandas as pd
import math
import random

class Vac:
    def __init__(self, folder_name, perc_dropout):
        self.folder_name = folder_name
        self.perc_dropout = perc_dropout

    def vac(self):
        df=pd.read_csv(self.folder_name + '/atom.txt', skiprows=1, header=None)

        grouped = df.groupby(df.columns[0])
        dfk = grouped.get_group("K")
        dfl = grouped.get_group("L")
        idx_increment = dfk.shape[0]

        dfl = dfl.drop(dfl.columns[[3, 4]], axis=1)

        rand_idx = random.sample(range(dfk.shape[0]), math.ceil((self.perc_dropout/100)*dfk.shape[0]))
        dropped_data = dfk.iloc[rand_idx][1].tolist()
        dfk = dfk.drop(rand_idx, axis=0)

        dropidx = [idx + idx_increment for idx in range(dfl.shape[0]) if dfl.iloc[idx][1] in dropped_data or dfl.iloc[idx][2] in dropped_data]

        dfl = dfl.drop(dropidx, axis=0)
        dfl[2] = dfl[2].astype(int)

        dfl.to_csv(self.folder_name + '/elements_vac.txt', index=False, header=False)
        dfk.to_csv(self.folder_name + '/nodes_vac.txt', index=False, header=False)

        header = "/PREP7\n"
        dfk_data = ""
        dfl_data = ""
        with open(self.folder_name + '/nodes_vac.txt') as fp:
            dfk_data = fp.read()
        with open(self.folder_name + '/elements_vac.txt') as fp:
            dfl_data = fp.read()
        header += dfk_data + dfl_data
        with open(self.folder_name + '/atom_vac.txt', 'w') as fp:
            fp.write(header)

        dfl.replace(to_replace="L", value="e", inplace=True)
        dfk.replace(to_replace="K", value="N", inplace=True)
        dfl.to_csv(self.folder_name + '/elements_vac.txt', index=False, header=False)
        dfk.to_csv(self.folder_name + '/nodes_vac.txt', index=False, header=False)

        header = "/PREP7\n"
        dfk_data = ""
        with open(self.folder_name + '/nodes_vac.txt') as fp:
            dfk_data = fp.read()
        header += dfk_data
        with open(self.folder_name + '/nodes_vac.txt', 'w') as fp:
            fp.write(header)

        header = "/PREP7\n"
        dfl_data = ""
        with open(self.folder_name + '/elements_vac.txt') as fp:
            dfl_data = fp.read()
        header += dfl_data
        with open(self.folder_name + '/elements_vac.txt', 'w') as fp:
            fp.write(header)