import re
from meowody.common import Duration, Script
from meowody.numbered import NumberedNote, NumberedSection


class NumberedScript(Script):
    def __init__(self):
        """
        :type
        """
        super(NumberedScript, self).__init__()

    def add_section(self, section):
        """
        :param section:
        :type section: meowody.lib.common.numbered.section.NumberedSection
        :return:
        """
        self.sections.append(section)

    @classmethod
    def loads(cls, line, duration_line=None):
        line = re.sub(r'\s+', ' ', line.strip())
        parts = line.split(' ')

        if duration_line is None:
            duration_parts = [Duration.t_4 if part != '|' else '|' for part in parts]
        else:
            duration_line = re.sub(r'\s+', ' ', duration_line.strip())
            duration_parts = duration_line.split(' ')

        script = cls()
        section = None
        for part, duration_part in zip(parts, duration_parts):
            if part == '|':
                if duration_part != '|':
                    raise Exception('note line and duration line mismatch!')
                script.add_section(section)
                section = None
            else:
                if duration_part == '|':
                    raise Exception('note line and duration line mismatch!')

                duration = Duration.loads(duration_part)
                note = NumberedNote.loads(part).with_duration(duration)
                if section is None:
                    section = NumberedSection()
                section.add_note(note)
        if section is not None:
            script.add_section(section)
        return script
