from tkinter import *
#import trial_for_import

#tkinter animation implementation for one run of the simulation
#skeleton code

class ed_visualization(object):
    def __init__(self, root, height = 400, width = 900, delay = 0.2):
        
        #declare the variables
        self.root = root
        self.root.title('Mock ER Animation')

        self.height = height
        self.width = width
        self.delay = delay
        
        #draw the canvas
        self.canvas = Canvas(self.root, height = 400, width = 900, background='grey')
        self.canvas.pack()
        self.canvas.update()


        #draw the rectangles on the canvas that denote the rooms
        #self.canvas.create_rectangle(0,0,900,400, fill = 'white', width = 2) #biggest layout
        self.canvas.create_rectangle(30,30,870,370, fill= 'white',  width = 3) #hospital boundaries
        
        self.canvas.create_rectangle(100,150,150,250, fill= 'grey',  width = 2) #registeration desk
        reg_label = Label(root, text= "Registeration Desk", font=('Arial', 10))
        reg_label.place(x = 75, y = 275)

        self.canvas.create_rectangle(270,100,350,300, fill= 'grey',  width = 2) #triage
        tri_label = Label(root, text= "Triaging station", font=('Arial', 10))
        tri_label.place(x = 268, y = 325)  

        self.canvas.create_rectangle(500,75,700,175, fill= 'grey',  width = 2) #Normal ED
        tri_label = Label(root, text= "ED Area", font=('Arial', 10))
        tri_label.place(x = 570, y = 50)

        
        self.canvas.create_rectangle(500,225,700,325, fill= 'grey',  width = 2) #ACU
        tri_label = Label(root, text= "ACU Area", font=('Arial', 10))
        tri_label.place(x = 570, y = 330)




    def create_patient():
        #draw a circle denoting a patient

        #declare the starting position
        
        #returns one patient in a given location
        pass
    
    def update():
        #updates the visualization with every time step

        #deletes patients that should be deleted

        #draws patients that should be drawn
        
        pass

    def move_pt():
        #This will be one of the most tricky implementation
        #Might also involve implementing more helper functions depending on where to move the patient
        #Involve moving the patient from one part of the clinic to the other
        #luckily all the coordinates of the room points will be predefined

        #try to implement movement in a way so that objects collide rather than overlap each other

        #use the .after() method for continuous movement
        #use the .bbox () method to detect the boundaries of objects and do something if there is a collission
        #use the attractive and repulsive forces concept to keep the balls close to each other.


        pass
    
    
if __name__ == "__main__":
    root = Tk()
    root.geometry('900x400')
    sim = ed_visualization(root)
    root.mainloop()