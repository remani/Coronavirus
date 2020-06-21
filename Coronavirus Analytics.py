import urllib.request
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
import datetime
from datetime import date, timedelta
import pandas as pd
import matplotlib as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import SimpleSEIR

# Possible additions: autofill the word "county"

win = tk.Tk()
win.title("Coronavirus Analytics")
tabControl = ttk.Notebook(win)
# This needs to be changed to the individual's download directory
#downloadDirectory = '/Users/kevincushing/Downloads/'
#downloadDirectory = '/Users/kevincushing/desktop/codingprojects/coronavirus/'
# os.chdir(downloadDirectory)

today = date.today()
yesterday = today - datetime.timedelta(days=1)
daybefore = today - datetime.timedelta(days=2)
daybeforedate = daybefore.strftime("%m/%d/%y").replace('/0', '/')
yesterdaydate = yesterday.strftime("%m/%d/%y").replace('/0', '/')
if yesterdaydate.startswith("0"):
    yesterdaydate = yesterdaydate[1:]
if daybeforedate.startswith("0"):
    daybeforedate = daybeforedate[1:]


def populateGraphTab(value, dates, f, pop):
    # Clear previously displayed figures
    for w in tab2.winfo_children():
        w.destroy()
    for w in tab4.winfo_children():
        w.destroy()
    for w in tab5.winfo_children():
        w.destroy()
    data = np.array([])
    days = np.array([])
    day0 = datetime.date(year=2020, month=1, day=22)

    # populate arrays of days and data
    count = 0
    for i in dates:
        # ignores the first 4 columns from the csv files as they do not contain
        # data
        if count >= 4:
            data = np.append(data, f(i))
            days = np.append(days, (count - 4))
        count = count + 1

    dates = [day0 + timedelta(days=i) for i in days]
    f = Figure(figsize=(8, 6), dpi=100)
    p = f.add_subplot(111, yscale="linear",
                      yticks=np.linspace(0, np.amax(data), 10))
    p.plot(dates, data)
    p.set_xlabel("Time (Months)")
    p.set_ylabel("Cases")
    p.set_title(value + " COVID-19 Confirmed Cases Graph")

    c = FigureCanvasTkAgg(f, master=tab2)
    c.draw()
    c.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # assume that this amount of actual cases were recorded
    # a study at the University of Montreal estimated a nationwide average of 12
    # cases per confirmed case
    percentOfCasesRecorded = 1/12
    # outputs an estimated number of active cases (assuming recovery time is
    # approximately 30 days - comes from analysis of reported cases vs reported
    # recoveries)
    percentConfirmedPositiveSick = 0.6
    recoveryTimeSick = 32
    recoveryTimeHealthy = 14
    currentCases = np.array([])
    for i in range(data.size):
        if i >= recoveryTimeSick:
            currentCases = np.append(currentCases,
                                     (data[i] / percentOfCasesRecorded)
                                     - ((((1 / percentOfCasesRecorded) - 1)
                                         + (1 - percentConfirmedPositiveSick))
                                         * data[i - recoveryTimeHealthy])
                                     - (percentConfirmedPositiveSick
                                        * data[i - recoveryTimeSick]))
        elif i >= recoveryTimeHealthy:
            currentCases = np.append(currentCases,
                                     (data[i] / percentOfCasesRecorded)
                                     - ((((1 / percentOfCasesRecorded) - 1)
                                         + (1 - percentConfirmedPositiveSick))
                                         * data[i - recoveryTimeHealthy]))
        else:
            currentCases = np.append(currentCases, data[i])
    # draws current cases graph on tab4
    f2 = Figure(figsize=(8, 6),  dpi=100)
    a2 = f2.add_subplot(111, yscale="linear", yticks=np.linspace(
        0, np.amax(currentCases), 10))
    a2.plot(dates, currentCases)
    a2.set_xlabel("Time (Months)")
    a2.set_ylabel("Estimated Current Cases")
    a2.set_title(value + " COVID-19 Estimated Active Cases")
    c2 = FigureCanvasTkAgg(f2, master=tab4)
    c2.draw()
    c2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # b(t) is the chance of contracting the disease multiplied by the number of
    # people an average individual comes in close contact with
    # This model uses a piecewise function to model societal reopening phase

    def b(t):
        # a study in China found that between 1-5% of people in close contact
        # with carriers of the disease cantracted it - assume 1% since people
        # will be encouraged to wear masks to reduce the spread
        transmissionRate = 0.01
        # assuming people are generally only in close contact with immediate
        # family and 2 close friends - average family size in the US is 3.14 according to
        # statista.com
        dailyCloseContactClosed = 4.14
        # assuming people are generally only in close contact with immediate
        # family and a few close friends (for the sake of simplicity let's say
        # 10)
        dailyCloseContactOpen = 12.14
        tOpen = 0
        if t >= tOpen:
            return dailyCloseContactOpen * transmissionRate
        else:
            return dailyCloseContactClosed * transmissionRate

    i0 = currentCases[currentCases.size - 1]
    r0 = data[data.size - 1] / percentOfCasesRecorded - \
        currentCases[currentCases.size - 1]
    # calculated based on annual birth and death rates
    mu = 0.016 / 365
    nu = 0.0086 / 365
    # based on data from the cdc
    latentTime = 5
    infTime = 12
    e0 = 0
    for i in range(latentTime):
        e0 = e0 + currentCases[currentCases.size -
                               1 - i] * b(-i) * (pop - i0 - r0) / pop
    s0 = pop - e0 - i0 - r0

    m = SimpleSEIR.SEIRModel(s0, e0, i0, r0, mu, nu,
                             latentTime, infTime, b)
    projDays = 500
    (projS, projE, projI, projR) = m.projectSEIR(projDays)

    def updatedM():
        def bTransform(t):
            return b(t - openScale.get())
        return SimpleSEIR.SEIRModel(
            s0, e0, i0, r0, mu, nu, latentTime, infTime, bTransform)

    def updateOpenTime(str):
        projDays = projScale.get()
        m = updatedM()
        (projS, projE, projI, projR) = m.projectSEIR(projDays)
        projectedCases = np.append(currentCases, projI[1:])
        a3.cla()
        dates = [day0 + timedelta(days=i) for i in range(projDays + days.size)]
        a3.plot(dates, projectedCases)
        a3.set_xlabel("Time (Months)")
        a3.set_ylabel("Projected Cases")
        a3.set_title(value + " COVID-19 Projected Cases")
        c3.draw()

    def updateProjDays(str):
        projDays = projScale.get()
        m = updatedM()
        (projS, projE, projI, projR) = m.projectSEIR(projDays)
        projectedCases = np.append(currentCases, projI[1:])
        a3.cla()
        dates = [day0 + timedelta(days=i) for i in range(projDays + days.size)]
        a3.plot(dates, projectedCases)
        a3.set_xlabel("Time (Months)")
        a3.set_ylabel("Projected Cases")
        a3.set_title(value + " COVID-19 Projected Cases")
        c3.draw()

    lF = tk.LabelFrame(master=tab5, bd=0)
    openScale = Scale(master=lF, to=200, orient=tk.HORIZONTAL,
                      label="Days until reopening", length=150,
                      command=updateOpenTime, tickinterval=200)
    openScale.pack(side=tk.LEFT)

    projScale = Scale(master=lF, to=1000, orient=tk.HORIZONTAL,
                      label="Days Projected", length=150, tickinterval=1000,
                      command=updateProjDays)
    projScale.pack(side=tk.LEFT)
    projScale.set(projDays)
    lF.pack()

    f3 = Figure(figsize=(8, 6), dpi=100)
    projectedCases = np.append(currentCases, projI[1:])
    a3 = f3.add_subplot(111, yscale="linear",
                        yticks=np.linspace(0, np.amax(projectedCases), 10))
    dates = [day0 + timedelta(days=i) for i in range(projDays + days.size)]
    a3.plot(dates, projectedCases)
    a3.set_xlabel("Time (Months)")
    a3.set_ylabel("Projected Cases")
    a3.set_title(value + " COVID-19 Projected Cases")
    c3 = FigureCanvasTkAgg(f3, master=tab5)
    c3.draw()
    c3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.X, expand=1)


def textAssigner(value):
    text1.set(value)
    text2.set(value + " COVID-19 Confirmed Cases Graph")
    text3.set(value + " COVID-19 Statistics")
    text4.set(value + " COVID-19 Estimated Active Cases")
    text5.set(value + " COVID-19 Projections")


def search(event):
    county = countyName.get().strip()
    st = state.get().strip()
    if county == '' and st == '':
        textAssigner("USA")
        cases = covidCaseData[date].sum()
        totalpopulation = countyPopulationData['population'].sum()
        percentinfected = str(cases/totalpopulation*100)
        deaths = covidDeathData[date].sum()
        percentdeaths = str(deaths/cases*100)
        percentpopdeaths = str(deaths/totalpopulation*100)
        percentDeaths.set(percentdeaths[:5]+'%')
        percentPopDeaths.set(percentpopdeaths[:5]+'%')
        Cases.set(cases)
        Deaths.set(deaths)
        percentInfected.set(percentinfected[:5]+'%')
        totalPopulation.set(totalpopulation)

        dates = list(covidCaseData.columns)

        def dataAtIndex(i):
            return covidCaseData[i].sum()
        populateGraphTab("USA", dates, dataAtIndex, totalpopulation)

    elif county == '':
        textAssigner(st)
        stateDataFrame = covidCaseData.loc[covidCaseData['State'] == st]
        deathDataFrame = covidDeathData.loc[covidDeathData['State'] == st]
        populationDataFrame = countyPopulationData.loc[countyPopulationData['State'] == st]
        totalpopulation = populationDataFrame['population'].sum()
        cases = stateDataFrame[date].sum()
        percentinfected = str(cases/totalpopulation*100)
        deaths = deathDataFrame[date].sum()
        percentdeaths = str(deaths/cases*100)
        percentpopdeaths = str(deaths/totalpopulation*100)
        percentDeaths.set(percentdeaths[:5]+'%')
        percentPopDeaths.set(percentpopdeaths[:5]+'%')
        Cases.set(cases)
        Deaths.set(deaths)
        percentInfected.set(percentinfected[:5]+'%')
        totalPopulation.set(totalpopulation)

        dates = list(covidCaseData.columns)

        def dataAtIndex(i):
            return covidCaseData.loc[covidCaseData['State'] == st][i].sum()
        populateGraphTab(st, dates, dataAtIndex, totalpopulation)

    elif len(st) > 2 or st.isalpha() is False or county.replace(" ", "").isalpha() is False:
        textAssigner("**Error: Invalid Entry")

    else:
        textAssigner(county + ", " + st)
        countyDataFrame = covidCaseData.loc[(covidCaseData['State'] == st) & (
            covidCaseData['County Name'] == county)]
        populationDataFrame = countyPopulationData.loc[(countyPopulationData['State'] == st) & (
            countyPopulationData['County Name'] == county)]
        deathDataFrame = covidDeathData.loc[(covidDeathData['State'] == st) & (
            covidDeathData['County Name'] == county)]
        totalpopulation = populationDataFrame['population'].sum()
        deaths = deathDataFrame[date].sum()
        percentpopdeaths = str(deaths/totalpopulation*100)
        cases = countyDataFrame[date].sum()
        percentdeaths = str(deaths/cases*100)
        percentinfected = str(cases/totalpopulation*100)
        Cases.set(cases)
        Deaths.set(deaths)
        percentDeaths.set(percentdeaths[:5]+'%')
        percentPopDeaths.set(percentpopdeaths[:5]+'%')
        percentInfected.set(percentinfected[:5]+'%')
        totalPopulation.set(totalpopulation)

        dates = list(covidCaseData.columns)

        def dataAtIndex(i):
            return covidCaseData.loc[(covidCaseData['State'] == st) & (
                covidCaseData['County Name'] == county)][i].sum()
        populateGraphTab(county + ", " + st, dates,
                         dataAtIndex, totalpopulation)


def populateStatisticsTab():
    print()


def populateProjectionsTab():
    print()


#url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
# urllib.request.urlretrieve(url, downloadDirectory +
#                           'covid_confirmed_usafacts.csv')
#url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv"
# urllib.request.urlretrieve(url, downloadDirectory +
#                           'covid_deaths_usafacts.csv')
#url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv"
# urllib.request.urlretrieve(url, downloadDirectory +
#                           'covid_county_population_usafacts.csv')

covidCaseData = pd.read_csv(
    "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv")

covidDeathData = pd.read_csv(
    "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv")

countyPopulationData = pd.read_csv(
    "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv")

dates = list(covidCaseData.columns)

if yesterdaydate in dates:
    date = yesterdaydate
else:
    date = daybeforedate


tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

# Tab 1 - Search tab
tabControl.add(tab1, text='Search')

countyName = StringVar()
state = StringVar()
text1 = StringVar()
Label(tab1, textvariable=text1).grid(row=3, column=1)
tk.Entry(tab1, textvariable=countyName).grid(row=0, column=1)
tk.Entry(tab1, textvariable=state).grid(row=1, column=1)
Label(tab1, text="County Name").grid(row=0)
Label(tab1, text="State").grid(row=1)
Label(tab1, text="*Must Be In 2 Letter Format (Ex. PA)*").grid(row=1, column=2)
Label(tab1, text="*County Name Can Be Left Blank For Statewide Statistics*").grid(row=0, column=2)
Label(tab1, text="*Both Fields Can Be Left Blank For Nationwide Statistics*").grid(row=2, column=2)
Label(tab1, text="Results For:").grid(row=3, column=0)
searchbutton = tk.Button(tab1, text='Search')
searchbutton.bind('<Button-1>', search)
searchbutton.grid(row=2, column=1)

# Tab 2 - confirmed cases graph
tabControl.add(tab2, text='Graph')

text2 = StringVar()
# Label(tab2, textvariable=text2).grid(row=0)

# Tab 3 - general statistics
tabControl.add(tab3, text='Statistics')

text3 = StringVar()
percentInfected = StringVar()
Cases = StringVar()
Deaths = StringVar()
percentDeaths = StringVar()
totalPopulation = StringVar()
percentPopDeaths = StringVar()
Label(tab3, textvariable=text3).grid(row=0)
Label(tab3, text="Cases:").grid(row=1, column=0)
Label(tab3, textvariable=Cases).grid(row=1, column=1)
Label(tab3, text="Total Population:").grid(row=2, column=0)
Label(tab3, textvariable=totalPopulation).grid(row=2, column=1)
Label(tab3, text="Percentage Infected:").grid(row=3, column=0)
Label(tab3, textvariable=percentInfected).grid(row=3, column=1)
Label(tab3, text="Deaths:").grid(row=4, column=0)
Label(tab3, textvariable=Deaths).grid(row=4, column=1)
Label(tab3, text="Percentages of Cases Resulting in Death:").grid(row=5, column=0)
Label(tab3, textvariable=percentDeaths).grid(row=5, column=1)
Label(tab3, text="Percentage of Population Dead:").grid(row=6, column=0)
Label(tab3, textvariable=percentPopDeaths).grid(row=6, column=1)

# Tab 4 - estimated current cases
tabControl.add(tab4, text='Estimations')
text4 = StringVar()

# Tab 5 - projected graph
tabControl.add(tab5, text='Projections')

text5 = StringVar()
# Label(tab5, textvariable=text5).grid(row=0)

tabControl.pack(expand=1, fill="both")
win.geometry("1000x600")
win.mainloop()
