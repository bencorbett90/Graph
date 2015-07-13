import easygui as eg

class GraphException(Exception):
	"""A custom exception for the graphing program."""
	def __init__(self, message):
		super(GraphException, self).__init__(message)
		eg.indexbox(message, 'Error', ["Continue"], default_choice = 'Continue')