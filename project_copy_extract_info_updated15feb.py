# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 15:06:54 2022

@author: amrma
"""

import os
import pathlib
import shutil
import re


directory=r"C:\Users\amrma\OneDrive\Desktop\pdf"
dsrpath=r"C:\Users\amrma\OneDrive\Desktop\distination"


# directory = "c:\\folder\\you\\want\\to\\work_on"

for root, subdirectories, files in os.walk(directory):
    # for subdirectory in subdirectories:
        # print(os.path.join(root, subdirectory))
    for file in files:
        f=os.path.join(root, file)
        print(f)
        if re.search('COL.+(pdf)$', f):
            shutil.copy(f, dsrpath)
            # print('file{}copied'.format(f))
        
        
        
        

# import pathlib
# open pdf and put spud date into dataframe
# import PyPDF2
# pathpdf='C:/Users/amrma/OneDrive/Desktop/pdf/BARAKAT DEEP-3X ML COL-T.D (06-08-2021).pdf'

for path in pathlib.Path(dsrpath).iterdir():
    if path.name[-3:] =='pdf':
        pdfFileObject = open(path, 'rb')
        pdfReaderObject = PyPDF2.PdfFileReader(pdfFileObject)
        # print(pdfReaderObject.read())
        s=''
        i=0
        while i<pdfReaderObject.getNumPages():
            pageinfo= pdfReaderObject.getPage(i)
            all=pageinfo.extractText()
            s=s+all
            i = i + 1
        
        # print(s)
        # text_file = open(r'C:\Users\amrma\OneDrive\Desktop\pdf\my_text_file.txt','w')
        text_file = open(f'{pdfFileObject.name[:-3]}txt','w')
        n = text_file.write(s)
        
        text_file.close()
        pdfFileObject.close()

import pandas as pd
import numpy as np

df=pd.DataFrame(columns =  ["location", "rig_spud_date", "rkb_msl","rkb_gl", "td_driller",
                            "td_logger","_13_375inchCSG","_9_625inchCSG",
                            "_7inchCSG", "logging1", "logging2", "last_fm"])  

for path in pathlib.Path(dsrpath).iterdir():
    if path.name[-3:] =='txt':
        txtFileObject = open(path)
        txtReaderObject = txtFileObject.read()
        
        # indexspud= txtReaderObject.index('RIG SPUD DATE')
        # rig_spud_date=txtReaderObject[indexspud+14:indexspud+25].strip()


        pattern=r'RIG SPUD DATE'
        if re.search(pattern, txtReaderObject):
            first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            rig_spud_date=txtReaderObject[first+14:last+12].strip()
            
            
        pattern=r'RKB.+M'
        if re.search(pattern, txtReaderObject):
            first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            rkb_msl=txtReaderObject[first+9:last+7].strip()

        pattern=r'RKB.+G'
        if re.search(pattern, txtReaderObject):
            first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            rkb_gl=txtReaderObject[first+9:last+6].strip()
            
        pattern=r'TD DRILLER'
        if re.search(pattern, txtReaderObject):
            first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            td_driller=txtReaderObject[first+11:last+7].strip()
        
        pattern=r'TD LOGGER'
        if re.search(pattern, txtReaderObject):
            first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            td_logger=txtReaderObject[first+10:last+6].strip()
        else:
            td_logger=np.nan

        pattern=r'SET 13 3/8.+CSG.?@(\s+)?\d+'
        if re.search(pattern, txtReaderObject):
            # print((re.search(pattern, txtReaderObject).group()))
            # first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            _13_375inchCSG=txtReaderObject[last-5:last].strip()
        else:
            _13_375inchCSG=np.nan
            
            
        pattern=r'SET 9 5/8.+CSG.?@(\s+)?\d+'
        if re.search(pattern, txtReaderObject):
            # print((re.search(pattern, txtReaderObject).group()))
            # first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            _9_625inchCSG=txtReaderObject[last-5:last].strip()
        else:
            _9_625inchCSG=np.nan
            
        # pattern=r'SET 7.+CSG'
        pattern=r'SET 7.+CSG.?@(\s+)?\d+'
        if re.search(pattern, txtReaderObject):
            # print((re.search(pattern, txtReaderObject).group()))
            # first=(re.search(pattern, txtReaderObject)).start()
            last=(re.search(pattern, txtReaderObject)).end()
            _7inchCSG=txtReaderObject[last-5:last].strip()
        else:
            _7inchCSG=np.nan
            

        
        # pattern=r'RUN#1'
        # if re.search(pattern, txtReaderObject):
        #     line=(re.search(pattern, txtReaderObject).group())
            
        #     print(line)
            
        #     lineindex=txtReaderObject.index(line)

        #     logging1=txtReaderObject[lineindex+5:lineindex+100]
        #     # first=logging.find(':')
        #     # last=logging.find(')')
        #     # firstrun=logging1[first+1:last]
        #     # print()
        #     # first=line.index('(')
        #     # last=line.index(')')
        #     # run_1=line[first:last].strip()
        # else:
        #     logging=np.nan
        #     # firstrun=np.nan
            
        
        #not tested yet
        pattern=r'RUN#1'
        if re.findall(pattern, txtReaderObject):
            line=re.findall(pattern, txtReaderObject)
            lineindex=txtReaderObject.index(line[0])
            logging1=txtReaderObject[lineindex+5:lineindex+100]

            if len(line) > 1:
                # lineindex=txtReaderObject.index(line[-1])
                lineindex=txtReaderObject.find(line, lineindex+5)  #starting from lineindex+1
                logging2=txtReaderObject[lineindex+5:lineindex+100]
            
            else:
                logging2=np.nan

        else:
            logging=np.nan
            # firstrun=np.nan        
              
        pattern=r"POSS TOP.+\s+?@"   
        if re.findall(pattern, txtReaderObject):    
            line=re.findall(pattern, txtReaderObject)
            lastline=line[-1]
            last_fm=lastline[8:-1].strip()

  
        lst=list((txtFileObject.name, rig_spud_date, rkb_msl, rkb_gl, td_driller, td_logger,
                  _13_375inchCSG, _9_625inchCSG, _7inchCSG, logging1, logging2, last_fm))
        df.loc[-1]=lst
        df.index=df.index +1
        df=df.sort_index()
        txtFileObject.close()
        

        # print(pdfReaderObject.read())


# path="C:/Users/amrma/OneDrive/Desktop/pdf/BARAKAT DEEP-3X ML COL-T.D (06-08-2021).txt"
# file = open(path)
# text=file.read()

# line=file.read()
# print(line)
# for each in file:
#     each =each.strip()
#     if re.search('Company', each):
#         print(each)

# indexspud= text.index('RIG SPUD DATE')
# indexWell= text.index('Well')

# rig_spud_date=text[indexspud+14:indexspud+25].strip()

# # pattern_well=r"Well "
# well_name=re.findall(pattern, text)

# # pattern=r"[0-9]{2}/[0-9]{2}/[0-9]{4}"
# # print(re.search(pattern, text))
# # date=re.findall(pattern, text)
# print(well_name)


# lst=list((file.name, rig_spud_date))
# # # print(lst)

# # df=pd.DataFrame(columns =  ["location", "rig_spud_date"])   
# df.loc[-1]=lst
# df.index=df.index +1
# df=df.sort_index()

# display(df)

# df
# # df.ind
