from meowody.common import Section
from meowody.symbolic import SymbolicSection


class NumberedSection(Section):
    def to_symbolic_section(self, major):
        """
        :param major:
        :type major: meowody.lib.common.symbolic_note.SymbolicNote
        :return:
        """
        section = SymbolicSection()
        for note in self.notes:
            sym_note = major.add(note)
            sym_note.update(note)
            section.add_note(sym_note)
        return section
