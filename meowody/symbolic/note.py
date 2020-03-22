import re
from meowody.common import Note, Accidental, Octave
from meowody.common.const import DEGREE_PITCH_DIFF
from meowody.context import context


class SymbolicNote(Note):
    """
    唱名
    """
    _start_ascii_code = ord('A')
    _n_symbolic_names = 7
    _str_pattern = re.compile(r'^(.*)([A-G])(.+)?$')

    name_to_pitch = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    def __init__(self, name=None, accidental=None, octave=None):
        super(SymbolicNote, self).__init__()
        self.name = name
        self.accidental = accidental if accidental is not None else 0
        self.octave = octave if octave is not None else 0
        self._pitch = None

    def __str__(self):
        return Accidental.symbol(self.accidental) + self.name + Octave.to_str(self.octave)

    def is_vocal(self):
        return self.name is not None

    @classmethod
    def loads(cls, s):
        res = cls._str_pattern.match(s)
        accidental_mark, name, octave_mark = res.groups()
        accidental = Accidental.loads(accidental_mark) if accidental_mark != '' else None
        octave = Octave.loads(octave_mark)
        return cls(name, accidental, octave)

    @property
    def pitch(self):
        if self._pitch is None:
            self._pitch = self.name_to_pitch[self.name] + self.accidental + self.octave * 12
        return self._pitch

    @classmethod
    def from_pitch(cls, pitch):
        octave = pitch // 12
        offset = pitch % 12

        if offset == 11 and context.accidental_preference == Accidental.FLAT:
            return cls(name='C', accidental=Accidental.FLAT, octave=octave + 1)
        else:
            last_pitch = None
            last_name = None
            for degree_index, name in enumerate(['C', 'D', 'E', 'F', 'G', 'A', 'B']):
                pitch = DEGREE_PITCH_DIFF[degree_index]
                if pitch == offset:
                    return cls(name=name, accidental=None, octave=octave)
                elif context.accidental_preference == Accidental.FLAT and pitch - 1 == offset:
                    # 比这一度低半度
                    return cls(name=name, accidental=Accidental.FLAT, octave=octave)
                elif context.accidental_preference == Accidental.SHARP and last_pitch + 1 == offset:
                    # 不是上一度也不是这一度，那就是上一度高半度
                    return cls(name=last_name, accidental=Accidental.SHARP, octave=octave)
                else:
                    # 继续看下一个
                    pass
                last_pitch = pitch
                last_name = name
        raise Exception('unexpected error')

    def clone(self):
        note = SymbolicNote(name=self.name, accidental=self.accidental, octave=self.octave)
        note.update(self)
        return note

    def add(self, numbered_note):
        """
        :param numbered_note:
        :param numbered_note: meowody.lib.common.numbered_note.NumberedNote
        :return:
        """
        if numbered_note.pitch is not None:
            new_pitch = self.pitch + numbered_note.pitch
            note = SymbolicNote.from_pitch(pitch=new_pitch)
        else:
            note = SymbolicNote()
        note.update(numbered_note)
        return note
