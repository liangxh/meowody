class Script(object):
    def __init__(self):
        self.sections = list()

    def add_section(self, section):
        if section.get_id() is not None:
            raise Exception('note id has been set???')
        section_id = len(self.sections)
        section.set_id(section_id)
        self.sections.append(section)

    def __iter__(self):
        for section in self.sections:
            yield section
