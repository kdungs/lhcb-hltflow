class StreamerFlowchart:
    def __init__(self, name, code, prefix=None, properties=None):
        from Sanitize import sanitize_prefix
        self.name = name
        self.code = code
        self.prefix = sanitize_prefix(prefix or name)
        self.properties = properties or {}
        self._tikz = None
    
    @property
    def tikz(self):
        if self._tikz is None:
            self._tikz = self.generateTikz()
        return self._tikz

    def generateTikz(self):
        operations = []
