'''Dictionaries containing all categories (category name: Category) and all
tasks (task name: Task)'''
categories = {}
tasks = {}
    
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

    def __repr__(self):
        return "Category("+self.name+", "+str(self.pos)+", "+self.colour+")"

    def catrow(category):
        catrow = 0
        if category.pos >= 3:
            prevcat = categories[category.pos - 2]
            catrow = len(prevcat.contents) + prevcat.row + 1
        return catrow

    def delcat(self):
        '''Deletes a Category from the categories dictionary. All tasks within
the category are deleted'''
        for e in categories[self.name].contents:
            tasks[e].deltask()
        del categories[self.name]

class Task(object):
    def __init__(self, name, category, points, pos):
        self.name = name
        self.category = category
        self.points = points
        self.pos = pos
        tasks[self.name] = self.category
        categories[self.category].contents.insert(self.pos,self.name)

    def __repr__(self):
        return "Task("+self.name+", "+self.category+", "+str(self.points)+", "+str(self.pos)+")"

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
    taskcat = input("category: ") or 'a'
    defaultpos = len(categories[taskcat].contents) + 1
    taskpos = input("list position (default: end): ") or str(defaultpos)
    taskpos = int(taskpos)
    tasks[taskname] = Task(taskname, taskcat, taskpoints, taskpos)
    



print (categories)
newcategory()
newcategory()
newtask()
newtask()
newtask()
print (categories)
print (tasks)
print (categories['a'].contents)
tasks['b'].deltask()
print (categories['a'].contents)
tasks['d'].changecat('a', 2)
print (categories['a'].contents)
print (categories['aa'].contents)
categories['aa'].delcat()
print (categories)




            


