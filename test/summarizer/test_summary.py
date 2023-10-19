import os
from copy import deepcopy

from tgen.common.util.prompt_util import PromptUtil
from tgen.summarizer.summary import Summary, SummarySection
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR


class TestSummary(BaseTest):
    SUMMARY = Summary({'Overview': SummarySection({'title': 'Overview',
                                                   'chunks': [
                                                       'SAFA is a software system for managing, visualizing, '
                                                       'and analyzing software projects.',
                                                       'It allows users to create projects containing artifacts like requirements.']}),
                       'Features': SummarySection({'title': 'Features',
                                                   'chunks': [
                                                       '## Trace Matrix Creation\nDefine allowed relationships between artifact types.',
                                                       '## Trace Matrix Editing\nEdit existing trace matrix rules.']}),
                       'Sub-systems': SummarySection({'title': 'Sub-systems', 'chunks': [
                           '## Access Management'
                           '\n- Functionality: Manages user access to data and features through roles, permissions, '
                           'authentication, and security.']}),
                       'Data Flow': SummarySection({'title': 'Data Flow', 'chunks': [
                           'The SAFA software system takes in data from # 10 various sources and transforms it to '
                           'provide traceability and project management capabilities.',
                           'User accounts and authentication data like emails and passwords are used '
                           'to create user accounts and manage access. '
                           'This user data flows into the access management subsystem to control what users can see and do.']})})

    def test_from_and_to_string(self):
        summary_string = str(self.SUMMARY)
        summary = Summary.from_string(summary_string)
        self.assertEqual(summary, self.SUMMARY)

        section_order = ["Data Flow", "DoesNotExit", "Overview"]
        summary_string = summary.to_string(section_order=section_order)
        self.assertTrue(summary_string.startswith(PromptUtil.as_markdown_header(section_order[0])))

        try:
            summary_string = summary.to_string(section_order=section_order, raise_exception_on_not_found=True)
            self.fail("did not raise exception on missing section")
        except KeyError:
            pass

    def test_load_and_save(self):
        filepath = os.path.join(TEST_OUTPUT_DIR, "summary.json")
        self.SUMMARY.save(filepath)
        summary = Summary.load_from_file(filepath)
        self.assertEqual(self.SUMMARY, summary)

    def test_reorder(self):
        summary = deepcopy(self.SUMMARY)
        section_order = ["Data Flow", "Features", "Overview"]
        summary.re_order_sections(section_order)
        for i, key in enumerate(summary.keys()):
            if i < len(section_order):
                self.assertEqual(key, section_order[i])


