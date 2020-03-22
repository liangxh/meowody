class Section(object):
    def __init__(self):
        self.notes = list()
        self.id = None

    def set_id(self, id_):
        self.id = id_
        return self

    def get_id(self):
        return self.id

    def add_note(self, note):
        """
        :param note:
        :return:
        """
        if note.get_id() is not None:
            raise Exception('note id has been set???')
        note_id = len(self.notes)
        note.set_id(note_id)
        self.notes.append(note)

    def __iter__(self):
        for note in self.notes:
            yield note
