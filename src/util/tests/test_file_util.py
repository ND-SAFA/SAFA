import os

from data.creators.tests.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from testres.base_test import BaseTest
from testres.paths.paths import TEST_OUTPUT_DIR
from testres.test_assertions import TestAssertions
from util.file_util import FileUtil


class TestFileUtil(BaseTest):
    def test_get_file_list(self):
        """
        Tests that pre-training data creator is able to retrieve relevant files in pre-training directory.
        """
        files_dir = FileUtil.get_file_list(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        expected_files = list(map(lambda f: os.path.join(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR, f),
                                  TestMLMPreTrainDatasetCreator.FILENAMES))
        TestAssertions.assert_lists_have_the_same_vals(self, expected_files, files_dir)
        files_single = FileUtil.get_file_list(TestMLMPreTrainDatasetCreator.DATAFILE)
        TestAssertions.assert_lists_have_the_same_vals(self, [expected_files[0]], files_single)

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
