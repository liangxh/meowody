import re
from meowody.common import Note, Accidental, Octave
from meowody.common.const import DEGREE_PITCH_DIFF
from meowody.context import context


class NumberedNote(Note):
    _str_pattern = re.compile(r'^(\D*)(\d+)(.*)$')

    def __init__(self, degree=None, accidental=None, octave=None):
        super(NumberedNote, self).__init__()
        self.degree = degree
        self.accidental = accidental
        self.octave = octave
        self._pitch = None

    @property
    def pitch(self):
        if self._rest or self._mute:
            return None
        if self._pitch is None:
            self._pitch = DEGREE_PITCH_DIFF[self.degree - 1] \
                + (self.accidental if self.accidental is not None else 0) \
                + self.octave * 12
        return self._pitch

    def __str__(self):
        return Accidental.symbol(self.accidental) + str(self.degree) + Octave.to_str(self.octave)

    @classmethod
    def loads(cls, s):
        res = cls._str_pattern.match(s)
        if res is None:
            raise Exception('failed to load {} as numbered_note'.format(s))
        prefix, degree, suffix = res.groups()
        degree = int(degree)
        if degree == 0:
            return cls.rest()
        else:
            note = cls(degree=degree)
            note._loads_prefix(prefix=prefix)
            note._loads_suffix(suffix=suffix)
            return note

    @classmethod
    def from_pitch(cls, pitch_diff):
        offset = pitch_diff % 12
        octave = pitch_diff // 12
        degree = None
        accidental = None
        if offset == 11 and context.accidental_preference == Accidental.FLAT:
            octave += 1
            accidental = Accidental.FLAT
            degree = 1
        else:
            last_pitch = None
            last_degree_idx = None
            for degree_idx, pitch in enumerate(DEGREE_PITCH_DIFF):
                if pitch == offset:
                    degree = degree_idx + 1
                    break
                elif context.accidental_preference == Accidental.FLAT and pitch - 1 == offset:
                    degree = degree_idx + 1
                    accidental = Accidental.FLAT
                    break
                elif context.accidental_preference == Accidental.SHARP and last_pitch + 1 == offset:
                    # 不是上一度也不是这一度，那就是上一度高半度
                    degree = last_degree_idx + 1
                    accidental = Accidental.SHARP
                    break
                else:
                    # 继续看下一个
                    pass
                last_pitch = pitch
                last_degree_idx = degree_idx
        if degree is None:
            raise Exception('failed to process: {}'.format(pitch_diff))
        return cls(degree=degree, accidental=accidental, octave=octave)

    @classmethod
    def from_sym_note_diff(cls, root_note, other_note):
        """
        :param root_note:
        :type root_note: meowody.lib.common.symbolic_note.SymbolicNote
        :param other_note:
        :type other_note: meowody.lib.common.symbolic_note.SymbolicNote
        :return:
        """
        return cls.from_pitch(other_note.pitch - root_note.pitch)
