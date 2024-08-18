import os
from os.path import dirname

from gen_common.constants.symbol_constants import USER_SYM
from gen_common.util.file_util import FileUtil
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.data.creators.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from gen_common_test.paths.base_paths import TEST_DIR_PATH, TEST_OUTPUT_DIR


class TestFileUtil(BaseTest):
    PARENT_DIR = os.path.dirname(__file__)

    def test_get_file_list(self):
        """
        Tests that pre-training data creator is able to retrieve relevant files in pre-training directory.
        """
        files_dir = FileUtil.get_file_list(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        expected_files = list(map(lambda f: os.path.join(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR, f),
                                  TestMLMPreTrainDatasetCreator.FILENAMES))
        self.assert_lists_have_the_same_vals(expected_files, files_dir)
        files_single = FileUtil.get_file_list(TestMLMPreTrainDatasetCreator.DATAFILE)
        self.assert_lists_have_the_same_vals([expected_files[0]], files_single)

    def test_move_dir_contents(self):
        """
        Tests that move dir contents moves all files inside the directory to the specified location
        """
        orig_dir = os.path.join(TEST_OUTPUT_DIR, "orig_dir")
        files = ["file1.txt", "file2.txt"]
        for filename in files:  # create empty files
            FileUtil.safe_open_w(os.path.join(orig_dir, filename))
        new_dir = os.path.join(TEST_OUTPUT_DIR, "new_dir")
        FileUtil.move_dir_contents(orig_dir, new_dir, delete_after_move=True)
        for filename in files:  # create empty files
            self.assertTrue(os.path.exists(os.path.join(new_dir, filename)))
        self.assertFalse(os.path.exists(os.path.join(TEST_OUTPUT_DIR, orig_dir)))

    def test_add_to_path(self):
        """
        Test ability to add components to path by index
        """
        test_component = "new-file"
        path = "/folder_1/folder_2/file"
        expected_path = f"/folder_1/folder_2/file/{test_component}"
        path_result = FileUtil.add_to_path(path, test_component, 3)
        self.assertEqual(expected_path, path_result)
        path_result = FileUtil.add_to_path(path, test_component, -1)
        self.assertEqual(expected_path, path_result)
        path_result = FileUtil.add_to_path(path, test_component, -2)
        self.assertEqual(f"/folder_1/folder_2/{test_component}/file", path_result)

    def test_path_to_list(self):
        """
        Tests that path is able to split into component parts
        """
        path = "/folder_1/folder_2/file"
        path_list = FileUtil.path_to_list(path)
        self.assertEqual(3, len(path_list))
        for expected_item in ["folder_1", "folder_2", "file"]:
            self.assertIn(expected_item, path_list)

    def test_get_file_name(self):
        """
        Tests that construction of parent-based file names works.
        :return:
        """
        self.assertEqual("456", FileUtil.get_file_name("456"))
        self.assertEqual("456", FileUtil.get_file_name("123/456"))
        self.assertEqual("123-456", FileUtil.get_file_name("123/456", 1))
        self.assertEqual("def-123-456", FileUtil.get_file_name("abc/def/123/456", 2))

    def test_find_all_file_paths_that_meet_condition(self):
        """
        Tests that move dir contents moves all files inside the directory to the specified location
        """
        base_dir = os.path.join(TEST_OUTPUT_DIR, "base_dir")
        nested_dir = os.path.join(base_dir, "nested_dir")
        files = ["file1.txt", "file2.txt"]

        for filename in files:  # create empty files
            FileUtil.safe_open_w(os.path.join(base_dir, filename))
            FileUtil.safe_open_w(os.path.join(nested_dir, filename))

        file_paths = FileUtil.get_all_paths(base_dir, lambda x: "2" in x)
        self.assertIn(os.path.join(base_dir, files[1]), file_paths)
        self.assertIn(os.path.join(nested_dir, files[1]), file_paths)

    def test_add_ext(self):
        originally_wrong_ext = "home/test.txt"
        with_csv = FileUtil.add_ext(originally_wrong_ext, FileUtil.CSV_EXT)
        self.assertEqual(with_csv, "home/test.csv")

        with_no_ext = "home/test"
        with_yaml = FileUtil.add_ext(with_no_ext, FileUtil.YAML_EXT)
        self.assertEqual(with_yaml, "home/test.yaml")

    def test_get_directory_path(self):
        expected_dirname = "/home/dir1"

        file_path_with_filename = expected_dirname + "/test.txt"
        dirname = FileUtil.get_directory_path(file_path_with_filename)
        self.assertEqual(dirname, expected_dirname)

        dirname = FileUtil.get_directory_path(expected_dirname)  # no filename
        self.assertEqual(dirname, expected_dirname)

    def test_expand_paths(self):
        starting_path = FileUtil.get_starting_path()
        expected_path = f"{TEST_DIR_PATH}/util/test_file_util.py"
        self.assertTrue(os.path.exists(expected_path))

        # Test 1 - Test that relative path to test file can be correctly assumed to starting path.
        r_var1 = "[replacement]"
        replacements_1 = {r_var1: "."}
        p1 = f"{r_var1}/test_file_util.py"
        output1 = FileUtil.expand_paths(p1, replacements_1)
        self.assertEqual(output1, os.path.join(starting_path, "test_file_util.py"))

        # Test 2 - Test that user path is correctly assumed.
        p2 = expected_path.replace(os.path.expanduser('~'), USER_SYM)
        output2 = FileUtil.expand_paths(p2)
        self.assertEqual(output2, expected_path)

        # Test 3 - test multiple assignments with relative paths
        replacements_3 = {"[replacement1]": "./hi", "[replacement2]": "./hola"}
        p3 = ["[replacement1]/one.txt", "[replacement2]/two.txt"]
        p3_dict = {i: path for i, path in enumerate(p3)}
        for iterable_paths in [p3, p3_dict]:
            expanded_path_iter = FileUtil.expand_paths(iterable_paths, replacements_3)
            self.assertTrue(expanded_path_iter[0].startswith(os.path.join(starting_path, "hi")))
            self.assertTrue(expanded_path_iter[1].startswith(os.path.join(starting_path, "hola")))

        # Tset 4 - Test that expanded path will not longer be modified.
        self.assertEqual(expected_path, FileUtil.expand_paths(expected_path))

        # Test 5 - Test that none replacements are not included in final output.
        replacements_3 = {"[replacement1]": "hi", "[replacement2]": None}
        p3_dict = {1: "[replacement1]/one.txt", 2: "[replacement2]"}
        expanded_path_without_none = FileUtil.expand_paths(p3_dict, replacements_3, remove_none_vals=True)
        self.assertEqual(len(expanded_path_without_none), 1)
        self.assertIn(1, expanded_path_without_none)

    def test_expand_paths_int(self):
        """
        Tests that numbers can replace variables.
        """
        result = FileUtil.expand_paths("[EPOCHS_INT]", {"[EPOCHS_INT]": 3})
        self.assertEqual(3, result)

    def test_order_paths_by_least_to_most_overlap(self):
        paths = ["root/path1", "root/path1/path2", "unrelated/path1", "root/other", "root", "unrelated"]
        expected_order = ['root', 'root/path1', 'root/path1/path2', 'root/other', 'unrelated', 'unrelated/path1']
        orderings = FileUtil.order_paths_by_overlap(paths)
        self.assertListEqual(expected_order, orderings)

    def test_collapse_paths(self):
        root_path = dirname(TEST_DIR_PATH)
        os.environ["ROOT_PATH"] = root_path
        p = f"{self.PARENT_DIR}/test_file_util.py"
        expected_path = os.path.relpath(p, root_path)
        collapsed_path_relative = FileUtil.collapse_paths(p, replacements={"[ROOT_PATH]": dirname(TEST_DIR_PATH)})
        self.assertEqual(collapsed_path_relative, f"[ROOT_PATH]/{expected_path}")

        replacements = {"[path1]": "root/path1",
                        "[path2]": "unrelated/path1",
                        "[ROOT]": "root"}
        paths = ["root/path1/code.py", "unrelated/path1/text.txt"]
        collapsed_paths = FileUtil.collapse_paths(paths, replacements)
        expanded_paths = ['[path1]/code.py', '[path2]/text.txt']
        self.assertListEqual(collapsed_paths, expanded_paths)

    def test_safely_join_paths(self):
        normal = FileUtil.safely_join_paths("path1", "path2", 3, ext=".txt")
        self.assertEqual(normal, "path1/path2/3.txt")

        with_none = FileUtil.safely_join_paths(None, "path2")
        self.assertEqual(with_none, None)

        with_empty = FileUtil.safely_join_paths("path1", "")
        self.assertEqual(with_empty, "")

    def test_is_code(self):
        code_files = ["test/code.py", "CODE.JAVA", ".h", "CPP", "test/makefile"]
        for file in code_files:
            self.assertTrue(FileUtil.is_code(file))
        self.assertFalse(FileUtil.is_code("not_code.txt"))

    def test_convert_path_to_human_readable(self):
        self.assertEqual(FileUtil.convert_path_to_human_readable("/path/to/somewhere.txt"), " path to somewhere")
