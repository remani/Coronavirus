import urllib.request
import tkinter as tk                    
from tkinter import ttk
from tkinter import *
import pandas as pd

win = tk.Tk()                       
win.title("Coronavirus Analytics") 
tabControl = ttk.Notebook(win)
directory='/Users/r_ema/Downloads/' #This needs to be changed to the individual's download directory

def search(event):
    county=countyName.get()
    st=state.get()
    
def populateGraphTab():
    print()

def populateStatisticsTab():
    print()

def populateProjectionsTab():
    print()
    
url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
urllib.request.urlretrieve(url, directory+ 'covid_confirmed_usafacts.csv')
url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv"
urllib.request.urlretrieve(url, directory+ 'covid_deaths_usafacts.csv')
url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv"
urllib.request.urlretrieve(url, directory+ 'covid_county_population_usafacts.csv')


tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Search')

countyName = StringVar()
state = StringVar()
countyEntry = tk.Entry(tab1, textvariable=countyName).grid(row=0, column=1)
stateEntry = tk.Entry(tab1, textvariable=state).grid(row=1, column=1)
Label(tab1, text="County Name").grid(row=0)
Label(tab1, text="State").grid(row=1)
Label(tab1, text="*Must Be In 2 Letter Format (Ex. PA)*").grid(row=1, column=2)
Label(tab1, text="*Can Be Left Blank For Statewide Statistics*").grid(row=0, column=2)
Label(tab1, text="*Both Fields Can Be Left Blank For Nationwide Statistics*").grid(row=2, column=2)
searchbutton = tk.Button(tab1, text='Search')
searchbutton.bind('<Button-1>', search)
searchbutton.grid(row=2, column=1)

tabControl.add(tab2, text='Graph')
tabControl.add(tab3, text='Statistics')
tabControl.add(tab4, text='Projections')
tabControl.pack(expand=1, fill="both")  
win.geometry("1000x600")
win.mainloop()                          