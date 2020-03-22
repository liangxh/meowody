import re
from meowody.common import Note
from meowody.symbolic import SymbolicNote
from meowody.numbered import NumberedNote
from meowody.common import Duration
from meowody.bass.string import BassString


class BassNote(Note):
    _pattern = re.compile(r'^([EADG]?)(\d+|x|\-)(\(([^\)]+)\))?$')

    def __init__(self):
        super(BassNote, self).__init__()
        self.string = None
        self.fret = None
        self._sym_note = -1

    def sub(self, other_note):
        """
        :param other_note:
        :type other_note: meowody.lib.bass.note.BassNote
        :return:
        """
        return NumberedNote.from_sym_note_diff(
            root_note=other_note.sym_note,
            other_note=self.sym_note
        )

    def with_string(self, string):
        """
        :param string:
        :type string: meowody.lib.common.symbolic_note.SymbolicNote
        :return:
        """
        self.string = string
        return self

    def with_pos(self, string, fret):
        """
        :param string:
        :type string: meowody.lib.common.symbolic_note.SymbolicNote
        :param fret:
        :type fret: int
        :return:
        """
        self.string = string
        self.fret = fret
        return self

    def with_sym_note(self, sym_note):
        if self._rest or self._mute or self.string is not None:
            raise Exception('The symbolic note of this bass note has been determined!')
        self._sym_note = sym_note
        return self

    def with_duration(self, duration):
        """
        :param duration:
        :type duration: meowody.lib.common.duration.Duration
        :return:
        """
        self.duration = duration

    def __str__(self):
        data = ''
        if self._mute:
            data += 'string={}, mute=True'.format(self.string.name)
        elif self._rest:
            data += 'rest=True'
        elif self.string is not None and self.fret is not None:
            data += 'string={}, fret={}'.format(self.string.name, self.fret)

        if self.duration is not None:
            data += ', duration=1/{}'.format(self.duration)
        return 'BassNote({})'.format(data)

    @property
    def sym_note(self):
        """
        获取对应唱名
        """
        if self._sym_note is -1:
            if self.string is not None and self.fret is not None:
                if self.fret == 0:
                    # 0品和音和弦的音一样
                    self._sym_note = self.string.clone()
                else:
                    self._sym_note = SymbolicNote.from_pitch(self.string.pitch + self.fret)
            elif self._mute:
                raise Exception('Mute note cannot be converted to symbolic note')
            elif self._rest:
                raise Exception('Rest note cannot be converted to symbolic note')
            else:
                raise Exception('Note information is not complete')
        return self._sym_note

    def get_string_index(self):
        return BassString.get_index(self.string.name)

    def get_loc(self):
        """
        获取键的位置
        """
        if not (self.string is not None and self.fret is not None):
            raise Exception('pos not set yet')
        return BassString.get_index(self.string.name), self.fret

    @classmethod
    def loads(cls, s):
        res = cls._pattern.match(s)
        if res is None:
            raise Exception('failed to load {} as BassNote'.format(s))
        string_name, fret, _, duration = res.groups()

        note = BassNote()
        if fret == '-':
            note.set_rest()
        else:
            string = BassString.get(string_name)
            if fret == 'x':
                note.with_string(string).set_mute()
            else:
                fret = int(fret)
                note.with_pos(string=string, fret=fret)
        if duration is not None:
            note.with_duration(Duration.loads(duration))
        return note

    @classmethod
    def from_symbolic_note(cls, sym_note):
        """
        :param sym_note:
        :param sym_note: meowody.lib.symbolic.note.SymbolicNote
        :return:
        """
        note = cls().update(sym_note)
        if sym_note.is_vocal():
            note.with_sym_note(sym_note=sym_note)
        return note

    def get_possible_positions(self):
        positions = dict()
        for string in BassString.iterate():
            pitch_diff = self.sym_note.pitch - string.pitch
            if pitch_diff >= 0:
                positions[string.name] = pitch_diff
        return positions

    @classmethod
    def show_positions(cls, positions):
        for string in BassString.iterate():
            offset = positions.get(string.name, '-')
            print('{} --{}--'.format(string.name, offset))

    def find_best_position(self, preference, last_note=None, next_note=None):
        """
        :param preference:
        :type preference: meowody.lib.bass.preference.SearchPositionPreference
        :param last_note:
        :type last_note: meowody.lib.bass.note.BassNote
        :param next_note:
        :type next_note: meowody.lib.bass.note.BassNote
        :return:
        """
        positions = self.get_possible_positions()
        best_fret, best_string = None, None

        if last_note is None or not preference.cares_last_note:
            for string_name, fret in positions.items():
                if (best_string is None) or (fret < best_fret):
                    best_string, best_fret = string_name, fret
        else:
            last_str_id = last_note.get_string_index()
            last_fret = last_note.fret

            min_dist = None
            for string_name, fret in positions.items():
                if preference.fret_0_best and fret == 0:
                    best_string, best_fret = string_name, fret
                    break

                str_id = BassString.get_index(string_name)
                dist = (last_str_id - str_id) ** 2 + (fret - last_fret) ** 2
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    best_string, best_fret = string_name, fret

        if best_string is None:
            raise Exception('not playable note: {}'.format(str(self.sym_note)))
        self.with_pos(string=BassString.get(best_string), fret=best_fret)
