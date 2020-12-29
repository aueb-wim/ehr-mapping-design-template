
class Correspondence(object):
    def __init__(self, source_paths=[], target_path=None, lastfunction=None, lastcolumn=None, expression=None):
        self.source = source_paths #list of source variables
        self.target = target_path #the target CDE
        self.lastfunction_key = lastfunction #the key of the last function clicked so as to go ahead
        #n load it whenever needed without the user understanding the refreshing of the window
        self.lastcolumn_key = lastcolumn #same thing for the last column clicked
        self.expression = expression