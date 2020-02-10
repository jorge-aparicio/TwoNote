import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class NoteMenu(Gio.Menu):
    def __init__(self):
        Gio.Menu.__init__(self)
        self.new_item = Gio.MenuItem.new('New Page', 'win.new')
        self.new_book_item = Gio.MenuItem.new('New Notebook', 'win.new_notebook')
        self.open_item = Gio.MenuItem.new('Open', 'win.open')
        self.save_item = Gio.MenuItem.new('Save', 'win.save')
        self.save_as_item = Gio.MenuItem.new('Save as', 'win.save_as')
        self.settings_item = Gio.MenuItem.new('Preferences', 'win.settings')

        # appends items to drop down menu
        self.append_item(self.new_item)
        self.append_item(self.new_book_item)
        self.append_item(self.open_item)
        self.append_item(self.save_item)
        self.append_item(self.save_as_item)
        self.append_item(self.settings_item)


'''	
class NoteActionGroup(Gio.SimpleActionGroup):
	def __init__(self):
		Gio.SimpleActionGroup.__init__(self)
		self.new_action = Gio.SimpleAction.new("new", None)
		self.new_action.connect("activate", self.new_clicked)
		self.insert(self.new_action)
		
		self.new_book_action = Gio.SimpleAction.new("new_notebook", None)
		self.new_book_action.connect("activate", self.new_book_clicked)
		self.insert(self.new_book_action)
		
		self.open_action = Gio.SimpleAction.new("open", None)
		self.open_action.connect("activate", self.open_clicked)
		self.insert(self.open_action)
		
		self.save_action = Gio.SimpleAction.new("save", None)
		self.save_action.connect("activate", self.save_clicked)
		self.insert(self.save_action)
		
		self.save_as_action = Gio.SimpleAction.new("save_as", None)
		self.save_as_action.connect("activate", self.save_as_clicked)
		self.insert(self.save_as_action)
		
		self.settings_action = Gio.SimpleAction.new("settings", None)
		self.settings_action.connect("activate", self.settings_clicked)
		self.insert(self.settings_action)
		
		
		
	def open_clicked(self, action, none):
		menu_func.open_file(self)
	
	def new_clicked(self, action, none):
		print("new")
		
	def new_book_clicked(self, action, none):
		print("new notebook")
		
	def save_clicked(self, action, none):
		menu_func.save_file(self, self.text)
    
	def save_as_clicked(self, action, none):
		print("save as")  
    
	def settings_clicked(self, action, none):
		print("settings")	

			
'''
filename = "Untitled"


def open_file(window, widget):
    open_dialog = Gtk.FileChooserDialog("Open an existing file", window, Gtk.FileChooserAction.OPEN, (
    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    open_response = open_dialog.run()

    if open_response == Gtk.ResponseType.OK:
        filename = open_dialog.get_filename()
        text = open(filename).read()
        widget.get_buffer().set_text(text)
        open_dialog.destroy()

    elif open_response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")
        open_dialog.destroy()


def save_file(window, widget):
    savechooser = Gtk.FileChooserDialog('Save File', window, Gtk.FileChooserAction.SAVE, (
    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
    allfilter = Gtk.FileFilter()
    allfilter.set_name('All files')
    allfilter.add_pattern('*')
    savechooser.add_filter(allfilter)

    txtFilter = Gtk.FileFilter()
    txtFilter.set_name('Text file')
    txtFilter.add_pattern('*.txt')
    savechooser.add_filter(txtFilter)
    response = savechooser.run()

    if response == Gtk.ResponseType.OK:
        filename = savechooser.get_filename()
        print(filename, 'selected.')
        buf = widget.get_buffer()
        start, end = buf.get_bounds()
        text = buf.get_text(start, end, True)

        try:
            open(filename, 'w').write(text)
        except SomeError as e:
            print('Could not save %s: %s' % (filename, err))
        savechooser.destroy()

    elif response == Gtk.ResponseType.CANCEL:
        print('Closed, file not saved.')
        savechooser.destroy()
