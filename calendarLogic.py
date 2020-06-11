import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkcalendar import DateEntry
import datetime

from meetingPlanner import *



#some global variables for our evvent planner

#begDate is the beginning date for our event
begDate=None


#endDate is the end date for our event
endDate=None

#personEntered is set to see if at least one person is entered
personEntered=None

#persons is a set of people that the user entered
persons=set()

#graph is a graph object for the event planning
graph=None

lowDate=None
endDate=None

isDestroyed=False

dateEntered=None





def viewCalendar():
    top = tk.Toplevel(root)

    today=datetime.date.today()

    mindate=datetime.date.today()
    #exception handling

    try:
        maxdate=datetime.date(mindate.year+4,mindate.month,mindate.day)
    except:
        #then we were on a leap year on last day of Feb
        maxdate=datetime.date(mindate.year+4,mindate.month+1,1)

    cal=Calendar(top,font="Arial 14",selectmode='day',locale='en_US',mindate=mindate,maxdate=maxdate,disabledforeground='red',cursor="hand1",year=mindate.year,month=mindate.month,day=mindate.day)
    cal.pack(fill="both",expand=True)


#method to get initial date range for event
def getInitialDateRange():

    def setBegDate():
        global begDate
        begDate=cal.get_date()
        top.destroy()
        getInitialDateRange()

    def setEndDate():
        global endDate 
        endDate=cal.get_date()
        #destroying current window
        top.destroy()
        #setup for the rest
        for widget in root.winfo_children():
            widget.destroy()
        #now we can create the graph
        global begDate
        global graph
        graph=DateGraph(begDate,endDate)
        #setting up person selection
        setupPersonSelection()        

    top =tk.Toplevel(root)
    if (begDate==None):
        Lab=ttk.Label(top,text='Choose the first possible date for your event!')
        Lab.pack()
    else :
        Lab=ttk.Label(top,text='Choose the last possible date for your event!')
        Lab.pack()

    if (begDate==None):
        mindate=datetime.date.today()
    else:
        mindate=begDate
    #exception handling

    try:
        maxdate=datetime.date(mindate.year+4,mindate.month,mindate.day)
    except:
        #then we were on a leap year on last day of Feb
        maxdate=datetime.date(mindate.year+4,mindate.month+1,1)

    cal=DateEntry(top,width=12,background='darkblue',foreground='white',borderwidth=2,mindate=mindate,maxdate=maxdate)
    cal.pack(padx=10,pady=10) 
    if (begDate==None):
        con=ttk.Button(top,text="confirm",command=setBegDate)
        con.pack()
    else :
        con=ttk.Button(top,text="confirm",command=setEndDate)
        con.pack()
    

def setupPersonSelection():
    def moveToAvailability():
        #we first check if the text is empty or not
        textString = name.get().replace(" ","").lower()
        if (textString!=""):
            #if its empty, we do nothing
            #else, we add the name to users and continue
            global persons
            global personEntered
            persons.add(textString)
            personEntered=textString
            #now we clear the root and setup date selection
            for widget in root.winfo_children():
                widget.destroy()    
            setupDateSelection()
    def moveToResult():
        #destroy current widgets and make the screen a result screen
        for widget in root.winfo_children():
            widget.destroy()    
        setupResultView()
    sel=label=ttk.Label(root,text="Participant Selection")
    sel.pack()
    name = tk.StringVar()
    nameText=ttk.Entry(root,text="Enter Name",textvariable=name)
    nameText.pack()
    availabilityButton = ttk.Button(root,text="Set Availablity for This Participant",command=moveToAvailability)
    availabilityButton.pack()
    if (personEntered!=None):
        #then we need to add an extra option to stop person entering
        moveToResultsButton=ttk.Button(root,text="Stop entering Persons",command=moveToResult)
        moveToResultsButton.pack()

def setupDateSelection():
    global isDestroyed
    isDestroyed=False
    global dateEntered
    dateEntered=None

    def moveToPersonView():
        #basically destroying the root and getting the person view again
        for widget in root.winfo_children():
            widget.destroy()
        setupPersonSelection()

    def setStopDatesButton():
        global dateEntered
        if (dateEntered!=None):
            stopDateButton=ttk.Button(root,text="Stop entering dates",command=moveToPersonView)
            stopDateButton.pack()

    def destroyAvailables():
        #function to destroy "all available" and "all unavailable" options once a user enters a date or date range
        global isDestroyed
        if (isDestroyed==False):
            allAvailableButton.destroy()
            allAbsentButton.destroy()
            isDestroyed=True


    def setAbsent():
        global graph
        graph.addAbsentUser(personEntered)
        moveToPersonView()
    def setAvailable():
        #available doesnt really do anything, we just move on to the next user
        moveToPersonView()
    
    def selectIndividualDate():
        def confirmIndividualDate():
            global dateEntered
            dateEntered=cal.get_date()
            #now I add the user/date pair to the graph and remove the window
            global graph
            graph.addUserDate(personEntered,dateEntered)
            destroyAvailables()
            top.destroy()
            setStopDatesButton()

        top =tk.Toplevel(root)
        ttk.Label(top,text='Choose a date').pack(padx=10,pady=10)
        global begDate
        global endDate
        mindate=begDate

        maxdate=endDate
        cal=DateEntry(top,width=12,background='darkblue',foreground='white',borderwidth=2,mindate=mindate,maxdate=maxdate)
        cal.pack(padx=10,pady=10)
        conf=ttk.Button(top,text="confirm",command=confirmIndividualDate)
        conf.pack()
  
    def getAbsenceRange():
        def setLowDate():
            global lowDate
            lowDate=cal.get_date()
            top.destroy()
            getAbsenceRange()

        def setHighDate():
            global highDate
            global lowDate
            highDate=cal.get_date()
            #for I/O removal of buttons
            global dateEntered
            dateEntered=highDate
            destroyAvailables()
            #destroying current window
            top.destroy()
            #now we can add all the dates in this range to the graph

            dates=getDateRange(lowDate,highDate)
            #resetting low date in case user wants to put other ranges
            lowDate=None
            highDate=None
            
            #adding to graph
            global graph
            global personEntered
            for x in dates:
                graph.addUserDate(personEntered,x)
            #setting up stop dates button to go back to person select 
            setStopDatesButton()

        top =tk.Toplevel(root)
        global lowDate
        global highDate
        if (lowDate==None):
            mssg =ttk.Label(top,text='Choose the first date for the range of absence!')
            mssg.pack()
        else :
            mssg=ttk.Label(top,text='Choose the last date for the range of absence!')
            mssg.pack()

        if (lowDate==None):
            global begDate
            mindate=begDate
        else:
            mindate=lowDate
        #exception handling

        global endDate
        maxdate=endDate

        cal=DateEntry(top,width=12,background='darkblue',foreground='white',borderwidth=2,mindate=mindate,maxdate=maxdate)
        cal.pack(padx=10,pady=10) 
        if (lowDate==None):
            confirm=ttk.Button(top,text="confirm",command=setLowDate)
            confirm.pack()
        else :
            confirm=ttk.Button(top,text="confirm",command=setHighDate)
            confirm.pack()






    #now we attach some widget buttons to the root
    global personEntered
    label=ttk.Label(root,text="Select Availability For "+personEntered)
    label.pack()
    allAvailableButton= ttk.Button(root,text="Available on Every Day",command=setAvailable)
    allAvailableButton.pack()
    allAbsentButton=ttk.Button(root,text="Unavailable on Every Day",command=setAbsent)
    allAbsentButton.pack()
    selectDateRangeButton=ttk.Button(root,text="Select Date Range where the individual is absent",command=getAbsenceRange)
    selectDateRangeButton.pack()
    selectIndividualDateButton=ttk.Button(root,text="Select Individual Date where the individual is absent",command=selectIndividualDate)
    selectIndividualDateButton.pack()
    stopDatesButton=None

def setupResultView():

    def showAbsentPopup():
        top=tk.Toplevel(root)
        #need to attach a list of total users and the list of absent users
        #first a label with the date
        lab = ttk.Label(top,text=dateList.get((dateList.curselection()[0])))
        lab.pack()
        allLab=ttk.Label(top,text="All Users")
        allLab.pack(side="left")
        absentLab=ttk.Label(top,text="Absent Users")
        absentLab.pack(side="right")
        #making a list of total users from global data
        allUserList = tk.Listbox(top)
        global persons
        for x in persons:
            allUserList.insert(tk.END,x)
        #attaching scroll bar to the list
        AllScroll = tk.Scrollbar(top,orient="vertical")
        allUserList.config(yscrollcommand=AllScroll.set)
        AllScroll.config(command=allUserList.yview)
        AllScroll.pack(side="left",fill="y")

        allUserList.pack(side="left")
        #creating list of absent users
        absentUserList = tk.Listbox(top)
        global graph
        absentList =graph.getAbsentUsers(bestDates[(dateList.curselection())[0]]) 
        for x in absentList:
            absentUserList.insert(tk.END,x)
        absentScroll = tk.Scrollbar(top,orient="vertical")
        absentUserList.config(yscrollcommand=absentScroll.set)
        absentScroll.config(command=absentUserList.yview)
        absentScroll.pack(side="right",fill="y")

        absentUserList.pack(side="right")
    label=ttk.Label(root,text="Best Dates for the Event")
    label.pack()
    #basically i need a scrollable list of clickable dates
    #on click, a popup shows with the date info and whos absent
    #So, I make a button for each best date with the num absent and the date in string format
    global graph
    bestDates = graph.getBestDates()
    absentButton = ttk.Button(root,text="See who is absent on the selected date",command=showAbsentPopup)
    absentButton.pack()
    dateList = tk.Listbox(root)
    for x in bestDates:
        dateList.insert(tk.END,x.strftime("%b/%d/%Y"))
    scroll = tk.Scrollbar(root,orient="vertical")
    dateList.config(yscrollcommand=scroll.set)
    scroll.config(command=dateList.yview)
    scroll.pack(side=tk.RIGHT,fill=tk.Y)
    dateList.pack(expand=True,fill=tk.Y)

root=tk.Tk()


label=ttk.Label(root,text="Welcome to My Planner",font="Sans 20")
label.pack(pady=10,padx=10)


calButt=ttk.Button(root,text='View the Calendar',command=viewCalendar)
calButt.pack()


initButt=ttk.Button(root,text='Enter a Date Range for Your Event',command=getInitialDateRange)
initButt.pack()

#ttk.Button(root,text='Choose Date Range',command=getDateRange).pack(padx=10,pady=10)

#ttk.Button(root,text='Choose Single Date',command=getIndividualDate).pack(padx=19,pady=10)
#ttk.Button(root,text='This User is All Absent!').pack(padx=19,pady=10)
#ttk.Button(root,text='This User is All Present!').pack(padx=19,pady=10)

root.mainloop()
