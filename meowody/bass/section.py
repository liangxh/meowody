import re
from meowody.numbered import NumberedNote
from meowody.bass import BassNote
from meowody.common import Section


class BassSection(Section):
    def get_numbered_notes(self):
        numbered_notes = [NumberedNote.from_pitch(0)]
        for note in self.notes[1:]:
            if note.is_mute() or note.is_rest():
                continue
            numbered_note = note.sub(self.notes[0])
            numbered_notes.append(numbered_note)
        return numbered_notes

    @classmethod
    def loads(cls, line):
        section = cls()
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)
        parts = line.split(' ')
        for part in parts:
            note = BassNote.loads(part)
            section.add_note(note)
        return section

    @classmethod
    def from_symbolic_section(cls, sym_section):
        section = cls()
        for sym_note in sym_section:
            note = BassNote.from_symbolic_note(sym_note)
            section.add_note(note)
        return section

    def first_note(self, with_sound=True):
        """
        :param with_sound: bool
        :return:
        """
        if not with_sound:
            return self.notes[0]
        else:
            for note in self.notes:
                if not note.is_mute() and not note.is_rest():
                    return note
            return None

    def last_note(self, with_sound=True):
        """
        :param with_sound: bool
        :return:
        """
        if not with_sound:
            return self.notes[-1]
        else:
            for i in range(len(self.notes)):
                note = self.notes[-i - 1]
                if not note.is_mute() and not note.is_rest():
                    return note
            return None

    def scan_positions(self, preference, last_section=None):
        """
        :param preference:
        :type preference: meowody.lib.bass.preference.SearchPositionPreference
        :param last_section:
        :type last_section: meowody.lib.bass.section.BassSection
        :return:
        """
        n_notes = len(self.notes)
        if last_section is not None and preference.cares_last_note:
            last_note = last_section.last_note(with_sound=preference.cares_notes_with_sound_only)
        else:
            last_note = None

        for i in range(n_notes):
            note = self.notes[i]
            if note.is_mute() or note.is_rest():
                if not preference.cares_notes_with_sound_only:
                    last_note = note
            else:
                note.find_best_position(
                    preference=preference,
                    last_note=last_note,
                    next_note=None
                )
                last_note = note
