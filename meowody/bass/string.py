from meowody.symbolic import SymbolicNote


class BassString(object):
    _name_to_string = {
        'G': SymbolicNote.loads('G'),
        'D': SymbolicNote.loads('D'),
        'A': SymbolicNote.loads('A.'),
        'E': SymbolicNote.loads('E.')
    }
    _ordered_string_names = ['E', 'A', 'D', 'G']

    @classmethod
    def get(cls, name):
        return cls._name_to_string[name]

    @classmethod
    def iterate(cls):
        for name in cls._ordered_string_names:
            yield cls._name_to_string[name]

    @classmethod
    def get_index(cls, name):
        """
        :param name: str
        :return:
        """
        return cls._ordered_string_names.index(name)
