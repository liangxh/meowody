from meowody.symbolic import SymbolicNote
from meowody.common.base.script import Script
from meowody.bass import BassSection
from meowody.utils.console import ConsoleLine, FontColor


class BassScript(Script):
    strings = [
        SymbolicNote.loads('G'),
        SymbolicNote.loads('D'),
        SymbolicNote.loads('A.'),
        SymbolicNote.loads('E.'),
    ]

    @classmethod
    def from_sym_script(cls, sym_script):
        """
        :param sym_script:
        :type sym_script: meowody.lib.symbolic.script.SymbolicScript
        :return:
        """
        script = cls()
        for sym_section in sym_script.sections:
            section = BassSection.from_symbolic_section(sym_section=sym_section)
            script.add_section(section)
        return script

    def scan_positions(self, preference):
        n_section = len(self.sections)
        last_section = None
        for i in range(n_section):
            section = self.sections[i]
            section.scan_positions(
                preference=preference,
                last_section=last_section
            )
            last_section = section

    def get_duration_scale(self, min_scale):
        scale = min_scale
        for section in self.sections:
            for note in section:
                if note.duration is None:
                    continue
                scale = max(scale, note.duration.get_scale())
        return scale

    def print(self):
        scale = self.get_duration_scale(min_scale=16)

        last_note = None
        for str_idx, string in enumerate(self.strings):
            line = ConsoleLine()
            line.append('{} ║'.format(string.name))

            for sec_idx, section in enumerate(self.sections):
                if sec_idx != 0:
                    line.append('|')
                for note in section:
                    if note.is_rest():
                        if str_idx == len(self.strings) - 3:
                            line.append('=' * note.duration.get_print_len(scale))
                        else:
                            line.append('-' * note.duration.get_print_len(scale))
                    else:
                        if note.is_mute():
                            line.append('x' + '~' * (note.duration.get_print_len(scale) - 1))
                        elif note.string.name == string.name:
                            if last_note.is_portamento():
                                line.append('~' * note.duration.get_print_len(scale))
                            else:
                                key = str(note.fret)
                                line.append(key + '~' * (note.duration.get_print_len(scale) - len(key)))
                        else:
                            line.append('-' * note.duration.get_print_len(scale))
                    last_note = note
            line.flush()

        line = ConsoleLine()
        line.append('   ')
        for sec_idx, section in enumerate(self.sections):
            if sec_idx != 0:
                line.append(' ')
            line.append('o.o.', fc=FontColor.Red)
            line.append('o.o.', fc=FontColor.Blue)
            line.append('o.o.', fc=FontColor.Red)
            line.append('o.o.', fc=FontColor.Blue)
        line.flush()

    def generate_hash(self):
        h = ''
        for section in self.sections:
            for note in section:
                h += str(note) + ' '
        return h
