from pathlib import Path
from renamer.entry import rename_class_or_function, move_class_or_function


def test_func_rename():
    got = rename_class_or_function(
        'tests/fixtures/test_rename_func_source',
        'func',
        'newfunc'
    )
    assert got[0][0] == 'tests/fixtures/test_rename_func_source\\source.py' and Path(
        'tests/fixtures/test_rename_func_expected/expected.py').read_text() == got[0][1]


def test_class_def_rename():
    got = rename_class_or_function(
        'tests/fixtures/test_def_class_rename_source',
        'SourceClass',
        'SClass'
    )
    assert got[0][0] == 'tests/fixtures/test_def_class_rename_source\\source.py' and Path(
        'tests/fixtures/test_def_class_rename_expected/expected.py').read_text() == got[0][1]


def test_class_base_rename():
    got = rename_class_or_function(
        'tests/fixtures/test_base_class_rename_source',
        'Base',
        'NewBase'
    )
    assert got[0][0] == 'tests/fixtures/test_base_class_rename_source\\source.py' and Path(
        'tests/fixtures/test_base_class_rename_expected/expected.py').read_text() == got[0][1]


def test_rename_many_files():
    got = rename_class_or_function(
        'tests/fixtures/test_rename_class_many_files_source',
        'FirstClass',
        'FFClass'
    )
    assert got[0][0] == 'tests/fixtures/test_rename_class_many_files_source\\source1.py' and \
           Path('tests/fixtures/test_rename_class_many_files_expected/source1.py').read_text() == got[0][1]

    assert got[1][0] == 'tests/fixtures/test_rename_class_many_files_source\\source2.py' and \
           Path('tests/fixtures/test_rename_class_many_files_expected/source2.py').read_text() == got[1][1]

    assert got[2][0] == 'tests/fixtures/test_rename_class_many_files_source\\source3.py' and \
           Path('tests/fixtures/test_rename_class_many_files_expected/source3.py').read_text() == got[2][1]


def test_rename_in_dir():
    got = rename_class_or_function(
        'tests/fixtures/test_rename_in_dir_source',
        'SClass',
        'FClass'
    )
    assert got[0][0] == 'tests/fixtures/test_rename_in_dir_source\\source1.py' and \
           Path('tests/fixtures/test_rename_in_dir_expected/source1.py').read_text() == got[0][1]

    assert got[1][0] == 'tests/fixtures/test_rename_in_dir_source\\dir\\source2.py' and \
           Path('tests/fixtures/test_rename_in_dir_expected/dir/source2.py').read_text() == got[1][1]


def test_move_function():
    got = move_class_or_function(
        'tests/fixtures/test_move_func_source',
        'source.py',
        'new_source.py',
        'function'
    )
    assert got[0][0] == 'tests/fixtures/test_move_func_source\\dest.py' and \
           got[0][1] == Path('tests/fixtures/test_move_func_expected/dest.py').read_text()
