from tkinter import *
#import trial_for_import
import random

#tkinter animation implementation for one run of the simulation
#skeleton code

class ed_visualization(object):
    def __init__(self, root, height = 400, width = 900, delay = 2):
        
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




    def create_patient(self):
        radius = 5
        x0 = 35 - radius
        x1 = 35+ radius
        y0 = 200 - radius
        y1 = 200 + radius

        self.pt = self.canvas.create_oval (x0,y0,x1,y1, fill='red')
        return self.pt
        

    def move_to_reg(self):
        #coordinates of registration x = 100,200
        reg_x = 100 + random.uniform(5,20) #adding some noise to the final destinatino so that there is no overlap
        reg_y = 200 + random.uniform(5,20)
        step_x = (reg_x - 35)/100
        step_y = (reg_y - 200)/100

        for i in range (100):
            self.canvas.move(self.pt, step_x,step_y)
            self.canvas.after(self.delay)
            self.canvas.update()

    def move_to_triage(self):
        #coordinates of registration x = 100,200
        tri_x = 320 + random.uniform(5,20) #adding some noise to the final destinatino so that there is no overlap
        tri_y = 200 + random.uniform(5,20)
        pt_coords = self.canvas.coords(self.pt)
        step_x = (tri_x - pt_coords[0])/100
        step_y = (tri_y - pt_coords[1])/100

        for i in range (100):
            self.canvas.move(self.pt, step_x,step_y)
            self.canvas.after(self.delay)
            self.canvas.update()
        
    def move_to_ED(self):
        #coordinates of registration x = 100,200
        ED_x = 600 + random.uniform(10,50) #adding some noise to the final destinatino so that there is no overlap
        ED_y = 100 + random.uniform(10,50)
        pt_coords = self.canvas.coords(self.pt)
        step_x = (ED_x - pt_coords[0])/100
        step_y = (ED_y - pt_coords[1])/100

        for i in range (100):
            self.canvas.move(self.pt, step_x,step_y)
            self.canvas.after(self.delay)
            self.canvas.update()

    def move_to_ACU(self):
        #coordinates of registration x = 100,200
        ACU_x = 600 + random.uniform(5,20) #adding some noise to the final destinatino so that there is no overlap
        ACU_y = 250 + random.uniform(5,20)
        pt_coords = self.canvas.coords(self.pt)
        step_x = (ACU_x - pt_coords[0])/100
        step_y = (ACU_y - pt_coords[1])/100

        for i in range (100):
            self.canvas.move(self.pt, step_x,step_y)
            self.canvas.after(self.delay)
            self.canvas.update()

    def move_to_exit(self):
        #coordinates of registration x = 100,200
        exit_x = 800 + random.uniform(5,20) #adding some noise to the final destinatino so that there is no overlap
        exit_y = 200 + random.uniform(5,20)
        pt_coords = self.canvas.coords(self.pt)
        step_x = (exit_x - pt_coords[0])/100
        step_y = (exit_y - pt_coords[1])/100

        for i in range (100):
            self.canvas.move(self.pt, step_x,step_y)
            self.canvas.after(self.delay)
            self.canvas.update()
    
if __name__ == "__main__":
    root = Tk()
    root.geometry('900x400')
    
            
    root.mainloop()