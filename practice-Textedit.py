import gi
import threading, time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GLib


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.Window.__init__(self, title="TwoNote")
        self.grid = Gtk.Grid()
        self.toolbar = Gtk.Toolbar()
        self.grid.add(self.toolbar)

        # buttons for toolbar
        self.button_bold = Gtk.ToggleToolButton()
        self.button_italic = Gtk.ToggleToolButton()
        self.button_underline = Gtk.ToggleToolButton()
        self.button_save = Gtk.ToolButton()
        self.button_open = Gtk.ToolButton()

        self.mytext = TextSet(self.button_bold, self.button_italic, self.button_underline)

        self.button_bold.set_icon_name("format-text-bold-symbolic")
        self.toolbar.insert(self.button_bold, 0)

        self.button_italic.set_icon_name("format-text-italic-symbolic")
        self.toolbar.insert(self.button_italic, 1)

        self.button_underline.set_icon_name("format-text-underline-symbolic")
        self.toolbar.insert(self.button_underline, 2)

        self.toolbar.insert(self.button_save, 3)
        self.toolbar.insert(self.button_open, 4)

        self.button_open.set_icon_name("document-open-data")
        self.button_save.set_icon_name("document-save")

        self.button_save.connect("clicked", self.save_file)
        self.button_open.connect("clicked", self.open_file)
        self.button_bold.connect("toggled", self.mytext.on_button_bold_clicked)
        self.button_italic.connect("toggled", self.mytext.on_button_italics_clicked)
        self.button_underline.connect("toggled", self.mytext.on_button_underline_clicked)

        self.grid.attach_next_to(self.mytext, self.toolbar, Gtk.PositionType.BOTTOM, 10, 30)

        self.add(self.grid)
        self.interval = 1
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):

        while True:
            self.tb = self.mytext.get_buffer()
            bounds = self.tb.get_selection_bounds()
            time.sleep(self.interval)
            if (len(bounds) != 0):
                location = self.tb.get_iter_at_mark(self.tb.get_insert())
                myTags = location.get_tags()
                if len(myTags) != 0:
                    for i in range(len(myTags)):
                        print(myTags[i].props.name)
                        if (myTags[i].props.name == "Bold"):
                            self.button_bold.set_active(True)
                        elif (myTags[i].props.name == "Italic"):
                            self.button_italic.set_active(True)
                        elif (myTags[i].props.name == "Underline"):
                            self.button_underline.set_active(True)
                else:
                    print("empty")
                    self.button_underline.set_active(False)
                    self.button_italic.set_active(False)
                    self.button_bold.set_active(False)

    filename = "Untitled"
    def open_file(self, widget):
        open_dialog = Gtk.FileChooserDialog("Open an existing file", self, Gtk.FileChooserAction.OPEN, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        open_response = open_dialog.run()

        if open_response == Gtk.ResponseType.OK:
            filename = open_dialog.get_filename()
            buf = self.mytext.get_buffer()
            des_tag_format = buf.register_deserialize_tagset()
            des_content = GLib.file_get_contents(filename)
            text = buf.deserialize(buf, des_tag_format, buf.get_start_iter(), des_content)

            self.mytext.get_buffer().set_text(text)
            open_dialog.destroy()

        elif open_response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            open_dialog.destroy()

    def save_file(self, widget):
        savechooser = Gtk.FileChooserDialog('Save File', self, Gtk.FileChooserAction.SAVE, (
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
            buf = self.mytext.get_buffer()
            start, end = buf.get_bounds()
            tag_format = buf.register_serialize_tagset()
            content = buf.serialize(buf, tag_format, start, end)

            try:
                GLib.file_set_contents(filename, content)
            except SomeError as e:
                print('Could not save %s: %s' % (filename, err))
            savechooser.destroy()

        elif response == Gtk.ResponseType.CANCEL:
            print('Closed, file not saved.')
            savechooser.destroy()


class TextSet(Gtk.TextView):
    def __init__(self, buttonBold, buttonItalic, buttonUnderline, interval=1):
        # Textview Setup
        Gtk.TextView.__init__(self)
        self.set_vexpand(True)
        self.set_indent(10)
        self.set_top_margin(90)
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.tb = TextBuffer()
        self.set_buffer(self.tb)
        # Thread setup
        self.button_bold = buttonBold
        self.button_italic = buttonItalic
        self.button_underline = buttonUnderline

    def on_button_bold_clicked(self, widget):
        state = widget.get_active()
        bounds = self.tb.get_selection_bounds()
        # highlighting
        if (len(bounds) != 0):
            start, end = bounds
            myIter = self.tb.get_iter_at_mark(self.tb.get_insert())
            myTags = myIter.get_tags()
            if (myTags == [] and state == True):
                self.tb.apply_tag_by_name("Bold", start, end)
            elif (myTags != [] and state == True):
                self.tb.apply_tag_by_name("Bold", start, end)

            else:
                for i in range(len(myTags)):
                    if (myTags[i].props.name == "Bold"):
                        self.tb.remove_tag_by_name("Bold", start, end)

        self.tb.bold_markup(widget)

    def on_button_italics_clicked(self, widget):
        state = widget.get_active()
        bounds = self.tb.get_selection_bounds()
        # highlighting
        if (len(bounds) != 0):
            start, end = bounds
            myIter = self.tb.get_iter_at_mark(self.tb.get_insert())
            myTags = myIter.get_tags()
            if (myTags == [] and state == True):
                self.tb.apply_tag_by_name("Italic", start, end)
            elif (myTags != [] and state == True):
                self.tb.apply_tag_by_name("Italic", start, end)

            else:
                for i in range(len(myTags)):
                    if (myTags[i].props.name == "Italic"):
                        self.tb.remove_tag_by_name("Italic", start, end)
        self.tb.italics_markup(widget)

    def on_button_underline_clicked(self, widget):
        state = widget.get_active()
        bounds = self.tb.get_selection_bounds()
        # highlighting
        if (len(bounds) != 0):
            start, end = bounds
            myIter = self.tb.get_iter_at_mark(self.tb.get_insert())
            myTags = myIter.get_tags()
            if (myTags == [] and state == True):
                self.tb.apply_tag_by_name("Underline", start, end)
            elif (myTags != [] and state == True):
                self.tb.apply_tag_by_name("Underline", start, end)

            else:
                for i in range(len(myTags)):
                    if (myTags[i].props.name == "Underline"):
                        self.tb.remove_tag_by_name("Underline", start, end)
        self.tb.underline_markup(widget)



    def mouse_clicked(self, window, event):
        self.button_bold.set_active(False)
        self.button_italic.set_active(False)
        self.button_underline.set_active(False)


class TextBuffer(Gtk.TextBuffer):
    def __init__(self):
        Gtk.TextBuffer.__init__(self)
        self.connect_after('insert-text', self.text_inserted)
        # A list to hold our active tags
        self.taglist_bold = []
        self.taglist_italics = []
        self.taglist_underline = []
        # Our Bold tag.
        self.tag_bold = self.create_tag("Bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.create_tag("Italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.create_tag("Underline", underline=Pango.Underline.SINGLE)

    def get_iter_position(self):
        return self.get_iter_at_mark(self.get_insert())

    def bold_markup(self, widget):
        self.bold_check = True
        ''' add "bold" to our active tags list '''
        if (widget.get_active() == True):
            if 'Bold' in self.taglist_bold:
                del self.taglist_bold[self.taglist_bold.index('Bold')]

            self.taglist_bold.append('Bold')
        else:
            self.bold_check = False

    def italics_markup(self, widget):
        self.italics_check = True
        ''' add "bold" to our active tags list '''
        if (widget.get_active() == True):

            if 'Italic' in self.taglist_italics:
                del self.taglist_italics[self.taglist_italics.index('Italic')]

            self.taglist_italics.append('Italic')

        else:
            self.italics_check = False

    def underline_markup(self, widget):

        self.underline_check = True
        ''' add "bold" to our active tags list '''
        if (widget.get_active() == True):
            if 'Underline' in self.taglist_underline:
                del self.taglist_underline[self.taglist_underline.index('Underline')]

            self.taglist_underline.append('Underline')

        else:
            self.underline_check = False

    def iter_length(self):
        if self.taglist_underline and self.tag_bold and self.taglist_italics:
            self.underline_iter_length = 0
            self.italics_iter_length = 0
        elif self.taglist_bold and self.taglist_underline:
                self.underline_iter_length = 0
        elif self.taglist_italics and self.taglist_underline:
            self.underline_iter_length = 0
        elif  self.taglist_bold and self.taglist_italics:
            self.italics_iter_length = 0


    def text_inserted(self, buffer, iter, text, length):
        # A text was inserted in the buffer. If there are ny tags in self.tags_on,   apply them
        # if self.taglist_None or self.taglist_Italic or self.taglist_Underline or self.taglist_Bold:
        iter.backward_chars(length)
        if self.taglist_italics:
            if self.italics_check:
                # This sets the iter back N characters
                self.apply_tag_by_name('Italic', self.get_iter_position(), iter)
            else:
               self.remove_tag_by_name("Italic",self.get_iter_position(), iter)

        if self.taglist_underline:
            print("step 1")
            if self.underline_check:
                print("step2")
                self.apply_tag_by_name('Underline', self.get_iter_position(), iter)

            else:
                self.remove_tag_by_name("Underline",self.get_iter_position(), iter)

        if self.taglist_bold:
            if self.bold_check:
                self.apply_tag_by_name('Bold', self.get_iter_position(), iter)
            else:
                    self.remove_tag_by_name("Bold",self.get_iter_position(), iter)

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
