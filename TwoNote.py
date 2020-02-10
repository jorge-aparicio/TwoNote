import gi
import Menu_Button as menu_button
import Popup as pop
import TextSet as text_set
import sidebar_menu as sidebar

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
import threading


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.Window.__init__(self, title="TwoNote")
        # size of window
        self.set_default_size(1920, 1080)
        self.header = Gtk.HeaderBar()
        self.header.set_name('NavyBlue')
        self.header.set_show_close_button(True)
        self.header.props.title = "TwoNote"
        self.set_titlebar(self.header)
        self.check = None


        # drop menu
        self.new_notebook_button = Gtk.Button.new_from_icon_name("emblem-new", 4)
        self.new_notebook_button.connect("clicked", self.new_book_clicked)


        self.header.pack_start(self.new_notebook_button)

        # buttons for toolbar
        self.button_bold = Gtk.ToggleToolButton()
        self.button_bold.set_name('yes')
        self.button_italic = Gtk.ToggleToolButton()
        self.button_underline = Gtk.ToggleToolButton()

        ## right vbox for notes
        self.vboxRight = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.vboxRight.set_name('yes')
        self.vboxRight.set_homogeneous(False)
        self.scroll_container = Gtk.ScrolledWindow()
        self.mytext = text_set.TextSet(self.button_bold, self.button_italic, self.button_underline)
        self.buff = self.mytext.get_buffer()
        self.scroll_container.add(self.mytext)
        self.vboxRight.pack_start(self.scroll_container, True, True, 0)

        # frame for right box
        self.rightFrame = Gtk.Frame()
        self.rightFrame.add(self.vboxRight)
        self.rightFrame.set_hexpand(True)
        self.rightFrame.set_vexpand(True)

        # Left Side Bar
        self.leftFrame = sidebar.SidebarWindow(self.mytext, self)

        # creates grid and adds frames
        self.grid = Gtk.Grid()
        self.grid.set_name('DodgerBlue')
        self.grid.attach(self.leftFrame, 0, 0, 1, 30)
        self.toolbar = Gtk.Toolbar()
        self.toolbar.set_name('gains')
        self.grid.attach(self.toolbar, 2, 0, 5, 1)
        self.grid.attach_next_to(self.rightFrame, self.leftFrame, Gtk.PositionType.RIGHT, 7, 30)

        self.button_bold.set_icon_name("format-text-bold-symbolic")
        self.toolbar.insert(self.button_bold, 0)

        self.button_italic.set_icon_name("format-text-italic-symbolic")
        self.toolbar.insert(self.button_italic, 1)

        self.button_underline.set_icon_name("format-text-underline-symbolic")
        self.toolbar.insert(self.button_underline, 2)

        self.button_bold.connect("toggled", self.mytext.on_button_bold_clicked)
        self.button_italic.connect("toggled", self.mytext.on_button_italics_clicked)
        self.button_underline.connect("toggled", self.mytext.on_button_underline_clicked)

        self.add(self.grid)

        # Create a box of linked items
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # says whatever we put in this box, theyre going to be together
        Gtk.StyleContext.add_class(self.box.get_style_context(), "linked")

        self.header.pack_start(self.box)

        self.connect('destroy', Gtk.main_quit)
        self.connect('delete_event', self.on_destroy)
        self.show_all()

        if (len(self.leftFrame.notebook_list) == 0):
            welcome = pop.Welcome(self)
            welcome.run()
            welcome.destroy()
            self.new_book_initial()
            '''
            self.popup = pop.PopUp(self, False, True)
            loop = True
            while(loop): 
                self.response = self.popup.run()
                if (self.response == Gtk.ResponseType.OK):
                    self.leftFrame.new_book(self.popup)
                    loop = False
            
            self.popup.destroy()
            '''


    def new_clicked(self, signal):
        self.check = True
        self.leftFrame.gui_notebook_page = self.leftFrame.notebook.get_current_page(self.leftFrame.notebook_layout)
        self.leftFrame.notebookname = self.leftFrame.notebook_layout.get_tab_label_text(self.leftFrame.gui_notebook_page)
        self.leftFrame.notebook = self.leftFrame.notebook_check(self.leftFrame.notebookname)
        self.popup = pop.PopUp(self, True, False)
        while (self.check):
            self.check = False
            self.response = self.popup.run()
            if (self.response == Gtk.ResponseType.OK):
                self.leftFrame.new_page(self.popup)
        self.popup.destroy()

    def rename(self, signal):
        self.check = True
        self.leftFrame.gui_notebook_page = self.leftFrame.notebook.get_current_page(self.leftFrame.notebook_layout)
        self.leftFrame.notebookname = self.leftFrame.notebook_layout.get_tab_label_text(self.leftFrame.gui_notebook_page)
        self.leftFrame.notebook = self.leftFrame.notebook_check(self.leftFrame.notebookname)
        
        try:
            self.leftFrame.pagename = self.leftFrame.active_button.pagename

        except AttributeError:
            return
        
        self.rename_pop = pop.Rename(self, self.leftFrame.notebookname, self.leftFrame.pagename)
        while (self.check):
            self.check = False
            self.response = self.rename_pop.run()
            if (self.response == Gtk.ResponseType.OK):
                self.leftFrame.rename(self.rename_pop)
        
        self.rename_pop.destroy()

    def delete(self, signal):
        self.leftFrame.gui_notebook_page = self.leftFrame.notebook.get_current_page(self.leftFrame.notebook_layout)
        self.leftFrame.notebookname = self.leftFrame.notebook_layout.get_tab_label_text(self.leftFrame.gui_notebook_page)
        self.leftFrame.notebook = self.leftFrame.notebook_check(self.leftFrame.notebookname)
        try:
            self.leftFrame.pagename = self.leftFrame.active_button.pagename

        except AttributeError:
            return
        self.delete_pop = pop.Delete(self, self.leftFrame.notebook, self.leftFrame.notebookname,
                                     self.leftFrame.pagename)
        self.response = self.delete_pop.run()
        if (self.response == Gtk.ResponseType.OK):
            self.leftFrame.delete(self.delete_pop)

        self.delete_pop.destroy()

    def new_book_clicked(self, signal):
        self.check = True
        self.popup = pop.PopUp(self, False, False)
        while (self.check):
            self.check = False
            self.response = self.popup.run()
            if (self.response == Gtk.ResponseType.OK):
                self.leftFrame.new_book(self.popup)
        self.popup.destroy()

    def duplicate_true(self):
        self.duplicate = pop.Duplicate(self, True)
        self.duplicate.run()
        self.duplicate.destroy()
        self.check = True

    def duplicate_false(self):
        self.duplicate2 = pop.Duplicate(self, False)
        self.duplicate2.run()
        self.duplicate2.destroy()
        self.check = True

    def on_destroy(self, widget = None, *data):
        if(self.leftFrame.active_button != None):
            name = self.leftFrame.active_button.get_page_name()
            self.leftFrame.save_current_page(name)
        self.leftFrame.save_notebook_contents()

    def new_book_initial(self):
        self.popup = pop.PopUp(self, False, True)
        loop = True
        while(loop): 
            self.response = self.popup.run()
            if (self.response == Gtk.ResponseType.OK):
                self.leftFrame.new_book(self.popup)
                loop = False
            
        self.popup.destroy()


if __name__ == '__main__':


    win = MainWindow()

    Gtk.main()
