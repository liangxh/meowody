import commandr
import meowody
from meowody.bass.string import BassString
from meowody.bass import BassNote
from meowody.bass import BassSection
from meowody.bass import BassScript
from meowody.symbolic import SymbolicNote
from meowody.symbolic import SymbolicScript
from meowody.numbered import NumberedScript
from meowody.bass.preference import SearchPositionPreference


@commandr.command
def show_options(name):
    sym_note = SymbolicNote.loads(name)
    note = BassNote().with_sym_note(sym_note=sym_note)
    positions = note.get_possible_positions()
    BassNote.show_positions(positions)


@commandr.command
def test_note(s):
    note = BassNote.loads(s)
    print(note)


@commandr.command
def analyse_session(line):
    section = BassSection.loads(line)
    numbered_notes = section.get_numbered_notes()
    print(' '.join(map(lambda _n: str(_n), numbered_notes)))


@commandr.command
def build_script(major_name, line):
    print()
    num_script = NumberedScript.loads(line)
    major = BassString.get(major_name)
    sym_script = SymbolicScript(major=major).load_from_numbered_script(num_script)
    script = BassScript.from_sym_script(sym_script)

    preference = SearchPositionPreference()
    preference.cares_notes_with_sound_only = True

    id_ = ord('A')
    occurred_hash = set()
    for cares_last_note in [True, False]:
        for fret_0_best in [True, False]:
            preference.cares_last_note = cares_last_note
            preference.fret_0_best = fret_0_best

            script.scan_positions(preference=preference)
            h = script.generate_hash()
            if h not in occurred_hash:
                print('Suggestion {}'.format(chr(id_)))
                script.print()
                print()
                id_ += 1
                occurred_hash.add(h)


@commandr.command('bf')
def build_from_file(filename):
    preference = SearchPositionPreference()
    preference.cares_notes_with_sound_only = True
    preference.cares_last_note = True
    preference.fret_0_best = False

    lines = list()
    with open(filename, 'r') as file_obj:
        for line in file_obj:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            lines.append(line)

    line_id = 0
    while line_id < len(lines):
        if not lines[line_id].startswith('1='):
            raise Exception('expected 1=* got: {}'.format(lines[line_id]))
        major_name = lines[line_id][2:]
        line = lines[line_id + 1]

        if line_id + 2 < len(lines) and not lines[line_id + 2].startswith('1='):
            duration_line = lines[line_id + 2]
            line_id += 3
        else:
            duration_line = None
            line_id += 2

        num_script = NumberedScript.loads(line, duration_line)
        major = SymbolicNote.loads(major_name)
        sym_script = SymbolicScript(major=major).load_from_numbered_script(num_script)
        script = BassScript.from_sym_script(sym_script)

        script.scan_positions(preference=preference)
        script.print()
        print()


if __name__ == '__main__':
    commandr.Run()
