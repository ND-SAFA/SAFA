import os

from gen_common_test.base.tests.base_test import BaseTest

from gen.data.github.code.cpp_to_header_link_creator import CPPToHeaderLinkCreator
from gen_test.res.paths import GEN_TEST_PROJECT_GITHUB_CPPANDHPP_PATH


class TestCppHeaderLinkCreator(BaseTest):
    CPP_FILES = ["file.cpp", "fnctl.cpp", "grp.cpp", "mman.cpp", "mqueue.cpp", "socket.cpp", "unistd.cpp"]
    UNLINKED_FILES = ["unistd.cpp", "fnctl.cpp"]
    DIR_PATH = GEN_TEST_PROJECT_GITHUB_CPPANDHPP_PATH
    SOURCE_PATH = os.path.join(DIR_PATH, "source")
    HEADER_PATH = os.path.join(DIR_PATH, "include", "iceoryx_platform")

    def test_get_all_cpp_files_in_dir(self):
        cpp_files = CPPToHeaderLinkCreator._get_all_cpp_files_in_dir(self.DIR_PATH)
        for file in self.CPP_FILES:
            self.assertIn(os.path.join(self.SOURCE_PATH, file), cpp_files)

    def test_split_base_path_and_filename(self):
        base_path, filename = CPPToHeaderLinkCreator._split_base_path_and_filename(os.path.join(self.SOURCE_PATH, "file.cpp"))
        self.assertEqual(base_path, self.SOURCE_PATH)
        self.assertEqual(filename, "file")

    def test_get_cpp_file_path_parts(self):
        module_path, code_path, filename = CPPToHeaderLinkCreator._get_cpp_file_path_parts(os.path.join(self.SOURCE_PATH, "file.cpp"))
        self.assertEqual(module_path, self.DIR_PATH + "/")
        self.assertEqual(filename, "file")

    def test_find_header_file(self):
        hpp_file = self.CPP_FILES[0].replace("cpp", "hpp")
        hpp_file = CPPToHeaderLinkCreator._find_header_file(self.DIR_PATH, hpp_file)
        self.assertEqual(hpp_file, os.path.join(self.HEADER_PATH, hpp_file))

    def test_get_header_path(self):
        cpp_file = self.CPP_FILES[0]
        hpp_file = cpp_file.replace("cpp", "hpp")
        hpp_file_found = CPPToHeaderLinkCreator._get_header_path(os.path.join(self.SOURCE_PATH, cpp_file))
        self.assertEqual(hpp_file_found, os.path.join(self.HEADER_PATH, hpp_file))

    def test_create_links(self):
        link_creator = self.get_cpp_to_header_link_creator()
        artifacts, links = link_creator.create_links()
        linked_files = set(self.CPP_FILES).difference(self.UNLINKED_FILES)
        self.assertEqual(len(links), len(linked_files))
        self.assertEqual(len(artifacts), 2 * len(linked_files))
        for file in linked_files:
            cpp_file_path = os.path.join("source", file)
            hpp_file_path = os.path.join("include", "iceoryx_platform", file.replace("cpp", "hpp"))
            self.assertIn(cpp_file_path, artifacts.keys())
            self.assertIn(hpp_file_path, artifacts.keys())
            link_exists = False
            for link in links.values():
                if link.source == cpp_file_path and link.target == hpp_file_path:
                    link_exists = True
                    break
            self.assertTrue(link_exists)

    def get_cpp_to_header_link_creator(self):
        return CPPToHeaderLinkCreator.from_dir_path(self.DIR_PATH, self.DIR_PATH)
