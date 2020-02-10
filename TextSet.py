import gi

gi.require_version('Gtk', '3.0')
import threading, time
from gi.repository import Gtk, Pango


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
        self.interval = 1
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):

        while True:
            bounds = self.tb.get_selection_bounds()
            time.sleep(self.interval)
            if (len(bounds) != 0):
                start, end = bounds
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
                    self.reset()
    def reset(self):
        self.button_underline.set_active(False)
        self.button_italic.set_active(False)
        self.button_bold.set_active(False)

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
        elif self.taglist_bold and self.taglist_italics:
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
                self.remove_tag_by_name("Italic", self.get_iter_position(), iter)

        if self.taglist_underline:
            print("step 1")
            if self.underline_check:
                print("step2")
                self.apply_tag_by_name('Underline', self.get_iter_position(), iter)

            else:
                self.remove_tag_by_name("Underline", self.get_iter_position(), iter)

        if self.taglist_bold:
            if self.bold_check:
                self.apply_tag_by_name('Bold', self.get_iter_position(), iter)
            else:
                self.remove_tag_by_name("Bold", self.get_iter_position(), iter)
