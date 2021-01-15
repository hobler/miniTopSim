import tkinter.tix as tix

from mini_topsim.gui_13 import *


tk_root = None
tk_notebook = None
tabnames = []
tabs = []
gui_classes = []


class GuiNew(Gui):
    """
    This class represents one Page of the GUI for reading, changing and writing purposes.

    It extends the Gui class from Aufgabe 13 (gui_13.py) and overwrites the init to modify it for use in the notebook.
    The input is read from the parameters.db file.
    """
    def __init__(self,maintk,frame,section,parameter_file,button_file,cfg_file,initial_file):
        """
        This function sets all needed configurations of one Page of the Notebook.

        Attributes
        ----------
        maintk : the main tkinter link
        frame : the tkinter frame of the page which is reserved for this section
        section : the section of this notebook page
        parameter_file : path to the parameter file
        button_file : path to the button file
        cfg_file : path to the config file
        initial_file : path to the initial values file
        """
        self.root = frame
        self.maintk = maintk

        self.root.protocol = maintk.protocol
        self.root.title = maintk.title
        self.root.geometry = maintk.geometry
        self.maintk.protocol('WM_DELETE_WINDOW', self.exit_window)

        # GUI13
        self.section = section
        self.parameter_file = parameter_file
        self.button_file = button_file
        self.cfg_file = cfg_file
        self.data = self.get_data()
        if initial_file is not None:
            cp = configparser.ConfigParser()
            cp.optionxform = str
            cp.read(initial_file)
            for key in cp[self.section]:
                val = eval(cp[self.section][key])
                self.data[key][0] = val

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
        tooltip = tix.Balloon(self.root)
        tooltip.subwidget('label').forget()
        tooltip.message.config(bg="gray95",fg="black")
        for subwidgets in tooltip.subwidgets_all():
            subwidgets.configure(bg='gray95')
        for entry in self.entries:
            tooltip.bind_widget(self.entries[entry]['entry'],balloonmsg=self.data[entry][2])

        self.root.bind("<<NotebookTabChanged>>",self.on_tab_switch)

    def exit_window(self):
        """
        This function will be called when you try to leave the GUI by the 'X'.
    
        You will be asked for saving it.
        """
        answer = False
        success = True
        answer = messagebox.askyesno('Create Config file?', 'Do you want '\
                                         'to save the parameters?')
        if answer:
            success = self.save()
        if success:
            self.close()

    def close(self):
        """
        This function closes the GUI.
        """
        self.maintk.destroy()

    def on_tab_switch(self):
        """
        This function resizes the gui to the size of the new tab.
        """
        screen_width = self.maintk.winfo_screenwidth()
        screen_height = self.maintk.winfo_screenheight()
        window_width = self.maintk.winfo_width()
        gui_width = 500
        if window_width < gui_width:
            window_width = gui_width
        gui_height = 100 + 30 * len(self.data)
        if gui_width > screen_width:
            gui_width = screen_width
        if gui_height > screen_height:
            gui_height = screen_height
        self.maintk.geometry('{}x{}'.format(window_width, gui_height))

    def save(self):
        """
        This function saves the data in a config file.

        Therefore a filedialog is opened to help you to get the right
        directory.
        """
        is_invalid = False
        for c in gui_classes:
            is_invalid |= (not c.check_data())
        if not is_invalid:
            cp = configparser.ConfigParser()
            cp.optionxform = str
            file_name = filedialog.asksaveasfilename(
                initialdir=self.cfg_file,
                title='Save config', filetypes=(('cfg-files', '*.cfg'),
                ('all files', '*.*')),
                defaultextension='.cfg',
                initialfile='beispiel2.cfg')
            for guis in gui_classes:
                cp.add_section(guis.section)
                for key, value in guis.data.items():
                    if type(value[0]) is str:
                        cp.set(guis.section, key, "'"+str(value[0]) +"'")
                    else:
                        cp.set(guis.section, key, str(value[0]))
            if file_name:
                with open(file_name, 'w') as file:
                    cp.write(file)
                messagebox.showinfo('Save', 'Save of config successfully!')
                return True
            else:
                return False


def notebook_tab_changed(event):
    '''
    Determines which Tab was switched to and triggers the event there.
    '''
    i = tk_notebook.index(tk_notebook.select())
    gui_classes[i].on_tab_switch()


def main():
    global tk_root
    global tk_notebook
    tk_root = tix.Tk()
    tk_notebook = ttk.Notebook(tk_root)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_parameter_file = os.path.join(current_dir, 'parameters.db')
    path_to_button_file = os.path.join(current_dir, 'info.png')
    parent_dir = os.path.dirname(current_dir)
    path_to_cfg_file = os.path.join(parent_dir, 'work', 'Aufgabe14_gui')
    path_to_init_file = None
    if not os.path.exists(path_to_parameter_file):
        print('File parameters.db cannot be found in directory {}'.format(
                                                    path_to_parameter_file))
        sys.exit()
    if not os.path.exists(path_to_button_file):
        print('File info.png cannot be found in directory {}'.format(
                                                    path_to_button_file))
        sys.exit()

    if len(sys.argv) == 2:
        path_to_init_file = os.path.join(parent_dir,sys.argv[1])
        if not os.path.exists(path_to_init_file):
            print('File *.cfg cannot be found in directory {}'.format(
                path_to_init_file))
            sys.exit()

    cp = configparser.ConfigParser()
    cp.optionxform = str
    cp.read(path_to_parameter_file)
    tabnames.extend(cp.sections())
    print(tabnames)

    for i in range(6):
        tabs.append(ttk.Frame(tk_notebook))
        tk_notebook.add(tabs[i], text=tabnames[i])
        gui_classes.append(GuiNew(tk_root, tabs[i], tabnames[i], path_to_parameter_file, path_to_button_file, path_to_cfg_file,path_to_init_file))

    tk_notebook.bind("<<NotebookTabChanged>>",notebook_tab_changed)
    tk_notebook.pack(expand=1, fill="both")
    tk_root.title('MiniTopSim-Project')
    tk_root.mainloop()

if __name__ == "__main__":
    main()