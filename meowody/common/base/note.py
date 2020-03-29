import re
from meowody.common.octave import Octave
from meowody.common.accidental import Accidental


class Note(object):
    _suffix_pattern = re.compile(r'^([^~]*)(~?)$')

    def __init__(self):
        self.octave = 0        # 八度
        self.accidental = 0    # 变音
        self.duration = None   # 时值
        self._portamento = False  # 是否要延音
        self._mute = False     # 是否闷音
        self._rest = False     # 是否休止符
        self.id = None

    def set_id(self, id_):
        self.id = id_
        return self

    def get_id(self):
        return self.id

    @classmethod
    def rest(cls):
        return cls().set_rest()

    @classmethod
    def mute(cls):
        return cls().set_rest()

    def is_mute(self):
        return self._mute

    def is_rest(self):
        return self._rest

    def set_mute(self):
        self._mute = True
        return self

    def set_rest(self):
        self._rest = True
        return self

    def set_portamento(self):
        self._portamento = True
        return self

    def is_portamento(self):
        return self._portamento

    def with_duration(self, duration):
        self.duration = duration
        return self

    def update(self, other_note):
        """
        :param other_note:
        :type other_note: meowody.lib.common.base.note.Note
        :return:
        """
        self.duration = other_note.duration
        self._mute = other_note.is_mute()
        self._rest = other_note.is_rest()
        self._portamento = other_note.is_portamento()
        return self

    def with_octave(self, octave):
        self.octave = octave
        return self

    def with_accidental(self, accidental):
        self.accidental = accidental
        return self

    def _loads_suffix(self, suffix):
        res = self._suffix_pattern.match(suffix)
        if res is None:
            raise Exception('failed to load suffix from string: {}'.format(suffix))
        octave_mark, portamento_mark = res.groups()
        octave = Octave.loads(octave_mark)
        self.with_octave(octave)
        if portamento_mark != '':
            self.set_portamento()

    def _loads_prefix(self, prefix):
        accidental_mark = prefix
        accidental = Accidental.loads(accidental_mark) if accidental_mark != '' else None
        self.with_accidental(accidental)
