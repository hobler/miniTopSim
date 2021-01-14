from work.Aufgabe14_gui.gui_13 import *
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
    def __init__(self,maintk,frame,section,parameter_file,button_file,cfg_file,initial_file):
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
        if initial_file is not None:
            print(initial_file)
            cp = configparser.ConfigParser()
            cp.optionxform = str
            cp.read(initial_file)
            open(initial_file, 'r')
            print(str(cp))
            print("INITS:")
            print(cp.sections())
            for key in cp[self.section]:
                if (cp[self.section][key]).replace(".", "").replace("-","").replace("True","0").replace("False", "0").isnumeric():
                    val = eval(cp[self.section][key])
                else:
                    val = cp[self.section][key]
                print(self.data[key])
                self.data[key][0] = val
                print(key + " | " + str(val))

            print("----------------------")
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
            print("Saving")
            cp = configparser.ConfigParser()
            cp.optionxform = str
            file_name = filedialog.asksaveasfilename(initialdir=self.cfg_file,
                                                     title='Save config', filetypes=(('cfg-files', '*.cfg'),
                                                                                     ('all files', '*.*')),
                                                     defaultextension='.cfg',
                                                     initialfile='beispiel2.cfg')
            for guis in gui_classes:
                cp.add_section(guis.section)
                for key, value in guis.data.items():
                    print(value)
                    cp.set(guis.section, key, str(value[0]))
            if file_name:
                with open(file_name, 'w') as file:
                    cp.write(file)
                messagebox.showinfo('Save', 'Save of config successfully!')
                return True
            else:
                return False

            

def test(event):
    print(event)
    i = tabs_frame.index(tabs_frame.select())
    print(i)
    gui_classes[i].onTabSwitch()

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_parameter_file = os.path.join(current_dir, 'parameters.db')
path_to_button_file = os.path.join(current_dir, 'info.png')
parent_dir = os.path.dirname(current_dir)
path_to_cfg_file = os.path.join(parent_dir, 'work', 'Aufgabe14_gui')
path_to_init_file = None
if(len(sys.argv) == 2):
    print(sys.argv)
    print(current_dir)
    path_to_init_file = os.path.join(parent_dir,sys.argv[1])
for i in range(6):
    tabs.append(ttk.Frame(tabs_frame))
    tabs_frame.add(tabs[i], text=tabnames[i])
    gui_classes.append(GuiNew(form, tabs[i], tabnames[i], path_to_parameter_file, path_to_button_file, path_to_cfg_file,path_to_init_file))

#a = GuiNew(form,tabs[0],tabnames[0],"parameters.db","info.png","beispiel.cfg")
#a.start()
tabs_frame.bind("<<NotebookTabChanged>>",test)
tabs_frame.pack(expand=1, fill="both")
form.mainloop()
#Gui(tabnames[0],"parameters.db","info.png","beispiel.cfg",)
