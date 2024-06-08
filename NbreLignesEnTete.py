import pandas as pd
#import csv
path_data = 'C:/Users/b.lefebvre/Documents/Work/Python/RecupDataOscillo/Donnees/'
file= path_data + 'Tek000_ALL.csv'
#df= pd.read_csv(file,header=None)

#total_rows=len(df.axes[0])
#total_cols=len(df.axes[1])
#print("Number of Rows: "+str(total_rows))
#print("Number of Columns: "+str(total_cols))

#print(len(df))


with open(file,'r') as read_obj:
    cpt= 1
    line= read_obj.readline()
    print(line)
    while not line.startswith('TIME'):
        line= read_obj.readline()
        cpt += 1
        print(line)
    print('Nombre de ligne d\'en-tête :', cpt)

#header = prev_line.strip().lstrip('TIME ').split()

#df = pd.read_csv(file, delimiter="\s+", names=header,skiprows=cpt)