import datetime
import tkinter

class HabitsGui(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.grid()
        self.username = "User"
        self.handler = HabitsHandler()
        self.labels = []

        self.titleVariable = tkinter.StringVar()
        title = tkinter.Label(self, textvariable=self.titleVariable,
                              fg="blue")
        title.grid(column=0, row=0, columnspan=2)
        
        self.titleVariable.set(self.username + "'s Habits")

        self.rowVariable = tkinter.IntVar()
        self.rowVariable.set(len(self.handler.categories) + len(self.handler.tasks) + 1)

        self.updatelists()
        
        setuserbutton = tkinter.Button(self, text="Set user", command=lambda:
                                       self.dialoguebox(["Enter username"], self.submit_name))
        setuserbutton.grid(column=3, row=0)

        catbutton = tkinter.Button(self, text="New category", command=lambda:
                                self.dialoguebox(["Category name:", "Position:",
                                    "Heading colour:"], self.submit_newcategory, 3))
        catbutton.grid(column=0, row=self.rowVariable.get())
        
        habbutton = tkinter.Button(self, text="New habit", command=lambda:
                                   self.dialoguebox(["Task name:", "Category:",
                                        "Points:", "Bonus points:", "Position:"],
                                        self.submit_newtask, 5))
        habbutton.grid(column=1, row=self.rowVariable.get())


    def updatelists(self):
        if hasattr(self, 'lists'):
            self.lists.destroy()
        self.lists = tkinter.Frame(self.parent, borderwidth=1)
        self.lists.grid(row=1)
        for key in self.handler.categories:
            self.labels.insert(self.handler.categories[key].pos, key)
            self.key = tkinter.Label(self.lists, text=key,
                                  bg=self.handler.categories[key].colour)
            self.key.grid(column=0, row=self.handler.categories[key].pos)
            print (key)
            print (self.handler.categories[key].pos)
            print (self.key.grid_info())

    def dialoguebox(self, msg, submit, entries=1):
        top = self.top = tkinter.Toplevel(self)
        self.variables = []
        self.allentries = []
        for i in range(entries):
            label = tkinter.Label(top, text=msg[i])
            label.grid(row=i, column=0, sticky='w')
            entry = tkinter.Entry(top)
            entry.grid(row=i, column=1)
            self.variables.append(label)
            self.allentries.append(entry)            
            
        self.allentries[0].focus_set()
        self.allentries[-1].bind("<Return>", submit)

        self.submitbutton = tkinter.Button(top, text="OK")
        self.submitbutton.bind("<Button-1>", submit)
        self.submitbutton.grid(row=entries+1, column=1, sticky='e')

        self.cancelbutton = tkinter.Button(top, text="Cancel",
                                      command=lambda: self.top.destroy())
        self.cancelbutton.grid(row=entries+1, column=2)

    def submit_name(self, event):
        data = self.allentries[0].get()
        if data:
            self.username = data
            self.top.destroy()
            self.titleVariable.set(self.username + "'s Habits")

    def submit_newcategory(self, event):
        '''creates a new category with dialogue entries
catname, catpos, catcolour'''
        data = []
        if self.allentries[0].get() != '':
            data.append(self.allentries[0].get())
        else:
            data.append('new category')
        if self.allentries[1].get() != '':
            data.append(int(self.allentries[1].get()))
        else:
            data.append(len(self.handler.categories))
        if self.allentries[2].get() != '':
            data.append(self.allentries[2].get())
        else:
            data.append('white')
        
        if data:
            self.handler.newcategory(data[0], data[1], data[2])
            self.top.destroy()
            self.updatelists()

    def submit_newtask(self, event):
        '''creates a new task with dialogue entries
taskname, taskcat, taskpoints, taskbonus, taskpos'''
        data = []
        if self.allentries[0].get() != '':
            data.append(self.allentries[0].get())
        else:
            data.append('new task')
        if self.allentries[1].get() != '':
            data.append(self.allentries[1].get())
        else:
            data.append('Uncategorised')
        if self.allentries[2].get() != '':
            data.append(int(self.allentries[2].get()))
        else:
            data.append(1)
        if self.allentries[3].get() != '':
            data.append(int(self.allentries[3].get()))
        else:
            data.append(0)
        if self.allentries[4].get() != '':
            data.append(self.allentries[4].get())
        else:
            data.append(len(self.handler.categories[data[1]].contents) + 1)
        
        if data:
            self.handler.newtask(data[0], data[1], data[2], data[3], data[4])
            self.top.destroy()
            self.updatelists()
            
        
class HabitsHandler():
    def __init__(self):
        self.categories = {} ##creates a blank dictionary to contain categories
        self.newcategory('Uncategorised', 1, 'white')
        self.tasks = {}  ##creates a blank dictionary to contain all tasks
        self.currentdate = datetime.date.today()

    def newcategory(self, catname, catpos, catcolour):
        self.categories[catname] = Category(catname, catpos, catcolour)
        for e in self.categories:
            if e == catname:
                pass
            elif self.categories[e].pos >= self.categories[catname].pos:
                self.categories[e].pos += 1
                          
    def newtask(self, taskname, taskcat, taskpoints, taskbonus, taskpos):
        self.tasks[taskname] = Task(taskname, taskcat, taskpoints, taskbonus, taskpos)
        self.categories[taskcat].contents.insert(taskpos, taskname)
        
    def delcat(self, cat):
        '''Deletes a Category from the categories dictionary. All tasks within
the category are deleted'''
        for e in self.categories[cat].contents:
            tasks[e].deltask()
        del self.categories[cat]

    def deltask(self, task):
        '''deletes a task from its category contents list, moves the position of
all remaining tasks in that category up by one, and deletes the Task from the task
dictionary'''
        self.tasks[task].category.contents.remove(task)
        for e in self.tasks[task].category.contents:
            self.tasks[e].pos -= 1
        del self.tasks[task]

    def changecat(self, task, newcat, newpos):
        '''moves a task to a different category'''
        self.tasks[task].category.contents.remove(task)
        self.tasks[task].category = newcat
        self.categories[newcat].contents.insert(newpos, task)

    def setdate(self):
        isValid = False
        while not isValid:
            userdate = (input("date (dd/mm/yyyy): "))
            try: # strptime throws an exception if the input doesn't match the pattern
                d = datetime.datetime.strptime(userdate, "%d/%m/%Y").date()
                isValid=True
            except:
                print ("Incorrect format. Try again. (dd/mm/yyyy)\n")
        self.currentdate = d
    
class Category(object):
    '''A category has a name,which will be displayed as a heading.
    It contains a dictionary of tasks, indexed by id.
    It has a position (1-n) in an ordered list of categories.
    It has a colour, indicating the background colour of the heading.
    It has a row, indicating its display row.
    It has an id, which is a unique identifier, used as an index.'''
    def __init__(self, name, pos, colour):
        self.name = name
        self.contents = []
        self.pos = pos
        self.colour = colour
        self.score = {}

    def __repr__(self):
        return "Category("+self.name+", "+str(self.pos)+", "+self.colour+")"


class Task(object):
    def __init__(self, name, category, points, bonus, pos):
        self.name = name
        self.category = category
        self.points = points
        self.bonus = bonus
        self.pos = pos
        self.score = {}

    def __repr__(self):
        return "Task("+self.name+", "+self.category+", "+str(self.points)+", "+str(self.pos)+")"

    def taskcolumn(self):
        return categories[self.category].column

    def taskrow(self):
        return categories[self.category].row + self.pos



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
        

                       

if __name__ == "__main__":
    app = HabitsGui(None)
    app.title("It's going to be a great day!")
    app.mainloop()




            


