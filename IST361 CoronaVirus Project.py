import urllib.request
import tkinter as tk                    
from tkinter import ttk
from tkinter import *
import pandas as pd

win = tk.Tk()                       
win.title("Coronavirus Analytics") 
tabControl = ttk.Notebook(win)
downloadDirectory='/Users/r_ema/Downloads/' #This needs to be changed to the individual's download directory

def search(event):
    county=countyName.get()
    st=state.get()
    if len(st)>2: #or st.isalpha() is False or county.isalpha() is False:
        text1.set("**Error: Invalid Entry")
        text2.set("**Error: Invalid Entry")
        text3.set("**Error: Invalid Entry")
        text4.set("**Error: Invalid Entry")
    elif county.strip() == '' and st.strip() == '':
        text1.set("USA")
        text2.set("USA Coronavirus Graph")
        text3.set("USA Coronavirus Statistics")
        text4.set("USA Coronavirus Projections")
    
    elif county.strip() == '':
        text1.set(st)
        text2.set(st+ " Coronavirus Graph")
        text3.set(st+ " Coronavirus Statistics")
        text4.set(st+ " Coronavirus Projections")
    
    else:
        text1.set(county+", "+ st)
        text2.set(county+ ", "+ st+ " Coronavirus Graph")
        text3.set(county+ ", "+ st+ " Coronavirus Statistics")
        text4.set(county+ ", "+ st+ " Coronavirus Projections")
    
def populateGraphTab():
    print()

def populateStatisticsTab():
    print()

def populateProjectionsTab():
    print()
    
url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
urllib.request.urlretrieve(url, downloadDirectory+ 'covid_confirmed_usafacts.csv')
url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv"
urllib.request.urlretrieve(url, downloadDirectory+ 'covid_deaths_usafacts.csv')
url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv"
urllib.request.urlretrieve(url, downloadDirectory+ 'covid_county_population_usafacts.csv')


tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

#Tab 1
tabControl.add(tab1, text='Search')

countyName = StringVar()
state = StringVar()
text1=StringVar()
Label(tab1, textvariable=text1).grid(row=3, column=1)
countyEntry = tk.Entry(tab1, textvariable=countyName).grid(row=0, column=1)
stateEntry = tk.Entry(tab1, textvariable=state).grid(row=1, column=1)
Label(tab1, text="County Name").grid(row=0)
Label(tab1, text="State").grid(row=1)
Label(tab1, text="*Must Be In 2 Letter Format (Ex. PA)*").grid(row=1, column=2)
Label(tab1, text="*County Name Can Be Left Blank For Statewide Statistics*").grid(row=0, column=2)
Label(tab1, text="*Both Fields Can Be Left Blank For Nationwide Statistics*").grid(row=2, column=2)
Label(tab1, text="Results For:").grid(row=3, column=0)
searchbutton = tk.Button(tab1, text='Search')
searchbutton.bind('<Button-1>', search)
searchbutton.grid(row=2, column=1)

#Tab 2
tabControl.add(tab2, text='Graph')

text2=StringVar()
Label(tab2, textvariable=text2).grid(row=0)

#Tab 3
tabControl.add(tab3, text='Statistics')

text3=StringVar()
Label(tab3, textvariable=text3).grid(row=0)

#Tab 4
tabControl.add(tab4, text='Projections')

text4=StringVar()
Label(tab4, textvariable=text4).grid(row=0)

tabControl.pack(expand=1, fill="both")  
win.geometry("1000x600")
win.mainloop()             
