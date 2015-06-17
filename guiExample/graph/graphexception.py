class GraphException(Exception):
	"""A custom exception for the graphing program."""
	def __init__(self, message):
		super(GraphException, self).__init__(message)