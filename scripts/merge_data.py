import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import re
Data_path = "data/ARS/Inpatient"

def merge_ARS_data(Data_path):
    file_list = os.listdir(Data_path)
    #file_list.sort()
    df_final = pd.DataFrame({'Antibiotic': [], 'R': [],'I' : [],'S' : [],'Species' : [],'Year' : []})
    for file in file_list:
        df = pd.read_csv(os.path.join(Data_path, file), sep = "\t")
        year = re.findall(r'\d+',file)[0]
        species = file[:file.index("_"+year)]
        df["Species"] = species
        df["Year"] = year
        df_final = df_final.append(df)

    return (df_final)

def timeline_plots(df,species,antib):
    Spec = df[df["Species"] == species]
    Res = Spec[Spec["Antibiotic"]== antib].sort_values(by=["Year"])
    plt.plot(Res["Year"],Res["R"]/Res["S"])



if __name__ == '__main__':

    df = merge_ARS_data(Data_path)
    timeline_plots(df, "Enterobacter_cloacae","Ciprofloxacin")
