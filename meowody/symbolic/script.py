from meowody.common import Script


class SymbolicScript(Script):
    def __init__(self, major):
        """
        :param major:
        :type major: meowody.lib.common.symbolic_note.SymbolicNote
        :type
        """
        super(SymbolicScript, self).__init__()
        self.major = major

    def load_from_numbered_script(self, num_script):
        for section in num_script:
            sym_section = section.to_symbolic_section(major=self.major)
            self.add_section(sym_section)
        return self
