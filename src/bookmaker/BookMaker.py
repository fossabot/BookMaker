#!/usr/bin/python3

import os
import shutil
import sys
import platform

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gio', '2.0')
gi.require_version('Gdk', '3.0')
# gi.require_version('Pango', '1.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, Gtk, GdkPixbuf

import about
from toc_view import TOCview
from markdown_view import MARKDOWNview
from pre_view import PREview

# The following declarations allow the application to be invoked from anywhere
# and access its database and .glade files etc. relative to its source directory.
from inspect import getsourcefile
from os.path import dirname


class Common():
    pass  # dummy class to use with getsourcefile


def where_am_i():  # use to find ancillary files e.g. .glade files
    return dirname(getsourcefile(Common))


UPSTART_LOGO = where_am_i() + '/logo.svg'

UI_MENU = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="menubar">
    <submenu>
      <attribute name="label">File</attribute>
      <section>
        <item>
          <attribute name="label">Select project folder</attribute>
          <attribute name="action">win.selectprojectfolder</attribute>
          <attribute name="accel">&lt;Ctrl&gt;O</attribute>
          <attribute name="icon">document-open</attribute>
        </item>
      </section>
      <section>
        <submenu>
          <attribute name="label">Export..</attribute>
            <section>
              <item>
                <attribute name="label">..to epub</attribute>
                <attribute name="action">win.exporttoepub</attribute>
              </item>
              <item>
                <attribute name="label">..to pdf</attribute>
                <attribute name="action">win.exporttopdf</attribute>
              </item>
            </section>
        </submenu>
      </section>
      <section>
        <item>
          <attribute name="label">Quit</attribute>
          <attribute name="action">app.quit</attribute>
          <attribute name="accel">&lt;Ctrl&gt;Q</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label">Edit</attribute>
      <section>
        <item>
          <attribute name="label">Undo</attribute>
          <attribute name="action">win.undo</attribute>
          <attribute name="accel">&lt;Ctrl&gt;Z</attribute>
          <attribute name="icon">edit-undo</attribute>
        </item>
        <item>
          <attribute name="label">Redo</attribute>
          <attribute name="action">win.redo</attribute>
          <attribute name="accel">&lt;Ctrl&gt;Y</attribute>
           <attribute name="icon">edit-redo</attribute>
       </item>
      </section>
      <section>
        <item>
          <attribute name="label">Copy</attribute>
          <attribute name="action">win.copy</attribute>
          <attribute name="accel">&lt;Ctrl&gt;C</attribute>
          <attribute name="icon">edit-copy</attribute>
        </item>
        <item>
          <attribute name="label">Cut</attribute>
          <attribute name="action">win.cut</attribute>
          <attribute name="accel">&lt;Ctrl&gt;X</attribute>
          <attribute name="icon">edit-cut</attribute>
        </item>
        <item>
          <attribute name="label">Paste</attribute>
          <attribute name="action">win.paste</attribute>
          <attribute name="accel">&lt;Ctrl&gt;V</attribute>
          <attribute name="icon">edit-paste</attribute>
        </item>
      </section>
      <section>      
        <submenu>
          <attribute name="label">Format</attribute>
            <section>
              <item>
                <attribute name="label">Bold</attribute>
                <attribute name="action">win.bold</attribute>
                <attribute name="icon">format-text-bold</attribute>
              </item>
              <item>
                <attribute name="label">Italic</attribute>
                <attribute name="action">win.italic</attribute>
                <attribute name="icon">format-text-italic</attribute>
              </item>
              <item>
                <attribute name="label">Underline</attribute>
                <attribute name="action">win.uline</attribute>
                <attribute name="icon">format-text-underline</attribute>
              </item>
            </section>
        </submenu>
      </section>
      <section>      
        <submenu>
          <attribute name="label">Insert</attribute>
            <section>
              <item>
                <attribute name="label">Image</attribute>
                <attribute name="action">win.insert-image</attribute>
                <attribute name="icon">insert-image</attribute>
              </item>
            </section>
        </submenu>
      </section>
    </submenu>
    <submenu>
      <attribute name="label">Help</attribute>
      <section>
        <item>
          <attribute name="label">About</attribute>
          <attribute name="action">win.about</attribute>
          <attribute name="icon">help-about</attribute>
          <attribute name="accel">F1</attribute>
        </item>
      </section>
    </submenu>
  </menu>
</interface>
"""
UI_TOOLBAR = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <object class='GtkToolbar' id='toolbar'>
    <property name='visible'>True</property>
    <property name='can_focus'>False</property>
    <child>
      <object class='GtkToolButton' id='toolbutton_selectprojectfolder'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Select project folder</property>
        <property name='action_name'>win.selectprojectfolder</property>
        <property name='icon_name'>document-open</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
     <child>
      <object class='GtkSeparatorToolItem'>
        <property name='draw'>True</property>
      </object>
      <packing>
        <property name='expand'>False</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_undo'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Undo</property>
        <property name='action_name'>win.undo</property>
        <property name='icon_name'>edit-undo</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_redo'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Redo</property>
        <property name='action_name'>win.redo</property>
        <property name='icon_name'>edit-redo</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
     <child>
      <object class='GtkSeparatorToolItem'>
        <property name='draw'>True</property>
      </object>
      <packing>
        <property name='expand'>False</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_cut'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Cut</property>
        <property name='action_name'>win.cut</property>
        <property name='icon_name'>edit-cut</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_copy'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Copy</property>
        <property name='action_name'>win.copy</property>
        <property name='icon_name'>edit-copy</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_paste'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Paste</property>
        <property name='action_name'>win.paste</property>
        <property name='icon_name'>edit-paste</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkSeparatorToolItem'>
        <property name='draw'>True</property>
      </object>
      <packing>
        <property name='expand'>False</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_bold'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Bold</property>
        <property name='action_name'>win.bold</property>
        <property name='icon_name'>format-text-bold</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_italic'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Italic</property>
        <property name='action_name'>win.italic</property>
        <property name='icon_name'>format-text-italic</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_uline'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Underline</property>
        <property name='action_name'>win.uline</property>
        <property name='icon_name'>format-text-underline</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkSeparatorToolItem'>
        <property name='draw'>True</property>
      </object>
      <packing>
        <property name='expand'>False</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_python'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Selection as Python code</property>
        <property name='action_name'>win.as_python</property>
        <property name='icon_name'>icon_py</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_text'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Selection as plain text</property>
        <property name='action_name'>win.as_text</property>
        <property name='icon_name'>icon_txt</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkSeparatorToolItem'>
        <property name='draw'>True</property>
      </object>
      <packing>
        <property name='expand'>False</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_image'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Insert image</property>
        <property name='action_name'>win.insert-image</property>
        <property name='icon_name'>insert-image</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
     <child>
      <object class='GtkSeparatorToolItem'>
        <property name='draw'>False</property>
      </object>
      <packing>
        <property name='expand'>True</property>
      </packing>
    </child>
    <child>
      <object class='GtkToolButton' id='toolbutton_quit'>
        <property name='visible'>True</property>
        <property name='can_focus'>False</property>
        <property name='tooltip_text' translatable='yes'>Quit</property>
        <property name='action_name'>app.quit</property>
        <property name='icon_name'>application-exit</property>
      </object>
      <packing>
        <property name='expand'>False</property>
        <property name='homogeneous'>True</property>
      </packing>
    </child>
  </object>
</interface>
"""
# The toc/markdown/preview subwindows are inserted below the toolbar by
# Python code, using an HBox.
UI_STATUSBAR = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <object class="GtkStatusbar" id="statusbar">
    <property name="visible">True</property>
    <property name="can_focus">True</property>
  </object>
</interface>
"""


class AppWindow(Gtk.ApplicationWindow):

    def on_destroy(self, widget):
        print("Caught destroy event")
        print("i.e. Main window destroyed; quit application")
        self.app.quit()

    def on_delete_event(self, widget, *data):
        print("Caught main window delete event")
        print("i.e. Main window close button clicked; ask user what to do")

        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Do you really want to close?")
        dialog.format_secondary_text(
            "(Your current changes will be saved automatically)")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            print("QUESTION dialog closed by clicking YES button")
            print("i.e. user really does want to close")
            print("     so save changes as promised and return False")
        else:
            if response == Gtk.ResponseType.NO:
                print("QUESTION dialog closed by clicking NO")
            elif response == Gtk.ResponseType.DELETE_EVENT:
                print("QUESTION dialog closed by clicking X")
            print("i.e. user didn't really want to close; return True")
            return True  # means we have dealt with signal; no action required

        self.MV.save_if_dirty(self.TV.project_directory, self.TV.filename_tail)
        return False  # means go ahead with the Gtk.main_quit action

    def __init__(self, app, **kwargs):
        Gtk.Window.__init__(self, application=app)
        # super().__init__(app, **kwargs)
        self.app = app
        self.connect('destroy', self.on_destroy)
        self.connect('delete-event', self.on_delete_event)

        print(f'This is {about.NAME} version {about.VERSION} using Python {platform.python_version()}')

        self.vbox = Gtk.VBox()

        self.builder = Gtk.Builder()
        self.builder.add_from_string(UI_MENU)
        app.set_menubar(self.builder.get_object("menubar"))

        self.builder.add_from_string(UI_TOOLBAR)
        # self.builder.connect_signals(self)
        self.vbox.add(self.builder.get_object("toolbar"))

        hbox = Gtk.HBox()
        self.vbox.add(hbox)  # add the hbox which will contain the toc/markdown/preview

        # Get the GdkScreen associated with the ApplicationWindow
        # Get the associated GdkDisplay (group of screens on one workstation)
        # Get the particular GdkMonitor within the GdkDisplay
        # Get the GdkMonitor's geometry (usable display rectangle)
        rect = self.get_screen().get_display().get_monitor(0).get_geometry()
        rect.height -= 28  # allow for panel height (approx)
        print(f"Size = {rect.width} x {rect.height}")

        # Let's size the working area (hbox) to 0.75 of the available desktop
        hbox.set_size_request(rect.width * 0.75, rect.height * 0.75)

        # Now size the subwindows within their hbox. The total width of the
        # three subwindows must add up to the width of the hbox.

        # Size the Table of Contents
        toc = TOCview(self)  # TOCview needs transient base for dialogs
        toc.set_size_request(rect.width * 0.15, -1)

        self.TV = toc
        hbox.add(toc)

        # Size the Markdown editing area
        self.MV = MARKDOWNview(toc)  # needs to reference toc for project directory/file details
        self.MV.set_size_request(rect.width * 0.25, -1)
        hbox.add(self.MV)

        self.TV.set_MV(self.MV)

        # Size the preview display area
        self.PV = PREview(toc)
        self.PV.set_size_request(rect.width * 0.35, -1)
        hbox.add(self.PV)

        # Now add the statusbar
        self.builder.add_from_string(UI_STATUSBAR)
        self.builder.connect_signals(self)

        self.statusbar = self.builder.get_object("statusbar")

        # its context_id - not shown in the UI but needed to uniquely identify the source of a message
        self.context_id = self.statusbar.get_context_id("example")

        self.vbox.add(self.statusbar)

        # we push a message onto the statusbar's stack
        self.statusbar.push(
            self.context_id, "Waiting for you to do something...")

        self.add(self.vbox)  # add the whole vbox to the window

        self.MV.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        #         self.PV.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        self.MV.set_PV(self.PV)
        self.MV.syncscroll_instance = None
        # SyncScroll(self.MV, self.PV)

        # Set up the actions to make the menu/toolbar "live" before
        # we populate the toc/markdown/preview.

        # The "win.selectprojectfolder" action
        selectprojectfolder_action = Gio.SimpleAction.new("selectprojectfolder", None)
        selectprojectfolder_action.connect("activate", self.on_selectprojectfolder_clicked)
        self.add_action(selectprojectfolder_action)

        # The "win.exporttoepub" action
        exporttoepub_action = Gio.SimpleAction.new("exporttoepub", None)
        exporttoepub_action.connect("activate", self.on_exporttoepub_clicked)
        self.add_action(exporttoepub_action)

        # The "win.exporttopdf" action  # experimental only
        # Commented out so action not defined -> greyed out in menu
        exporttopdf_action = Gio.SimpleAction.new("exporttopdf", None)
        exporttopdf_action.connect("activate", self.on_exporttopdf_clicked)
        self.add_action(exporttopdf_action)

        # The "win.undo/redo" actions
        undo_action = Gio.SimpleAction.new("undo", None)
        undo_action.connect("activate", self.on_undo_clicked)
        self.add_action(undo_action)

        redo_action = Gio.SimpleAction.new("redo", None)
        redo_action.connect("activate", self.on_redo_clicked)
        self.add_action(redo_action)

        # The "win.copy/paste/cut" actions
        copy_action = Gio.SimpleAction.new("copy", None)
        copy_action.connect("activate", self.on_copy_clicked)
        self.add_action(copy_action)

        paste_action = Gio.SimpleAction.new("paste", None)
        paste_action.connect("activate", self.on_paste_clicked)
        self.add_action(paste_action)

        cut_action = Gio.SimpleAction.new("cut", None)
        cut_action.connect("activate", self.on_cut_clicked)
        self.add_action(cut_action)

        # The "win.bold/italic/underline" actions
        bold_action = Gio.SimpleAction.new("bold", None)
        bold_action.connect("activate", self.on_bold_clicked)
        self.add_action(bold_action)

        italic_action = Gio.SimpleAction.new("italic", None)
        italic_action.connect("activate", self.on_italic_clicked)
        self.add_action(italic_action)

        underline_action = Gio.SimpleAction.new("uline", None)
        underline_action.connect("activate", self.on_uline_clicked)
        self.add_action(underline_action)

        # The "win.as_python/as_text" actions
        # The relevant icons for the toolbar are designed externally
        # and placed in ~/.icons/icon_py.png and ~/.icons/icon_text.png
        as_python_action = Gio.SimpleAction.new("as_python", None)
        as_python_action.connect("activate", self.on_as_python_clicked)
        self.add_action(as_python_action)

        as_text_action = Gio.SimpleAction.new("as_text", None)
        as_text_action.connect("activate", self.on_as_text_clicked)
        self.add_action(as_text_action)

        # The "win.insert-image" action
        image_action = Gio.SimpleAction.new("insert-image", None)
        image_action.connect("activate", self.on_insert_image_clicked)
        self.add_action(image_action)

        # The "win.about" action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_clicked)
        self.add_action(about_action)

        # -------------------------------------------------------------
        # Superimpose the file chooser dialog, open the SUMMARY.md and
        # display the table of contents and the default (README) file.
        # -------------------------------------------------------------
        if self.TV.open_gitbook_folder():
            opening_section = self.TV.table_of_contents()

            self.set_title("BookMaker - " + self.TV.project_directory)

            self.MV.is_dirty = False  # DON'T write nothingness to SUMMARY.md !!!

            self.MV.textbuffer.begin_not_undoable_action()
            self.TV.filename_tail = "README"
            self.TV.open_section(opening_section, self.TV.project_directory, self.TV.filename_tail)
            self.MV.textbuffer.end_not_undoable_action()

            self.TV.re_write_summary()

    # Callbacks for "win" actions

    def on_selectprojectfolder_clicked(self, action, parameter):
        print("selectprojectfolder clicked")
        # self.TV.choose_project_folder()
        with self.TV.choose_project_folder() as project_directory:
            # project_directory = \
            #     '/home/chris/MDProject/Code/programming-python-with-gtk-and-sqlite'
            if project_directory:
                os.chdir(project_directory)  # Always work in the project directory

            # The directory/file details will belong to TV as convention
            self.TV.project_directory = project_directory
            self.TV.filename_tail = 'README'

    def on_exporttoepub_clicked(self, action, parameter):
        print("exporttoepub clicked")
        self.TV.export_to_epub()

    def on_exporttopdf_clicked(self, action, parameter):
        print("exporttopdf clicked")
        self.TV.export_to_pdf()

    def on_undo_clicked(self, action, parameter):
        print("undo clicked")
        if self.MV.textbuffer.can_undo():
            self.MV.textbuffer.undo()
            self.MV.is_dirty = True

    def on_redo_clicked(self, action, parameter):
        print("redo clicked")
        if self.MV.textbuffer.can_redo():
            self.MV.textbuffer.redo()
            self.MV.is_dirty = True

    def on_copy_clicked(self, action, parameter):
        print("copy clicked")
        self.MV.textbuffer.copy_clipboard(self.MV.clipboard)  # Copies the currently-selected text to the clipboard.

    def on_paste_clicked(self, action, parameter):
        print("paste clicked")
        editable = self.MV.textview.get_editable()
        self.MV.textbuffer.paste_clipboard(self.MV.clipboard, None, editable)  # Pastes the contents of the clipboard.
        self.MV.is_dirty = True

    def on_cut_clicked(self, action, parameter):
        print("cut clicked")
        editable = self.MV.textview.get_editable()
        self.MV.textbuffer.cut_clipboard(self.MV.clipboard, editable)
        # Copies the currently-selected text to a clipboard, then deletes the text if it’s editable.
        self.MV.is_dirty = True

    def on_bold_clicked(self, action, parameter):
        print("bold clicked")
        self.MV.wrap_selection("**", "**")
        self.MV.is_dirty = True

    def on_italic_clicked(self, action, parameter):
        print("italic clicked")
        self.MV.wrap_selection("*", "*")
        self.MV.is_dirty = True

    def on_uline_clicked(self, action, parameter):
        print("uline clicked")
        self.MV.wrap_selection("_", "_")
        self.MV.is_dirty = True

    def on_strike_clicked(self, action, parameter):
        print("strike clicked")
        self.MV.wrap_selection("~~", "~~")
        self.MV.is_dirty = True

    def on_as_python_clicked(self, action, parameter):
        print("as_python clicked")
        self.MV.wrap_selection("```py\n", "```")
        self.MV.is_dirty = True

    def on_as_text_clicked(self, action, parameter):
        print("as_text clicked")
        self.MV.wrap_selection("```text\n", "```")
        self.MV.is_dirty = True

    def on_insert_image_clicked(self, action, parameter):

        dlg = Gtk.FileChooserDialog("Insert Image", self, Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dlg.set_current_folder(self.TV.project_directory)
        dlg.set_default_response(Gtk.ResponseType.OK)

        filter = Gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        dlg.add_filter(filter)

        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            imagefilepath = dlg.get_filename()  # actually gets the full path to the file

            images_directory = os.path.join(self.TV.project_directory, '_images')

            # copy the file to the "_images" directory
            shutil.copy(imagefilepath, images_directory)

            # this directory will be copied into the OEBPS directory of the epub, so we
            # need to insert a **relative** link in the generated xhtml content file.

            # Need to be in the current .md file's directory so the relative path will
            # work now in the preview as well as later in the epub file structure.
            os.chdir(os.path.split(self.TV.filename_path)[0])
            print(os.getcwd())
            #
            # NOTE: the .xhtml file structure (below project_directory/_book) must be
            # kept parallel to the .md file structure (below project_directory).
            relative = os.path.relpath(self.TV.project_directory, os.getcwd())
            relative = os.path.join(relative, '_images')
            print(relative)
            print(self.TV.filename_tail)

            self.MV.textbuffer.insert_at_cursor('![]({0}/{1})'.format(relative, os.path.split(imagefilepath)[1]))

            self.MV.is_dirty = True

        dlg.destroy()

    # noinspection PyMethodMayBeStatic
    def on_about_clicked(self, action, parameter):
        """
        Show an About dialog.
        """
        dialog = Gtk.AboutDialog()
        dialog.set_program_name(about.NAME)
        dialog.set_version("%s %s" % ('Version', about.VERSION))
        dialog.set_copyright(about.COPYRIGHT)
        dialog.set_comments(about.DESCRIPTION)
        dialog.set_authors(about.AUTHORS)
        # dialog.set_website(about.WEBSITE)

        dialog.set_license_type(Gtk.License.MIT_X11)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            UPSTART_LOGO,
            about.DEFAULT_LOGO_SIZE_WIDTH, about.DEFAULT_LOGO_SIZE_HEIGHT, True)
        dialog.set_logo(pixbuf)
        dialog.run()
        dialog.destroy()


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(self)
            # title="Hello World!")

        self.window.show_all()

        dmx, dmy = self.window.get_size()
        print(f"Size = {dmx} x {dmy}")

    def do_startup(self):
        # FIRST THING TO DO: do_startup()
        Gtk.Application.do_startup(self)

        # The "app.new"_action
        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.on_new_clicked)
        self.add_action(new_action)

        # The "app.quit"_action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_clicked)
        self.add_action(quit_action)

    # The callbacks for app actions
    # noinspection PyMethodMayBeStatic
    def on_new_clicked(self, action, parameter):
        print("new clicked")

    def on_quit_clicked(self, action, parameter):
        print("quit clicked")
        # Call on_destroy directly to get same effect as clicking window 'x'
        if not self.window.on_delete_event(self.window):
            self.quit()

def main():
    app = Application()
    app.run(sys.argv)


if __name__ == "__main__":
    appl = Application()
    appl.run(sys.argv)
