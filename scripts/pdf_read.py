import tabula
import glob
import sys
import pandas as pd

pdf_files=glob.glob(sys.argv[1]+"*.pdf")
print (pdf_files)
#from tabula import read_df
for f in pdf_files:
  
  df=tabula.read_pdf(f, lattice=True)
  df=df.iloc[1:]
  df=df.drop(df.columns[2],axis=1)
  df=df.drop(df.columns[3],axis=1)
  df=df.drop(df.columns[4],axis=1)
  df=df.drop(df.columns[-1],axis=1)
  df.columns=['Antibiotic','R','I','S']
  df.to_csv(f+".csv",index=False,sep='\t')
