import os
from pathlib import Path
import libcst


class RenameTransformer(libcst.CSTTransformer):

    def __init__(self, old_name, target_name):
        self._old_name = old_name
        self._target_name = target_name

    def leave_ClassDef(self, original_node, updated_node):
        new_bases = []
        for base_node in original_node.bases:
            if base_node.value.value == self._old_name:
                new_bases.append(libcst.Arg(libcst.Name(self._target_name)))
            else:
                new_bases.append(base_node)
        if original_node.name.value == self._old_name:
            return updated_node.with_changes(name=libcst.Name(self._target_name))
        else:
            new_node = updated_node.with_changes(bases=new_bases)
            return new_node

    def leave_ImportFrom(self, original_node, updated_node):
        new_names = []
        new_module = original_node.module
        for alias in original_node.names:
            if alias.name.value == self._old_name:
                new_names.append(libcst.ImportAlias(name=libcst.Name(self._target_name), asname=alias.asname))
            else:
                new_names.append(alias)
        return updated_node.with_changes(module=new_module, names=new_names)

    def leave_FunctionDef(self, original_node, updated_node):
        if original_node.name.value == self._old_name:
            # Create a new ClassDef node with the updated name
            return updated_node.with_changes(name=libcst.Name(self._target_name))
        else:
            return updated_node

    def leave_Call(self, original_node, updated_node):
        if isinstance(original_node.func, libcst.Name) and original_node.func.value == self._old_name:
            new_func = libcst.Name(self._target_name)
            return updated_node.with_changes(func=new_func)
        if isinstance(original_node.func, libcst.Attribute):
            if isinstance(original_node.func.value, libcst.Name) and original_node.func.value.value == self._old_name:
                new_attribute = libcst.Attribute(value=libcst.Name(self._target_name), attr=original_node.func.attr)
                return updated_node.with_changes(func=new_attribute)
        return updated_node


class MoveClassTransformer(libcst.CSTTransformer):
    def __init__(self, original_file, new_file, class_name):
        self.original_file = original_file
        self.new_file = new_file
        self.class_name = class_name

    def leave_ImportFrom(self, original_node, updated_node):
        file_array = self.new_file.split('/')
        for i in range(len(file_array)):
            file_array[i] = file_array[i].replace('.py', '')
        if len(file_array) == 1:
            if original_node.module.value == self.original_file[:-3]:
                for alias in original_node.names:
                    if alias.name.value == self.class_name:
                        return updated_node.with_changes(module=libcst.Name(self.new_file[:-3]))
        return updated_node


def rename_variable(source_code: str, old_name: str, target_name: str) -> str:
    rename_transformer = RenameTransformer(old_name, target_name)
    original_tree = libcst.parse_module(source_code)
    renamed_tree = original_tree.visit(rename_transformer)
    return renamed_tree.code


def rename_class_or_function(directory: str, source_name, dest_name):
    files_and_path_result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                files_and_path_result.append(
                    (str(file_path), rename_variable(Path(file_path).read_text(), source_name, dest_name)))
    return files_and_path_result


def move_class_or_function(directory: str, source_file: str, new_source_file: str, source: str):
    files_and_path_result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                tr = MoveClassTransformer(str(Path(source_file)), new_source_file, source)
                file_path = os.path.join(root, file)
                original_tree = libcst.parse_module(Path(file_path).read_text())
                renamed_tree = original_tree.visit(tr)
                files_and_path_result.append((file_path, renamed_tree.code))
    return files_and_path_result
