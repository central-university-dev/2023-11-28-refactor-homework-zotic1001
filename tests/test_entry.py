import os
from pathlib import Path
from renamer.entry import rename_class_or_function, move_class_or_function


def replace_last_folder(path, new_folder_name):
    path = Path(path)
    path_components = list(path.parts)
    for i in range(len(path_components) - 1, -1, -1):
        if '.' not in path_components[i]:
            path_components[i] = new_folder_name
            break
    new_path = Path(*path_components)
    return new_path


def test_func_rename():
    got = rename_class_or_function(
        'tests/fixtures/test_rename_func_source',
        'func',
        'newfunc'
    )
    for k in got.keys():
        assert got[k] == replace_last_folder(k, 'test_rename_func_expected').read_text()


def test_class_def_rename():
    got = rename_class_or_function(
        'tests/fixtures/test_def_class_rename_source',
        'SourceClass',
        'SClass'
    )
    for k in got.keys():
        assert got[k] == replace_last_folder(k, 'test_def_class_rename_expected').read_text()


def test_class_base_rename():
    got = rename_class_or_function(
        'tests/fixtures/test_base_class_rename_source',
        'Base',
        'NewBase'
    )
    for k in got.keys():
        assert got[k] == replace_last_folder(k, 'test_base_class_rename_expected').read_text()


def test_rename_many_files():
    got = rename_class_or_function(
        'tests/fixtures/test_rename_class_many_files_source',
        'FirstClass',
        'FFClass'
    )
    for k in got.keys():
        assert got[k] == Path(str(k).replace('test_rename_class_many_files_source',
                                             'test_rename_class_many_files_expected')).read_text()


def test_rename_in_dir():
    got = rename_class_or_function(
        'tests/fixtures/test_rename_in_dir_source',
        'SClass',
        'FClass'
    )
    for k in got.keys():
        assert got[k] == Path(str(k).replace('test_rename_in_dir_source',
                                             'test_rename_in_dir_expected')).read_text()


def test_move_function():
    got = move_class_or_function(
        'tests/fixtures/test_move_func_source',
        'source.py',
        'new_source.py',
        'function'
    )
    for k in got.keys():
        assert got[k] == Path(str(k).replace('test_move_func_source',
                                             'test_move_func_expected')).read_text()
