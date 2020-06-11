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

def getDateRange():
    #just using individual date method to get date range
    top =tk.Toplevel(root) 
    mindate = datetime.date.today()
    try:
        maxdate=datetime.date(mindate.year+4,mindate.month,mindate.day)
    except:
        #then we were on a leap year on last day of Feb
        maxdate=datetime.date(mindate.year+4,mindate.month+1,1)

    ttk.Label(top,text='Choose First Date of Range').pack(padx=10,pady=10)
    cal=DateEntry(top,width=12,background='darkblue',foreground='white',borderwidth=2,mindate=mindate,maxdate=maxdate)
    cal.pack(padx=10,pady=10)

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
        ttk.Label(top,text='Choose the first possible date for your event!').pack(padx=10,pady=10)
    else :
        ttk.Label(top,text='Choose the last possible date for your event!').pack(padx=10,pady=10)

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
        ttk.Button(top,text="confirm",command=setBegDate).pack()
    else :
        ttk.Button(top,text="confirm",command=setEndDate).pack()
    

def setupPersonSelection():
    def moveToAvailability():
        #we first check if the text is empty or not
        textString = nameText.get().replace(" ","").lower()
        if (textString!=""):
            #if its empty, we do nothing
            #else, we add the name to users and continue
            global persons
            global personEntered
            persons.add(textString())
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
    label=ttk.Label(root,text="Participant Selection").pack()
    nameText=ttk.Entry(root,text="Enter Name").pack()
    availabilityButton = ttk.Button(root,text="Set Availablity for This Participant",command=moveToAvailability).pack(padx=10,pady=10)
    if (personEntered!=None):
        #then we need to add an extra option to stop person entering
        moveToResultsButton=ttk.Button(root,text="Stop entering Persons",command=moveToResult).pack(padx=10,pady=10)

def setupDateSelection():
    isDestroyed=False
    dateEntered=None

    def moveToResultView():
        #basically destroying the root and getting the result screen
        for widget in root.winfo_children():
            widget.destroy()
        setupResultView()

    def setStopDatesButton():
        stopDateButton=ttk.Button(root,text="Stop entering dates",command=moveToResultView).pack()

    def destroyAvailables():
        #function to destroy "all available" and "all unavailable" options once a user enters a date or date range
        if (!isDestroyed):
            allAvailableButton.destroy
            allAbsentButton.destroy
            isDestroyed=True


    def setAbsent():
        global graph
        graph.addAbsentUser(personEntered)
        for widget in root.winfo_children():
            widget.destroy()
        setupPersonSelection()
    def setAvailable():
        #available doesnt really do anything, we just move on to the next user
        for widget in root.winfo_children():
            widget.destroy()
        setupPersonSelection()
    
    def selectIndividualDate():
        def confirmIndividualDate():
            dateEntered=cal.get_date()
            #now I add the user/date pair to the graph and remove the window
            global graph
            graph.addUserDate(personEntered,dateEntered)
            destroyAvailables()
            top.destroy()

        top =tk.Toplevel(root)
        ttk.Label(top,text='Choose a date').pack(padx=10,pady=10)

        mindate=datetime.date.today()
        #exception handling

        try:
            maxdate=datetime.date(mindate.year+4,mindate.month,mindate.day)
        except:
            #then we were on a leap year on last day of Feb
            maxdate=datetime.date(mindate.year+4,mindate.month+1,1)

        cal=DateEntry(top,width=12,background='darkblue',foreground='white',borderwidth=2,mindate=mindate,maxdate=maxdate)
        cal.pack(padx=10,pady=10)
        ttk.Button(top,text="confirm",command=confirmIndividualDate).pack()
  
    def getDateRange():
        lowDate=None
        highDate=None
        def setLowDate():
            lowDate=cal.get_date()
            top.destroy()
            getDateRange()

        def setHighDate():
            highDate=cal.get_date()
            #for I/O removal of buttons
            dateEntered=highDate
            #destroying current window
            top.destroy()
            #now we can add all the dates in this range to the graph
            dates=getDateRange(lowDate,highDate)
            #adding to graph
            global graph
            global personEntered
            for x in dates:
                graph.addUserDate(personEntered,x)
                

        top =tk.Toplevel(root)
        if (lowDate==None):
            ttk.Label(top,text='Choose the first possible date for your event!').pack(padx=10,pady=10)
        else :
            ttk.Label(top,text='Choose the last possible date for your event!').pack(padx=10,pady=10)

        if (lowDate==None):
            global begDate
            mindate=begDate
        else:
            mindate=lowDate
        #exception handling

        try:
            maxdate=datetime.date(mindate.year+4,mindate.month,mindate.day)
        except:
            #then we were on a leap year on last day of Feb
            maxdate=datetime.date(mindate.year+4,mindate.month+1,1)

        cal=DateEntry(top,width=12,background='darkblue',foreground='white',borderwidth=2,mindate=mindate,maxdate=maxdate)
        cal.pack(padx=10,pady=10) 
        if (lowDate==None):
            ttk.Button(top,text="confirm",command=setLowDate).pack()
        else :
            ttk.Button(top,text="confirm",command=setHighDate).pack()






    #now we attach some widget buttons to the root
    global personEntered
    label=ttk.Label(root,text="Select Availability For "+personEntered).pack()
    allAvailableButton= ttk.Button(root,text="Available on Every Day",command=setAvailable).pack()
    allAbsentButton=ttk.Button(root,text="Unavailable on Every Day",command=setAbsent).pack()
    selectDateRangeButton=ttk.Button(root,text="Select Date Range where the individual is absent",command=selectDateRange).pack()
    selectIndividualDateButton=ttk.Button(root,text="Select Individual Date where the individual is absent",command=selectIndividualDate).pack()
    stopDatesButton=None

def setupResultView():
    label=ttk.Label(root,text="Best Dates for the Event").pack()

root=tk.Tk()


label=ttk.Label(root,text="Welcome to My Planner",font="Sans 20")
label.pack(pady=10,padx=10)


ttk.Button(root,text='View the Calendar',command=viewCalendar).pack(padx=10,pady=10)

ttk.Button(root,text='Enter a Date Range for Your Event',command=getInitialDateRange).pack(padx=10,pady=10)

#ttk.Button(root,text='Choose Date Range',command=getDateRange).pack(padx=10,pady=10)

#ttk.Button(root,text='Choose Single Date',command=getIndividualDate).pack(padx=19,pady=10)
#ttk.Button(root,text='This User is All Absent!').pack(padx=19,pady=10)
#ttk.Button(root,text='This User is All Present!').pack(padx=19,pady=10)

root.mainloop()
