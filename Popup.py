import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PopUp(Gtk.Dialog):

    def __init__(self, parent, boolean, boolean2):
        
        #boolean2 takes care of initial popup
        if (boolean == True):
            name = "New Page"

        else:
            name = "New NoteBook"

        Gtk.Dialog.__init__(self, name, parent, modal=True)
        if(boolean2):
            self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        else:
            self.add_buttons("Cancel", Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_default_size(200, 100)
        self.set_border_width(30)
        self.set_name('grey')

        area = self.get_content_area()

        if (boolean):
            self.entry = Gtk.Entry()
            self.entry.set_text("Page Name")
            self.entry.set_max_length(20)
            area.add(self.entry)

        else:
            self.entry = Gtk.Entry()
            self.entry.set_text("Notebook Name")
            self.entry.set_max_length(13)
            self.entry2 = Gtk.Entry()
            self.entry2.set_text("First Page")
            self.entry2.set_max_length(20)
            area.add(self.entry)
            area.add(self.entry2)

        self.show_all()


class Rename(Gtk.Dialog):
    def __init__(self, parent, notebook_name, page_name):
        Gtk.Dialog.__init__(self, "Rename", parent, destroy_with_parent=True)
        self.set_name('grey')
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(200, 100)
        self.set_border_width(30)

        area = self.get_content_area()

        # content
        self.notebook = Gtk.Notebook()
        self.entry_notebook = Gtk.Entry()
        self.entry_notebook.set_text(notebook_name)
        self.entry_notebook.set_max_length(13)
        self.notebook.insert_page(self.entry_notebook, Gtk.Label("Notebook"), -1)

        self.entry_page = Gtk.Entry()
        self.entry_page.set_text(page_name)
        self.entry_page.set_max_length(20)
        self.notebook.insert_page(self.entry_page, Gtk.Label("Page"), -1)

        area.add(self.notebook)
        area.show_all()


class Delete(Gtk.Dialog):
    def __init__(self, parent, notebook, name, pagename):

        Gtk.Dialog.__init__(self, "Delete", parent, modal=True)
        self.set_name('grey')
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(300, 225)
        self.set_border_width(60)
        self.set_resizable(True)

        area = self.get_content_area()

        # content
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(60)

        self.check_buttons = []

        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        label = Gtk.Label(name)
        self.button = GuiButton(name)
        self.check_buttons.append(self.button)

        self.box1.pack_start(label, True, True, 0)
        self.box2.pack_start(self.button, True, True, 0)

        label = Gtk.Label(pagename)
        self.box1.pack_start(label, True, True, 0)

        self.button = GuiButton(label)
        self.check_buttons.append(self.button)
        if (label.get_text() == pagename):
            self.button.set_active(True)
            self.box2.pack_start(self.button, True, True, 0)

        label = Gtk.Label('Deleting Notebook Will Delete Pages as Well.')
        self.grid.attach(self.box1, 2, 2, 2, 2)
        self.grid.attach_next_to(self.box2, self.box1, Gtk.PositionType.RIGHT, 2, 2)
        self.grid.attach_next_to(label, self.box2, Gtk.PositionType.BOTTOM, 2, 2)
        self.grid.show_all()

        area.add(self.grid)
        area.show_all()


class Duplicate(Gtk.Dialog):
    def __init__(self, parent, boolean):
        Gtk.Dialog.__init__(self, "Duplicate Found", parent, modal=True)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_name('grey')
        self.set_default_size(200, 100)
        self.set_border_width(30)

        area = self.get_content_area()

        name = None
        if (boolean):
            name = "Page cannot be duplicated."

        else:
            name = "Notebook cannot be duplicated."

        self.label = Gtk.Label(name)

        area.add(self.label)

        area.show_all()

class Welcome(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Welcome", parent, modal=True)
        self.set_default_size(600,200)
        self.set_border_width(30)
        self.set_name('grey')

        area = self.get_content_area()
        
        label = Gtk.Label("Project TwoNote")
        label.set_name('label')
        label2 = Gtk.Label("Version 0.5")
        label2.set_name('label2')
        label3 = Gtk.Label("September 2018")
        label3.set_name('label2')
        area.add(label)
        area.add(label2)
        area.add(label3)

        area.show_all()

class GuiButton(Gtk.CheckButton):
    def __init__ (self, pagename):
        Gtk.CheckButton.__init__(self)
        self.name = pagename
