import easygui as eg

# Wraps basic easygui functions, the API is at http://easygui.sourceforge.net/api.html.

def getFilePath(msg = None, title = None, default = '*', filetypes = None, 
		multiple = False):
    """ Opens a Tkinter GUI to select a file. Returns the path of that file.
    
    MSG -- message to display
    TITLE -- the window title
    DEFAULT -- only display files matching default path, wildcards are allowed
    FILETYPES -- the filetypes to show.
    MULTIPLE -- allows the selection of multiple files.

    RETURNS -- The path of the selected file(s), or NONE if no file was selected.
    
    The DEFAULT argument works as follows: the GUI only displays the files that match
    the DEFAULT path. Such that a DEFAULT of 'C:/test/*.py' will open the window in C:/test/
    and only show .py files. A DEFAULT of 'C:/test/test*.py' would only show python files in the
    test directory who's names begin with 'test'.

    The FILETYPES argument works as follows: it must be a list of file types such as
    "*.txt" or "*.pdf". The items of the list are then options in the drop down file 
    type selector. The list may also contain a list of file types that's ended by a
    description such as ['*.py', '*.java', '*.c', 'Code']. Therefore to allow two options
    to select between CSS .css and HTML .htm, .html files the following could be used
    ['*.css', ['*.htm', '*.html', 'HTML files']]
    """
    path = eg.fileopenbox(msg, title, default, filetypes, multiple)
    if path != ".":
    	return path
    else:
    	return None

def twoButtonWindow(msg = "Exit?", title = 'Exit', choice1 = 'Yes',
 		choice2 = 'No', default = True):
	"""Opens a Tkinter GUI to select from two options.

	MSG -- the message to display in the GUI.
	TITLE -- the title to display in the GUI window.
	CHOICE1 -- The string to display on the first button.
	CHOICE2 -- The string to display on the second button.
	DEFAULT -- The highlighted choice when the window is created. 
			   If true the first choice is highlighted.
	
	RETURNS -- TRUE if CHOICE1 was selected, FALSE if CHOICE2 was
			   selected or the window was exited. 
	"""
	if default == True:
		return eg.boolbox(msg, title, (choice1, choice2), default_choice = choice1)
	else:
		return eg.boolbox(msg, title, (choice1, choice2), default_choice = choice2)

def getDirectory(title = None, default = None):
	""" Opens a Tkinter GUI to select a directory.

	TITLE -- the title to display in the GUI window.
	DEFAULT -- The starting directory.

	RETURNS -- The selected path or None if no directory was selected.
	"""
	return eg.diropenbox(title = title, default = default)

def saveFile(msg = None, title = None, default = '', filetypes = None):
	"""Opens a Tkinter GUI to save a file.

	MSG -- The message to be displayed
	TITLE -- The title on the GUI window
	DEFAULT -- The default filename to return
	FILETYPES -- The filetypes that the user can choose.

	RETURNS -- The name of the file, or None if the user exited.

	The FILETYPES argument works as follows: it must be a list of file types such as
    "*.txt" or "*.pdf". The items of the list are then options in the drop down file 
    type selector. The list may also contain a list of file types that's ended by a
    description such as ['*.py', '*.java', '*.c', 'Code']. Therefore to allow two options
    to select between CSS .css and HTML .htm, .html files the following could be used
    ['*.css', ['*.htm', '*.html', 'HTML files']]
	"""
	return eg.filesavebox(msg, title, default, filetypes)

def textBox(msg = 'Enter something.', title = '', default = '', strip = True, image = None):
	"""Opens a GUI from which the user can enter a line of text.

	MSG -- The message to be displayed
	TITLE -- The window title
	DEFAULT -- The default input, returned if the user enters nothing.
	STRIP -- If TRUE, the return value has all whitespace stripped from it.
	IMAGE -- Path to an image to display.

	RETURNS -- The user's input, or NONE if the user exited.
	"""
	return eg.enterbox(msg, title, default, strip, image)
