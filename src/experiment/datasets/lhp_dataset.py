import json
import os
from typing import Dict, List, Tuple

from trace.data.trace_dataset_creator import TraceDatasetCreator


class LHPDataset:
    PATH = "/Users/albertorodriguez/desktop/safa data/validation/LHP Test"

    def __init__(self):
        self.safety_goals = self.__read_safa_artifacts("sg.json")  # sg
        self.functional_requirements = self.__read_safa_artifacts("fsr.json")  # fr
        self.system_requirements = self.__read_safa_artifacts("SYS.json")  # sr
        self.software_requirements = self.__read_safa_artifacts("swr.json")  # swr
        self.hardware_requirements = self.__read_safa_artifacts("hwr.json")  # hwr
        self.fr2sg = self.__read_safa_traces("fsr2sg.json")
        self.sr2fr = self.__read_safa_traces("SYS2fsr.json")
        self.swr2sr = self.__read_safa_traces("swr2SYS.json")
        self.hwr2sr = self.__read_safa_traces("hwr2SYS.json")
        self.trace_matrices = [
            (self.hardware_requirements, self.system_requirements, self.hwr2sr),
            (self.software_requirements, self.system_requirements, self.swr2sr),
            (self.system_requirements, self.functional_requirements, self.sr2fr),
            (self.functional_requirements, self.safety_goals, self.fr2sg)
        ]

    def get_dataset(self, model_generator) -> TraceDatasetCreator:
        sources = [trace_matrix[0] for trace_matrix in self.trace_matrices]
        targets = [trace_matrix[1] for trace_matrix in self.trace_matrices]
        links = []
        for trace_matrix in self.trace_matrices:
            links.extend(trace_matrix[2])
        trace_dataset_creator = TraceDatasetCreator(
            source_layers=sources,
            target_layers=targets,
            true_links=links,
            model_generator=model_generator
        )
        return trace_dataset_creator

    def __read_safa_artifacts(self, data_file_name: str) -> Dict[str, str]:
        data_file_path = os.path.join(LHPDataset.PATH, data_file_name)
        data_file = self.__read_json_file(data_file_path)
        artifacts = {}
        for a in data_file["artifacts"]:
            artifacts[a["name"]] = a["body"]
        return artifacts

    def __read_safa_traces(self, data_file_name: str) -> List[Tuple[str, str]]:
        data_file_path = os.path.join(LHPDataset.PATH, data_file_name)
        data_file = self.__read_json_file(data_file_path)
        traces = []
        for t in data_file["traces"]:
            traces.append((t["sourceName"], t["targetName"]))
        return traces

    @staticmethod
    def __read_json_file(path_to_file: str):
        with open(path_to_file, "r") as json_file:
            json_content = json.loads(json_file.read())
            return json_content
