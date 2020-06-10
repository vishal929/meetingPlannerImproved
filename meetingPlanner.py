import datetime

#Defining a graph type class for my dates
#basically the user will enter people and the dates that they cannot make it
#then, we will create a graph with all the dates of absences
#if there are as many absences as dates in the range, then we will choose the dates with the least people absent
#otherwise we will choose the dates with nobody absent

#dateNode class, which has a date, list of users associated with it, and a degree
class DateData:
    def __init__(self):
        self.usersAbsent=set()
        self.degree=0


#dateGraph class, which hosts our graph of DateNode nodes
class DateGraph:
    def __init__(self,begDate,endDate):
        listDates = getDateRange(begDate,endDate)
        #list that holds dates in the graph and maps each date to date data
        self.dates={}
        #at initialization (initializes data for every date in the range)
        for x in listDates:
            self.dates[x]=DateData()
        #list of users that are all present
        self.completelyPresent=set()
        #list of users that are completely absent
        self.completelyAbsent=set()
    
    #adding a specific node based on user-timedate key pair
    def addUserDate(self,user,timedate):
        #date that the user is absent must be a valid date (guarunteed to exist upon initialization of the graph)
        dataToConsider = self.dates[timedate]
        dataToConsider.usersAbsent.add(user)
        dataToConsider.degree=len(dataToConsider.usersAbsent)
        
    #adding a user that is completely absent
    def addAbsentUser(self,user):
        self.completelyAbsent.add(user)

    #adding a user that is completely present
    def addPresentUser(self,user):
        self.completelyPresent.add(user)
    
    #getting all the users that are absent on a specific date
    def getAbsentUsers(self,timedate):
        absentees=[]
        for x in self.dates[timedate].usersAbsent:
            absentees.append(x)
        for x in self.completelyAbsent:
            absentees.append(x)
        return absentees

    #counts the degree of a node
    def countDegree(self,timedate):
        #count the degree here
        #we just count the number of users associated to this date
        count=0
        for person in self.dates[timedate].usersAbsent:
            count+=1
        return count

    #method to get the best dates in the graph
    def getBestDates(self):
        #goes through all the dates and gets a list of the best dates (based on least people missing)
        #i do one pass to find the date with the least people absent (least degree)
        #then i do another pass to add other dates with the same degree and add them to the list
        bestDate=None
        bestDates=[]
        for x in self.dates:
            if (bestDate==None):
                bestDate=x
            else :
                if (self.countDegree(bestDate)>self.countDegree(x)):
                    #then x has the least people absent
                    bestDate=x
        
        #second pass to add all the dates with this least associativity
        for x in self.dates:
            if (self.countDegree(x)==self.countDegree(bestDate)):
                bestDates.append(x)
        #returning the list of best dates, ready to be printed out to the user
        return bestDates

    #function to print out the list of best dates and the users attending
    def printBestDates(self):
            listDates = self.getBestDates()
            if (len(listDates)>1):
                print("Best Dates and Absentees:\n")
                print("------------------------------------------------------\n")
            else :
                print("Best Date and Absentees:\n")
                print("------------------------------------------------------\n")
            
            #now iterating through the dates given and printing out the date and the absentees
            for x in listDates:
                print(x.strftime("%b/%d/%Y\n"))
                print("Absent:")
                listAbsent = self.getAbsentUsers(x)
                if (len(listAbsent)==0):
                    print("NOBODY ABSENT!!!")
                else:
                    for y in listAbsent:
                        if (y!=len(listAbsent)-1):
                            print(" "+y+",")
                        else:
                            print(" "+y)
                
                print("\n")
                print("------------------------------------------------------\n")
        
#some functions to help with date stuff

#gets all the dates in the given range (returns a list of datetimes)
def getDateRange(begDate,endDate):
    testDate=datetime.date(begDate.year,begDate.month,begDate.day)
    dates=[]
    while(testDate <=endDate):
       dates.append(testDate)
       testDate+=datetime.timedelta(days=1)
    return dates



#function to check if a date is in the range specified by the user
def isValidDate(enteredDate, begDate,endDate):
    if (enteredDate<=endDate and enteredDate>=begDate):
        return True
    else:
        return False


#function to turn a string in form of "mm/dd/yy" into a datetime
def getDateTime(enteredDate):
    #print("date"+enteredDate)
    #print("month"+enteredDate[0:2]+"\n")
    #print("day"+enteredDate[3:5]+"\n")
    #print("year"+enteredDate[6:10]+"\n")
    #date=datetime.date(int(enteredDate[6:9]),int(enteredDate[0:1]),int(enteredDate[3:4]))
    #return date
    dateTime =datetime.datetime.strptime(enteredDate,"%m/%d/%Y")
    return datetime.date(dateTime.year,dateTime.month,dateTime.day)


#when user is entering data about other users, they can optionally say ALL ABSENT Except ..., ALL ABSENT, NOT ABSENT, NOT ABSENT except..., in addition to just listing dates
#if a user is all absent, then they can just be excluded from the graph basically.
#likewise, if a user is not absent, they can also be excluded from the graph
def main():
    #creating a graph to use
    while True:
        dateRange = input("Please enter a date range for the event in the format mm/dd/yyyy:mm/dd/yyyy\n")
        #removing whitespace from the entire date, if any
        dateRange=dateRange.replace(" ","")
        if (len(dateRange)!=21):
            print("Date range could not be recognized! Please enter a valid date range in the format mm/dd/yyyy:mm/dd/yyyy\n")
            continue

        #splitting up ending date string and beginning date string
        dateRange=dateRange.split(":")
        begDate=dateRange[0]
        endDate=dateRange[1]
        #turning our date strings into actual date objects for future usefulness
        #exception checking
        try:
            begDate=getDateTime(begDate)
            endDate=getDateTime(endDate)
        except :
            print("The date range could not be recognized! Please try again in the format mm/dd/yyyy:mm/dd/yyyy\n")
            continue
        if (endDate<begDate):
            print("The ending date is earlier than the starting date! Please enter a valid date range!")
            continue
        #creating our date graph with the given date range
        graph = DateGraph(begDate,endDate)
        #list of all usernames entered in this operation
        users=set()
        print("Now you will be prompted to enter information for each user associated with this event: \n")
        break
    while True:
        user=input("please enter the person's name. Enter - if you want to stop.\n")
        user=user.replace(" ","")
        if (user=="-"):
            break
        else :
            users.add(user)
            #this is so user cannot select allAbsent or allpresent after picking a date
            userSelectedDate=False
        while True:
            dates=None
            if (userSelectedDate):
                dates=input("Please enter an individual date in the form mm/dd/yyyy or a range in the form mm/dd/yyyy:mm/dd/yyyy, or - if you wish to stop entering dates.") 
            else:
                dates=input("Please enter either ALL ABSENT, ALL PRESENT, a date range of the form mm/dd/yyyy:mm/dd/yyyy in which the individual WOULD BE ABSENT, or an individual date of the form mm/dd/yyyy in which the individual WOULD BE ABSENT and hit enter. When you wish to stop please enter - .\n")


            dates=dates.replace(" ","")
            dates=dates.lower()
            if (dates=="allabsent"):
                if (userSelectedDate):
                    print("I am sorry, it seems there was an invalid input! Please try again: \n")
                else:
                    #we have to check off all absent
                    graph.addAbsentUser(user)
                    break
            elif (dates=="-"):
                #then we stop
                break
            elif (dates=="allpresent"):
                if (userSelectedDate):
                    print("I am sorry, it seems there was an invalid input! Please try again: \n")
                else:
                    #we have to check off all present
                    #in other words, do nothing, because all present doesnt really matter
                    break
            elif (len(dates)==21 and dates[10]==":"):
                #we have a date range
                #we should check if start date is valid and end date is valid
                dates=dates.split(":")
                start = dates[0]
                end = dates[1]
                #exception handling
                try:
                    start = getDateTime(start)
                    end=getDateTime(end)
                except:
                    print("The date range could not be recognized. Please try again in the format mm/dd/yyyy:mm/dd/yyyy \n")
                    continue
                if (isValidDate(start,begDate,endDate) and isValidDate(end,begDate,endDate)):
                    #then i need to add all the dates in this range to the dictionary
                    datesList = getDateRange(start,end)
                    for x in datesList:
                        #I need to add the date user pair to the graph
                        graph.addUserDate(user,x)
                    userSelectedDate=True
                else:
                    #then we have some invalid input
                    print("I am sorry, it seems there was an invalid input! Please try again: \n")
            elif(dates[2]=="/" and dates[5]=="/"):
                #then we have an individual date
                #we should check if this date is valid and then if valid, we add it, else not
                #exception handling
                try:
                    dates=getDateTime(dates)
                except:
                    print("Date could not be recognized. Please try again in the form mm/dd/yyyy \n")
                    continue
                if (isValidDate(dates,begDate,endDate)):
                    #then we add this date to the graph dictionary
                    graph.addUserDate(user,dates)
                    userSelectedDate=True
                else:
                    print("I am sorry, it seems there was an invalid input! Please try again: \n")
            else:
                #then we have some invalid input
                print("I am sorry, it seems there was an invalid input! Please try again: \n")
    #now we find the list of the best dates and print them
    #we first print the list of all the users
    print("Users associated with this event: \n")
    for x in users:
        print(x+"\n")
    #now i print the output of the best dates
    graph.printBestDates()


#running my main
if (__name__=="__main__"):
    main()
