import datetime
import tkinter

class habits(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.grid()
        self.username = "User"

        self.titleVariable = tkinter.StringVar()
        title = tkinter.Label(self, textvariable=self.titleVariable,
                              fg="blue")
        title.grid(column=0, row=0, columnspan=2)
        
        self.titleVariable.set(self.username + "'s Habits")

        setuserbutton = tkinter.Button(self, text="Set user", command=lambda:
                                       self.dialoguebox("Enter username", self.submit_name))
        setuserbutton.grid(column=3, row=0)

        catbutton = tkinter.Button(self, text="New category")
        catbutton.grid(column=0, row=1)
        
        habbutton = tkinter.Button(self, text="New habit")
        habbutton.grid(column=1, row=1)

    def dialoguebox(self, msg, submit, extra=True):
        top = self.top = tkinter.Toplevel(self)
        dialoguelabel = tkinter.Label(top, text=msg)
        dialoguelabel.grid(row=0, column=0)

        if extra:
            self.dialogueentry = tkinter.Entry(top)
            self.dialogueentry.grid(row=1)
            self.dialogueentry.focus_set()
            self.dialogueentry.bind("<Return>", submit)

            self.submitbutton = tkinter.Button(top, text="OK")
            self.submitbutton.bind("<Button-1>", submit)
            self.submitbutton.grid(row=2, column=1)

        self.cancelbutton = tkinter.Button(top, text="Cancel",
                                      command=lambda: self.top.destroy())
        self.cancelbutton.grid(row=2, column=2)

    def submit_name(self, event):
        data = self.dialogueentry.get()
        if data:
            self.username = data
            self.top.destroy()
            self.titleVariable.set(self.username + "'s Habits")
        
                       

if __name__ == "__main__":
    app = habits(None)
    app.title("It's going to be a great day!")
    app.mainloop()
        
categories = {} ##creates a blank dictionary to contain categories
tasks = {}  ##creates a blank dictionary to contain all tasks
currentdate = datetime.date.today()
    
class Category(object):
    '''A category has a name,which will be displayed as a heading.
    It contains a dictionary of tasks, indexed by id.
    It has a position (1-n) in an ordered list of categories.
    It has a colour, indicating the background colour of the heading.
    It has a row, indicating its display row.
    It has an id, which is a unique identifier, used as an index.'''
    def __init__(self, name, pos = len(categories) + 1, colour = "white",):
        self.name = name
        self.contents = []
        self.pos = pos
        self.colour = colour
        self.row = self.catrow()
        self.column = self.catcolumn()
        self.score = {}

    def __repr__(self):
        return "Category("+self.name+", "+str(self.pos)+", "+self.colour+")"

    def catcolumn(self):
        return abs(self.pos%2 - 1)
    
    def catrow(self):
        catrow = 0
        if self.pos >= 3:
            prevcat = categories[self.pos - 2]
            catrow = len(prevcat.contents) + prevcat.row + 1
        return catrow

    def delcat(self):
        '''Deletes a Category from the categories dictionary. All tasks within
the category are deleted'''
        for e in categories[self.name].contents:
            tasks[e].deltask()
        del categories[self.name]

class Task(object):
    def __init__(self, name, category, points, bonus, pos):
        self.name = name
        self.category = category
        self.points = points
        self.bonus = bonus
        self.pos = pos
        tasks[self.name] = self.category
        self.column = self.taskcolumn()
        self.row = self.taskrow()
        categories[self.category].contents.insert(self.pos,self.name)
        self.score = {}

    def __repr__(self):
        return "Task("+self.name+", "+self.category+", "+str(self.points)+", "+str(self.pos)+")"

    def taskcolumn(self):
        return categories[self.category].column

    def taskrow(self):
        return categories[self.category].row + self.pos

    def deltask(self):
        '''deletes a task from its category contents list, moves the position of
all remaining tasks in that category up by one, and deletes the Task from the task
dictionary'''
        categories[self.category].contents.remove(self.name)
        for e in categories[self.category].contents:
            tasks[e].pos -= 1
        del tasks[self.name]

    def changecat(self, newcat, newpos):
        '''moves a task to a different category'''
        categories[self.category].contents.remove(self.name)
        self.category = newcat
        categories[newcat].contents.insert(newpos, self.name)

    def incrementscore(self, inc):
        '''updates the score for a habit by creating or modifying an entry in
the score dictionary (with the current date as key). The habit's points
attribute is multiplied by inc to get the amount by which the score is changed'''
        global currentdate
        yesterday = currentdate + datetime.timedelta(days=-1)
        if currentdate in self.score:
            self.score[currentdate] += self.points * inc
            categories[self.category].score[currentdate] += self.points * inc
        else:
            self.score[currentdate] = self.points * inc
            categories[self.category].score[currentdate] = self.points * inc
        if yesterday in self.score and self.score[yesterday] > 0:
            self.score[currentdate] += self.bonus * inc
            categories[self.category].score[currentdate] += self.bonus * inc
        

def newcategory():
    defaultpos = len(categories) + 1
    catname = input("category name: ")
    catpos = input("list position (default: end): ") or str(defaultpos)
    catpos = int(catpos)
    catcolour = input("header colour (default: white): ") or "white"
    categories[catname] = Category(catname, catpos, catcolour)
    
                      
def newtask():
    taskname = input("task name: ")
    taskpoints = (input("points: ")) or str(1)
    taskpoints = int(taskpoints)
    taskbonus = (input("bonus: ")) or str(0)
    taskbonus = int(taskbonus)
    taskcat = input("category: ") or 'a'
    defaultpos = len(categories[taskcat].contents) + 1
    taskpos = input("list position (default: end): ") or str(defaultpos)
    taskpos = int(taskpos)
    tasks[taskname] = Task(taskname, taskcat, taskpoints, taskbonus, taskpos)
    
def setdate():
    isValid = False
    while not isValid:
        userdate = (input("date (dd/mm/yyyy): "))
        try: # strptime throws an exception if the input doesn't match the pattern
            d = datetime.datetime.strptime(userdate, "%d/%m/%Y").date()
            isValid=True
        except:
            print ("Incorrect format. Try again. (dd/mm/yyyy)\n")
    return d




            


