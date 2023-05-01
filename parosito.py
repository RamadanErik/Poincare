import pandas as pd


#Módosítandók:

mappa = 'B:/egyetem/6_hatodik_félév/Önlab/meresek_eredmenye/'

file1 = 'masodik.csv'
file2 = 'EventLog -20230425-031523_2.Log'

file_ki = 'B:/egyetem/6_hatodik_félév/Önlab/meresek_eredmenye/masodik_plate.xlsx'


####################
file1 = mappa+file1
file2 = mappa+file2


df = pd.read_csv(file1,sep=";")
print(df.head())

f = open(file2,'r')
log = f.read()
log = log.replace("\n \t","\t")
tomb=log.split('\n')
for i in range(len(tomb)):
    tomb[i]=tomb[i].split('\t')



df2 = pd.DataFrame(tomb,columns=['Ido','Info','szam','Muvelet','Pozício','Vmi','Vmi2','Vmi3','Vmi4'])
df2_szurt = df2.loc[df2['Muvelet'] == "MoveToPosition Requested "]

lst_rot=[]
for index, row in df2_szurt.iterrows():
    t = row['Ido']
    poz = row['Pozício']
    ido = t.split(" ")
    idopont = ido[1].split(":")
    idopont_szam = int(idopont[0]) * 3600 + int(idopont[1]) * 60 + float(idopont[2])
    poz2=poz.split(" = ")
    poz2_szam=poz2[1]
    lst1 = [idopont_szam,int(poz2_szam),round(int(poz2_szam)*170/1370,2)]
    lst_rot.append(lst1)



lst_mert=[]

for index, row in df.iterrows():
    t = row['Time[date hh:mm:ss] ']
    s0 = row[' S 0 [mW]']
    s1 = row[' S 0 [mW]']
    s2 = row[' S 0 [mW]']
    s3 = row[' S 0 [mW]']
    ido = t.split(" ")
    idopont = ido[1].split(":")
    idopont_szam = int(idopont[0])*3600+int(idopont[1])*60+float(idopont[2])
    #print(idopont_szam)
    lst1 = [idopont_szam,float(s0),float(s1),float(s2),float(s3)]
    lst_mert.append(lst1)

print(lst_rot)
print(lst_mert)


for i in range(len(lst_rot)):
    for j in range(len(lst_mert)):
        if lst_mert[j][0]>lst_rot[i][0] and j!=0:
            lst_rot[i].extend([lst_mert[j-1][1],lst_mert[j-1][2],lst_mert[j-1][3],lst_mert[j-1][4]])
            break




dfki = pd.DataFrame(lst_rot, columns=['Időpont','Pozíció','Fok','S0','S1','S2','S3'])


writer = pd.ExcelWriter(file_ki)
dfki.to_excel(writer, sheet_name='Adatok')
writer.close()