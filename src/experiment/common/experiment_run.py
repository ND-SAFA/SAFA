import os
from typing import Dict, List, Tuple

from transformers import AutoModel, AutoTokenizer, BertForMaskedLM, DataCollatorForLanguageModeling, \
    LineByLineTextDataset, \
    Trainer, \
    TrainingArguments

from experiment.common.model_architecture import ModelArchitecture
from experiment.common.pretraining_data import PretrainingData
from experiment.common.project import Project
from experiment.common.run_mode import RunMode
from experiment.datasets.lhp_dataset import LHPDataset
from trace.jobs.trace_args_builder import TraceArgsBuilder
from trace.train.trace_trainer import TraceTrainer


class ExperimentRun:
    def __init__(self,
                 model_state_path: str,
                 pretraining: PretrainingData,
                 training_repositories: List[str],
                 metrics: List[str],
                 architecture: ModelArchitecture = ModelArchitecture.NL_BERT,
                 ):
        self.model_state_path = model_state_path
        self.training_repositories = training_repositories
        self.metrics = metrics
        self.architecture = architecture
        self.run_name = "_".join([model_state_path, pretraining.value])

    def push(self):
        model = AutoModel.from_pretrained(self.model_state_path)
        model.push_to_hub("thearod5/automotive")

    def perform_run(self,
                    output_dir: str,
                    run_mode_str: str,
                    **kwargs: Dict):
        run_mode = RunMode[run_mode_str.upper()]
        run_save_path = os.path.join(output_dir, self.run_name)
        training_data = self.__create_training_data(self.training_repositories)
        sources: List[Dict[str, str]] = training_data[0]
        targets: List[Dict[str, str]] = training_data[1]
        links: List[Tuple[str, str]] = training_data[2]

        # Trace Trainer
        lhp_dataset = LHPDataset()
        trace_args = TraceArgsBuilder(self.architecture.value,
                                      self.model_state_path,
                                      output_dir,
                                      sources,
                                      targets,
                                      links,
                                      metrics=self.metrics,
                                      validation_percentage=0,
                                      **kwargs).build()

        trace_trainer = TraceTrainer(args=trace_args)

        # Run
        if run_mode in [RunMode.TRAIN, RunMode.TRAINEVAL]:
            trace_trainer.perform_training()
            trace_trainer.save_model(run_save_path)
        if run_mode in [RunMode.EVAL, RunMode.TRAINEVAL]:
            eval_dataset = lhp_dataset.get_dataset(trace_args.model_generator).get_prediction_dataset()
            predictions = trace_trainer.perform_prediction(eval_dataset)
            print("Predictions", "-" * 25)
            for metric in self.metrics:
                print(metric, ":", predictions["metrics"][metric])

    def perform_language_modeling(self, dir_path: str, output_dir: str):
        self.run_name = "nl_bert_automotive"
        run_save_path = os.path.join(output_dir, self.run_name)
        os.mkdir(run_save_path)
        print("MODEL STATE PATH:", self.model_state_path)
        print("RUN NAME:", run_save_path)

        aggregate_file_path = self.collect_text_files(dir_path)
        tokenizer = AutoTokenizer.from_pretrained(self.model_state_path)

        dataset = LineByLineTextDataset(
            tokenizer=tokenizer,
            file_path=aggregate_file_path,
            block_size=128,
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm=True, mlm_probability=0.15
        )

        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=10,
            per_gpu_train_batch_size=64,
            save_steps=10_000,
            save_total_limit=2,
            prediction_loss_only=True,
        )

        model = BertForMaskedLM.from_pretrained(self.model_state_path)

        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=dataset,
        )
        tokenizer.save_vocabulary(run_save_path)
        trainer.train()

        trainer.save_model(run_save_path)

    def collect_text_files(self, dir_path: str) -> str:
        clean_text = ""
        for file_name in os.listdir(dir_path):
            if file_name in ["aggregate.txt", ".DS_Store"]:
                continue
            file_path = os.path.join(dir_path, file_name)
            clean_text += self.clean_text(file_path)
        aggregate_file_path = os.path.join(dir_path, "aggregate.txt")
        with open(aggregate_file_path, "w") as aggregate_file:
            aggregate_file.write(clean_text)
        return aggregate_file_path

    def clean_text(self, file_path: str):
        clean_lines = []
        for file_line in self.__read_text(file_path).split("\n"):
            if len(file_line.strip()) == 0:
                continue
            clean_lines.append(file_line)
        return "\n".join(clean_lines)

    def __read_text(self, file_path: str):
        with open(file_path, "r") as file:
            return file.read()

    def __create_training_data(self, training_repositories: List[str]):
        training_sources = []
        training_targets = []
        training_links = []
        for repo_name in training_repositories:
            project = Project(repo_name)
            for level in project.get_levels():
                training_sources.append(level.sources)
                training_targets.append(level.targets)
                training_links.extend(level.links)

        return training_sources, training_targets, training_links
