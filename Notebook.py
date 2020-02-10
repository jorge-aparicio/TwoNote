import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import BinaryTree as btree


class Notebook:
    def __init__(self, string, win):
        self.sidebar = win
        self.NotebookName = string
        #self.tree = btree.BinaryTree()
        self.pages = []
        self.buttons = []
        self.boolean = True
        self.pressed = False

        self.currentButton = None

    def add(self, pagename):
        #self.tree.insert(page)
        self.pages.append(pagename)

    def list_pages(self):
        if (len(self.pages) == 0):
            print("[]")

        else:
            for i in range(len(self.pages)):
                print(self.pages[i])

    def add_notebook_gui(self, layout, name):
        list_box = Gtk.ListBox()
        list_box.set_name('grey')
        list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        #list_box.set_activate_on_single_click(False)
        layout.insert_page(list_box, Gtk.Label(name), -1)
        layout.show_all()

    ##makes newly made notebook tab to current and returns listbox(page)
    def set_current_section(self, layout):
        layout.set_current_page(-1)
        current = layout.get_current_page()
        currentpage = layout.get_nth_page(current)
        return currentpage

    def add_page_gui(self, page, page_name, notebook_name):
        row = Gtk.ListBoxRow()
        row.set_name('header')
        self.name = page_name
        toggleButton = PageButton(notebook_name, page_name)
        #toggleButton.set_name('turquoise')
        toggleButton.connect("pressed", self.open_page, self)
        self.buttons.append(toggleButton)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        box.set_name('header')
        row.add(box)
        box.pack_start(toggleButton, True, True, 0)
        page.add(row)


    def get_current_page(self, layout):
        return layout.get_nth_page(layout.get_current_page())

    def set_name(self, name):
        self.NotebookName = name

    def get_name(self):
        return self.NotebookName

    def get_Children(self):
        return self.pages

    def get_child_at_index(self, num):
        return self.pages[num]

    def set_page_name(self, previous_name, new_name):
        for i in range(len(self.pages)):
            if (self.pages[i] == previous_name):
                widget = self.buttons[i]
                widget.set_label(new_name)
                print('in here')
                self.pages[i] = new_name

    def contains_page(self, name):
        for i in range(len(self.pages)):
            if(self.pages[i] == name):
                return True

        return False

    def save_current_page(self, notebook, buff):
        button = notebook.sidebar.active_button
        name = button.get_label()
        prev_file = open(name, 'w+')
        start, end = buff.get_bounds()
        buff_content = buff.get_text(start, end, True)
        prev_file.write(buff_content)

    def open_page(signal, button, notebook):
        notebook.currentButton = button
        notebook.sidebar.text_view.reset()
        notebook.sidebar.previous_button = notebook.sidebar.active_button
        if(notebook.sidebar.previous_button != None):
            prev_name = notebook.sidebar.previous_button.get_page_name()
            notebook.sidebar.save_current_page(prev_name)
            notebook.sidebar.previous_button.set_active(False)

        name = button.get_page_name()
        notebook.sidebar.load_current_page(name)
        notebook.sidebar.active_button = button
        notebook.boolean = False


class PageButton(Gtk.ToggleButton):
    def __init__(self, notebookname, page_name):
        Gtk.ToggleButton.__init__(self, label=page_name)
        self.notebook_name = notebookname
        self.pagename = page_name


    def get_page_name(self):
        tmp = self.get_label()
        return self.notebook_name + "_" + tmp

    def set_page_name(self, name):
        self.pagename = name




