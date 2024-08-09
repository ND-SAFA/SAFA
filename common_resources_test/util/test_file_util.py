import os
from os.path import dirname
from unittest import skip

from common_resources.tools.constants.env_var_name_constants import PROJ_PATH_PARAM
from common_resources.tools.constants.environment_constants import PROJ_PATH
from common_resources.tools.constants.symbol_constants import USER_SYM
from common_resources.tools.util.file_util import FileUtil
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.data.creators.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from common_resources_test.paths.base_paths import TEST_DIR_PATH, TEST_OUTPUT_DIR
from common_resources_test.test_constants import TEST_DIR_NAME


class TestFileUtil(BaseTest):
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
        os.environ[PROJ_PATH_PARAM] = os.path.join(dirname(dirname(__file__)), "common_resources")
        expected_path = f"{TEST_DIR_PATH}/util/test_file_util.py"
        self.assertTrue(os.path.exists(expected_path))

        replacement_var = "[replacement]"
        replacements_relative = {replacement_var: "."}
        relative_path = f"{replacement_var}/{TEST_DIR_NAME}/util/test_file_util.py"
        expanded_path_relative = FileUtil.expand_paths(relative_path, replacements_relative)
        self.assertEqual(expected_path, expanded_path_relative)

        user_path = os.path.expanduser('~')
        without_user_path = expected_path.replace(user_path, USER_SYM)
        expanded_path_user = FileUtil.expand_paths(without_user_path)
        self.assertEqual(expanded_path_user, expected_path)

        replacements = {"[replacement1]": "./hi", "[replacement2]": "./hola"}
        path_list = ["[replacement1]/one.txt", "[replacement2]/two.txt"]
        paths_dict = {i: path for i, path in enumerate(path_list)}
        for iterable_paths in [path_list, paths_dict]:
            expanded_path_iter = FileUtil.expand_paths(iterable_paths, replacements)
            self.assertTrue(expanded_path_iter[0].startswith(os.path.join(PROJ_PATH, "hi")))
            self.assertTrue(expanded_path_iter[1].startswith(os.path.join(PROJ_PATH, "hola")))
        self.assertEqual(expected_path, FileUtil.expand_paths(expected_path))

        replacements = {"[replacement1]": "hi", "[replacement2]": None}
        paths_dict = {1: "[replacement1]/one.txt", 2: "[replacement2]"}
        expanded_path_without_none = FileUtil.expand_paths(paths_dict, replacements, remove_none_vals=True)
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

    @skip("Need feedback on why this is the expected behavior")
    def test_collapse_paths(self):
        expanded_path = f"{os.path.dirname(PROJ_PATH)}/test/util/test_file_util.py"
        relative_path = f"../test/util/test_file_util.py"
        collapsed_path_relative = FileUtil.collapse_paths(expanded_path)
        self.assertEqual(relative_path, collapsed_path_relative)

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
