from gui import *
import tkinter as tk
import tkinter.ttk as ttk
import sys
import os
import configparser

tabnames = ['Setup', 'Initial Conditions', 'Numerics', 'Beam', 'Physics', 'Output']

form = tk.Tk()
tabs_frame = ttk.Notebook(form)
tabs = []
gui_classes = []


#tabs.add(tab2, text="TAB2")

#label = ttk.Label(tabs[0], relief='sunken', text='PARAMETER')

#redbutton = tk.Button(tabs[0], text="Red", fg="red")
#redbutton.pack( side = tk.LEFT)


class GuiNew(Gui):
    def __init__(self,maintk,frame,section,parameter_file,button_file,cfg_file):
        print("GuiNew")
        self.root = frame
        self.maintk = maintk

        self.root.protocol = maintk.protocol
        self.root.title = maintk.title
        self.root.geometry = maintk.geometry
        #self.root.destroy = maintk.destroy
        #self.children = None
        self.root.protocol('WM_DELETE_WINDOW', self.exit_window)
        #GUI13
        self.section = section
        self.parameter_file = parameter_file
        self.button_file = button_file
        self.cfg_file = cfg_file
        self.data = self.get_data()

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        gui_width = 500
        gui_height = 100 + 30 * len(self.data)
        if gui_width > screen_width:
            gui_width = screen_width
        if gui_height > screen_height:
            gui_height = screen_height

        self.maintk.geometry('{}x{}'.format(gui_width, gui_height))
        x_position = int(screen_width/2 - gui_width/2)
        y_position = int(screen_height/2 - gui_height/2)
        self.maintk.geometry('+{}+{}'.format(x_position, y_position))
    
        self.display()
        self.root.bind("<<NotebookTabChanged>>",self.onTabSwitch)
        #self.root.pack()

    def exit_window(self):
        """
        This function will be called when you try to leave the GUI by the 'X'.
    
        If there is no unsaved work, it just will close like the 'Cancel' 
        button. If there is something new you will be asked for saving it.
        """
        
        equal = self.data_already_in_file()
        answer = False  
        success = True
        if not equal:
            messagebox.showwarning('Unsaved Data', 'The data isn\'t equal to '\
                                   'the file beispiel.cfg')
            answer = messagebox.askyesno('Create Config file?', 'Do you want '\
                                         'to save the parameters?')
                
        if answer:
            success = self.save()
        if success:
            self.close()
            
    def close(self):
        self.maintk.destroy()
        
    def onTabSwitch(self):
        print("SWITCHUP")
        screen_width = self.maintk.winfo_screenwidth()
        screen_height = self.maintk.winfo_screenheight()
        window_width = self.maintk.winfo_width()
        gui_width = 500
        if(window_width < gui_width):
            window_width = gui_width
        gui_height = 100 + 30 * len(self.data)
        if gui_width > screen_width:
            gui_width = screen_width
        if gui_height > screen_height:
            gui_height = screen_height
        print(window_width)
        self.maintk.geometry('{}x{}'.format(window_width, gui_height))
        x_position = int(screen_width/2 - gui_width/2)
        y_position = int(screen_height/2 - gui_height/2)
        #self.maintk.geometry('+{}+{}'.format(x_position, y_position))
    def save(self):
        print("HAAAAA")
        is_invalid = False
        for c in gui_classes:
            is_invalid |= (not c.check_data())
            print(is_invalid)
        if not is_invalid:
            print("KKKKKKKKKKKKKK")
            all_data = {}
            for guis in gui_classes:
                all_data.update(guis.data)
            config = CreateConfigFile(all_data)
            success = config.save_file(tabnames, self.cfg_file)
            if success:
                messagebox.showinfo('Save', 'Save of config successfully!')
                return True
            

def test(event):
    print(event)
    i = tabs_frame.index(tabs_frame.select())
    print(i)
    gui_classes[i].onTabSwitch()
        

for i in range(6):
    tabs.append(ttk.Frame(tabs_frame))
    tabs_frame.add(tabs[i], text=tabnames[i])
    gui_classes.append(GuiNew(form, tabs[i], tabnames[i], "../../../../parameters.db", "info.png", "beispiel.cfg"))

#a = GuiNew(form,tabs[0],tabnames[0],"parameters.db","info.png","beispiel.cfg")
#a.start()
tabs_frame.bind("<<NotebookTabChanged>>",test)
tabs_frame.pack(expand=1, fill="both")
form.mainloop()
#Gui(tabnames[0],"parameters.db","info.png","beispiel.cfg",)
