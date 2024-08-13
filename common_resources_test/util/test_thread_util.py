from common_resources.tools.util.thread_util import ThreadUtil
from common_resources_test.base_tests.base_test import BaseTest


class TestThreadUtil(BaseTest):
    """
    Requirements: https://www.notion.so/nd-safa/thread_util-a4a22a3229314b49ac6532ff9d4b36ee?pvs=4
    """

    def test_multi_threaded(self):
        """
        Pipeline shall perform a series of similar jobs in a multi-threaded fashion
        """
        payloads = [1, 2]
        results = ThreadUtil.multi_thread_process("Testing multi-threaded jobs", payloads, lambda p: p,
                                                  n_threads=2,
                                                  collect_results=True,
                                                  max_attempts=1).results
        self.assertEqual(payloads, results)

    def test_re_tries(self):
        """
        Pipeline shall restart thread on error if re-tries are available
        """
        max_attempts = 2
        thread_sleep = 0.1
        n_threads = 2
        global_state = {"attempts": 0}

        def job_worker(payload):
            if global_state["attempts"] == 0:
                global_state["attempts"] += 1
                raise ValueError(f"Thread {payload}: This is a test error.")

            return payload

        payloads = [1, 2]

        results = ThreadUtil.multi_thread_process("Testing multi-threaded jobs", payloads, job_worker,
                                                  n_threads=n_threads,
                                                  collect_results=True,
                                                  max_attempts=max_attempts,
                                                  sleep_time=thread_sleep).results
        self.assertEqual(payloads, results)

    def test_assert_max_retries(self):
        """
        Pipeline fails if the maximum number of retries is reached.
        """
        max_attempts = 1
        thread_sleep = 0.1
        n_threads = 1

        def job_worker(payload):
            for i in range(max_attempts):
                raise ValueError("This is a test error.")

            return payload

        payloads = [1, 2]

        def try_threading():
            ThreadUtil.multi_thread_process("Testing multi-threaded jobs", payloads, job_worker,
                                            n_threads=n_threads,
                                            collect_results=True,
                                            max_attempts=max_attempts,
                                            sleep_time=thread_sleep)

        self.assert_error(try_threading, ValueError, "This is a test error.")
