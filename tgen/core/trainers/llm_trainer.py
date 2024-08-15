import json
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple, Union

from common_resources.data.dataframes.prompt_dataframe import PromptDataFrame
from common_resources.data.keys.prompt_keys import PromptKeys
from common_resources.data.keys.structure_keys import StructuredKeys, TraceKeys
from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.data.tdatasets.idataset import iDataset
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.llm.abstract_llm_manager import AbstractLLMManager, CONTENT_KEY, Message
from common_resources.llm.args.open_ai_args import OpenAIParams
from common_resources.llm.llm_responses import ClassificationResponse, GenerationResponse
from common_resources.llm.llm_task import LLMCompletionType
from common_resources.llm.prompts.prompt import Prompt
from common_resources.llm.prompts.prompt_builder import PromptBuilder
from common_resources.tools.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.llm_response_util import LLMResponseUtil

from tgen.chat.message_meta import MessageMeta
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.abstract_trainer import AbstractTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.metrics.metrics_manager import MetricsManager
from tgen.prompts.supported_prompts.classification_prompts import CLASSIFICATION_LABEL, CLASSIFICATION_SCORES, CURRENT_LABELS, \
    REVERSE_CATEGORIES


class LLMTrainer(AbstractTrainer):
    """
    Interfaces with open-ai server to fine-tune models and make predictions
    """

    def __init__(self, initial_state: LLMTrainerState):
        """
        Initializes the trainer with the necessary arguments for training and prediction
        :param initial_state: The current state of the trainer to use
        """
        super().__init__(initial_state.trainer_dataset_manager, trainer_args=initial_state.llm_manager.llm_args)
        self.state = initial_state

    def perform_training(self, completion_type: LLMCompletionType = LLMCompletionType.CLASSIFICATION) -> Any:
        """
        Handles training of the model
        :param completion_type: The type of completion task being performed.
        :return: The training response
        """
        train_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.TRAIN])
        training_file_id = train_dataset.get_project_file_id(self.llm_manager,
                                                             prompt_builder=self.prompt_builders)
        custom_params = {}
        instructions = {}
        include_classification_metrics = DatasetRole.VAL in self.trainer_dataset_manager
        if include_classification_metrics:
            instructions["include_classification_metrics"] = True
            instructions["prompt_builder"] = self.prompt_builders
            val_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.VAL])
            custom_params[OpenAIParams.VALIDATION_FILE] = val_dataset.get_project_file_id(
                self.llm_manager,
                prompt_builder=self.prompt_builders)

        res = self.llm_manager.make_fine_tune_request(completion_type=completion_type, training_file=training_file_id,
                                                      instructions=instructions, **custom_params)
        logger.info(res.events[-1].message)
        return res

    def perform_prediction(self,
                           dataset_role: DatasetRole = DatasetRole.EVAL,
                           datasets: Union[List[iDataset], iDataset] = None,
                           message_prompts: List[str] = None,
                           system_prompts: List[str] = None,
                           save_and_load_path: str = EMPTY_STRING,
                           raise_exception: bool = True) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param datasets: The dataset to use instead of from the dataset manager
        :param message_prompts: The list of prompts to use instead of making from the dataset
        :param system_prompts: List of existing system prompts if applicable.
        :param save_and_load_path: The path to load or save response
        :param raise_exception: If True, raises an exception if a response fails
        :return: THe prediction response
        """
        datasets = self._get_dataset(dataset_role, datasets)
        prompt_df, message_prompts, system_prompts = self._get_prompts_for_predictions(datasets, message_prompts, system_prompts)

        res = self._make_generation_request(self.state.llm_manager, message_prompts, system_prompts,
                                            self.state.completion_type, raise_exception, save_and_load_path)

        batch_responses = LLMResponseUtil.get_batch_responses(res)
        debugging = [p + NEW_LINE + str(r) for p, r in zip(message_prompts, batch_responses)]
        prompt_builder_map = OrderedDict({prompt_builder.id: prompt_builder
                                          for prompt_builder in (self.prompt_builders
                                                                 if isinstance(self.prompt_builders, list)
                                                                 else [self.prompt_builders])})
        prompt_builder_ids = prompt_df[PromptKeys.PROMPT_BUILDER_ID]
        if isinstance(res, ClassificationResponse):
            output = self._create_classification_output(res, datasets)
        elif isinstance(res, GenerationResponse):
            output = self._create_generation_output(res.batch_responses, prompt_builder_map, prompt_builder_ids)
        else:
            raise NotImplementedError(f"Unable to translate response to task: {type(res)}")
        return output

    @staticmethod
    def perform_chat(llm_manager: AbstractLLMManager,
                     chat_history: List[MessageMeta | Message],
                     system_prompts: str = None,
                     prompt_builder: PromptBuilder = None,
                     save_and_load_path: str = EMPTY_STRING,
                     raise_exception: bool = True) -> TracePredictionOutput:
        """
        Gets the next response in the chat.
        :param llm_manager: The llm manager to use for the chat.
        :param chat_history: The list of message sent between user and LLM.
        :param system_prompts: The system prompts for chat if applicable.
        :param prompt_builder: Used to parse response.
        :param save_and_load_path: The path to load or save response
        :param raise_exception: If True, raises an exception if a response fails
        :return: THe prediction response
        """
        if isinstance(chat_history[0], MessageMeta):
            chat_history = MessageMeta.to_llm_messages(chat_history)

        res = LLMTrainer._make_generation_request(llm_manager, chat_history, system_prompts, raise_exception=raise_exception,
                                                  save_and_load_path=save_and_load_path)
        if prompt_builder:
            output = LLMTrainer._create_generation_output(res.batch_responses, {prompt_builder.id: prompt_builder},
                                                          [prompt_builder.id])
        else:
            output = TracePredictionOutput(predictions=res.batch_responses, original_response=res.batch_responses)

        return output

    @staticmethod
    def predict_from_prompts(llm_manager: AbstractLLMManager,
                             prompt_builders: Union[PromptBuilder, List[PromptBuilder]] = None,
                             message_prompts: List[Prompt] = None,
                             system_prompts: List[Prompt] = None,
                             save_and_load_path: str = EMPTY_STRING,
                             raise_exception: bool = True,
                             **prompt_kwargs) -> TracePredictionOutput:
        """
        Makes generation predictions from a list of prompts
        :param llm_manager: The llm manager to use for predictions
        :param prompt_builders: The prompt builder to parse the response (or additionally create prompts)
        :param message_prompts: The list of prompts to use unless built from prompt_builder
        :param system_prompts: List of existing system prompts if applicable.
        :param save_and_load_path: Path used to load or save predictions
        :param raise_exception: If True, raises an exception if a response fails
        :param prompt_kwargs: Additional arguments used when building prompts (optionally)
        :return: The output from the predictions
        """
        if not isinstance(prompt_builders, list):
            prompt_builders = [prompt_builders]
        if not message_prompts:
            prompt_dicts = [pb.build(llm_manager.prompt_args, **prompt_kwargs) for pb in prompt_builders]
            message_prompts = [prompt[PromptKeys.PROMPT] for prompt in prompt_dicts]
            system_prompts = [prompt[PromptKeys.SYSTEM] for prompt in prompt_dicts]
        if not system_prompts:
            system_prompts = [None for _ in message_prompts]

        prompt_builder_ids = [pb.id for pb in prompt_builders]
        if len(prompt_builder_ids) != len(message_prompts):
            assert len(prompt_builder_ids) == 1, "Mismatch between # of prompts and builders"
            prompt_builder_ids = [prompt_builder_ids[0] for _ in message_prompts]

        prompt_df = PromptDataFrame({PromptKeys.PROMPT: message_prompts,
                                     PromptKeys.COMPLETION: [EMPTY_STRING for _ in message_prompts],
                                     PromptKeys.PROMPT_BUILDER_ID: prompt_builder_ids,
                                     PromptKeys.SYSTEM: system_prompts})
        dataset = PromptDataset(prompt_df=prompt_df)
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets(eval=dataset)
        initial_state = LLMTrainerState(llm_manager=llm_manager, prompt_builders=prompt_builders,
                                        trainer_dataset_manager=trainer_dataset_manager)
        trainer = LLMTrainer(initial_state)
        return trainer.perform_prediction(save_and_load_path=save_and_load_path,
                                          raise_exception=raise_exception,
                                          message_prompts=list(prompt_df[PromptKeys.PROMPT]),
                                          system_prompts=system_prompts)

    def cleanup(self) -> None:
        """
        Performs any necessary cleanup at the end of the job
        :return: None
        """
        pass

    @staticmethod
    def _make_generation_request(llm_manager: AbstractLLMManager,
                                 message_prompts: Union[str, List], system_prompts: Union[str, List] = None,
                                 completion_type: LLMCompletionType = LLMCompletionType.GENERATION,
                                 raise_exception: bool = False,
                                 save_and_load_path: str = None) -> Union[ClassificationResponse, GenerationResponse]:
        """
        Makes a request to the llm manager to generate a response.
        :param llm_manager: The llm manager to use.
        :param message_prompts: List of prompts to provide to the LLM.
        :param system_prompts: The system prompt to provide context in Anthropic convos.
        :param completion_type: The type of completion (generation or classification).
        :param raise_exception: If True, raises an exception if the request fails.
        :param save_and_load_path: Path to load or save responses to.
        :return: The response(s) from the model.
        """
        assert not save_and_load_path or save_and_load_path.endswith(FileUtil.YAML_EXT), "Response must be saved to yaml file."

        reloaded = LLMResponseUtil.reload_responses(save_and_load_path)
        missing_generations = isinstance(reloaded, List) or reloaded is None
        recent_prompt = LLMTrainer._get_most_recent_prompt(message_prompts)  # debugging

        if missing_generations:
            res = llm_manager.make_completion_request(
                completion_type=completion_type,
                prompt=message_prompts,
                system=system_prompts,
                original_responses=reloaded,
                raise_exception=raise_exception and not save_and_load_path)
            LLMResponseUtil.save_responses(res, save_and_load_path)
        else:
            res = reloaded
        LLMResponseUtil.get_failed_responses(res, raise_exception=raise_exception)
        return res

    @staticmethod
    def _get_most_recent_prompt(message_prompts: List | str) -> str:
        """
        Gets the first prompt for debugging.
        :param message_prompts: A list of prompts or messages or a single string.
        :return: The first prompt.
        """
        if isinstance(message_prompts, str):
            return message_prompts
        if isinstance(message_prompts, list):
            if isinstance(message_prompts[-1], Dict):
                return message_prompts[-1][CONTENT_KEY]
            else:
                return message_prompts[-1]

    @staticmethod
    def _create_generation_output(responses: List[str], prompt_builder_map: Dict[str, PromptBuilder],
                                  prompt_builder_ids: List[str]) -> TracePredictionOutput:
        """
        Creates the output for a generation
        :param responses: The response from the completion.
        :param prompt_builder_map: Map of id to the builder for each prompt builder responsible for building the prompts
        :param prompt_builder_ids: List of ids for prompt builders corresponding to the order of responses
        :return: The generation output.
        """
        if len(prompt_builder_map) == len(responses):  # reorder to match the order of the input prompt builders
            prompt_builder_id_to_response = {p_id: r for r, p_id in zip(responses, prompt_builder_ids)}
            responses = [prompt_builder_id_to_response[p_id] for p_id in prompt_builder_ids]
            prompt_builder_ids = prompt_builder_map.keys()
        predictions = []
        for i, (r, p_id) in enumerate(zip(responses, prompt_builder_ids)):
            try:
                pred = prompt_builder_map[p_id].parse_responses(r) if not isinstance(r, Exception) else r
            except Exception as e:
                print("Unable to parse response: r:")
                pred = None
            predictions.append(pred)
        return TracePredictionOutput(predictions=predictions,
                                     original_response=responses)  #

    def _create_classification_output(self, res: ClassificationResponse, datasets: List[PromptDataset]):
        """
        Creates the output for a classification
        :param res: The response from the completion
        :param datasets: The dataset being predicted on
        :param prompt_builder_map: Map of id to the builder for each prompt builder responsible for building the prompts
        :return: The classification output
        """
        all_prediction_entries = []
        all_metrics = {}
        all_label_ids = []
        for dataset in datasets:
            trace_dataset = dataset.trace_dataset
            trace_df = trace_dataset.trace_df
            prediction_entries = []

            scores = []
            labels = []
            classifications = []
            class2correct = {}
            for i, classification_item in enumerate(res.batch_responses):
                r = classification_item.text
                if isinstance(r, Exception):
                    continue
                entry = LLMResponseUtil.extract_labels(r, {label: label for label in CURRENT_LABELS})
                entry[CLASSIFICATION_LABEL] = entry[CLASSIFICATION_LABEL].upper().strip()

                score = self._extract_score(entry)
                trace_row = trace_df.iloc[i]
                label = trace_row[TraceKeys.LABEL.value]
                predicted_label = 1 if score >= 0.5 else 0
                correct_label = "correct" if label == predicted_label else "wrong"

                entry[StructuredKeys.SCORE] = score
                entry[TraceKeys.SOURCE.value] = trace_row[TraceKeys.SOURCE.value]
                entry[TraceKeys.TARGET.value] = trace_row[TraceKeys.TARGET.value]
                entry[TraceKeys.LABEL.value] = trace_row[TraceKeys.LABEL.value]

                self._update_classification_metrics(class2correct, correct_label, entry, label)
                scores.append(score)
                labels.append(label)
                classifications.append(entry["classification"])
                prediction_entries.append(entry)

            all_prediction_entries.extend(sorted(prediction_entries, key=lambda p: p[TraceKeys.SCORE.value], reverse=True))
            if trace_dataset is not None and len(trace_dataset.trace_df[TraceKeys.LABEL].unique()) == 2:
                metrics_manager = MetricsManager(trace_df=trace_dataset.trace_df,
                                                 predicted_similarities=scores)
                metrics = metrics_manager.eval(self.llm_manager.llm_args.metrics)
                if metrics:
                    logger.log_with_title("Candidate Metrics", repr(metrics))
                    logger.log_with_title("Class Counts", json.dumps(class2correct))
                all_metrics = {metric: all_metrics.get(metric, 0) + result for metric, result in metrics.items()}
                all_label_ids.extend(labels)
        all_metrics = {metric: all_metrics.get(metric, 0) / len(datasets) for metric, result in all_metrics.items()}
        output = TracePredictionOutput(prediction_entries=prediction_entries, metrics=all_metrics, label_ids=all_label_ids)
        return output

    def _get_prompts_for_predictions(self, datasets: Optional[List[PromptDataset]],
                                     message_prompts: List[str] = None,
                                     system_prompts: List[str] = None) -> Tuple[PromptDataFrame, List[str], List[Optional[str]]]:
        """
        Gets the prompts to use for prediction.
        :param datasets: Dataset to fill in artifacts and traces in the prompt.
        :param message_prompts: List of existing message prompts if applicable.
        :param system_prompts: List of existing system prompts if applicable.
        :return: The prompts dataframe and list of corresponding prompts.
        """
        if not message_prompts:
            prompt_df = self._create_prompts_for_prediction(datasets, self.prompt_builders)
            message_prompts = list(prompt_df[PromptKeys.PROMPT])
        else:
            if datasets:
                assert len(datasets) == 1, "If prompts are provided, only one dataset may be used"
                prompt_df = datasets[0].get_prompt_dataframe()
            else:
                system_prompts = [None for _ in message_prompts] if not system_prompts else system_prompts
                prompt_df = PromptDataFrame({PromptKeys.PROMPT: message_prompts,
                                             PromptKeys.SYSTEM: system_prompts})
        if not system_prompts:
            system_prompts = [DataFrameUtil.get_optional_value_from_df(row, PromptKeys.SYSTEM) for _, row in prompt_df.itertuples()]
        return prompt_df, message_prompts, system_prompts

    def _create_prompts_for_prediction(self, datasets: Union[PromptDataset, List[PromptDataset]],
                                       prompt_builders: Union[PromptBuilder, List[PromptBuilder]]) -> PromptDataFrame:
        """
        Gets the prompts used for the prediction
        :param datasets: The dataset to use when creating the prompts
        :param prompt_builders: The builder(s) to use to create the prompts
        :return: The prompts and the prompt dataframe
        """
        if not datasets:
            prompt_entries = []
            for prompt_builder in prompt_builders:
                prompt_dict = prompt_builder.build(self.state.llm_manager.prompt_args)
                prompt_dict[PromptKeys.PROMPT_BUILDER_ID] = prompt_builder.id
                prompt_entries.append(prompt_dict)
            return PromptDataFrame(prompt_entries)
        datasets = [datasets] if not isinstance(datasets, list) else datasets
        if len(datasets) > 1:
            prompt_df = PromptDataFrame()
            if len(prompt_builders) == 1:
                for dataset in datasets:
                    prompt_df = prompt_df.concat(self._create_prompts_for_prediction(dataset, prompt_builders))
            else:
                assert len(datasets) == len(prompt_builders), "Must supply a prompt builder per dataset " \
                                                              "or one prompt builder for all datasets"
                for dataset, prompt_builder in zip(datasets, prompt_builders):
                    prompt_df = prompt_df.concat(prompt_df, self._create_prompts_for_prediction(dataset, prompt_builder),
                                                 ignore_index=True)
        else:
            prompt_df = datasets[0].get_prompt_dataframe(prompt_builders=prompt_builders,
                                                         prompt_args=self.llm_manager.prompt_args)
        return prompt_df

    def _get_dataset(self, dataset_role: DatasetRole, datasets: Optional[Union[iDataset, List[iDataset]]]) -> Optional[List[iDataset]]:
        """
        Gets the dataset to use for a given role if applicable.
        :param dataset_role: The dataset role to get the dataset for.
        :param datasets: The datasets to use if not using the trainer dataset manager.
        :return: The dataset to use for a given role if applicable.
        """
        if datasets or self.trainer_dataset_manager and self.trainer_dataset_manager[dataset_role]:
            datasets = self.trainer_dataset_manager[dataset_role] if not datasets else datasets
            datasets = [datasets] if not isinstance(datasets, list) else datasets
            datasets: List[PromptDataset] = [self.convert_dataset_to_prompt_dataset(dataset) for dataset in datasets]
        else:
            assert self.state.completion_type != LLMCompletionType.CLASSIFICATION, "Need dataset for classification"
        return datasets

    @staticmethod
    def _extract_score(entry):
        """
        Extracts the score from the classification entry response.
        :param entry: Entry containing score or classification, to extract score from.
        :return: The final score as a float.
        """
        classification = entry["classification"]
        lower_bound, upper_bound = CLASSIFICATION_SCORES[classification]
        score_range = upper_bound - lower_bound
        try:
            confidence = float(entry["confidence"])
            if classification in REVERSE_CATEGORIES:
                score = upper_bound - (confidence * score_range)
            else:
                score = (confidence * score_range) + lower_bound
        except:
            score = lower_bound
            logger.info("Processing link with missing score.")

        return score

    @staticmethod
    def _update_classification_metrics(class2correct, correct_label, entry, label) -> None:
        """
        Updates the classification metrics on the categories of traces.
        :param class2correct: The current metrics on the classes.
        :param correct_label: The correct label of the entry.
        :param entry: The
        :param label:
        :return:
        """
        classification = entry["classification"]
        if classification not in class2correct:
            class2correct[classification] = {c: 0 for c in [0, 1]}
        class2correct[classification][label] += 1

    def __getattr__(self, item: str) -> Any:
        """
        Gets an item from its state since it does not exist in trainer
        :param item: The name of the item to get
        :return: The item
        """
        if not item.startswith("__"):
            try:
                return getattr(self.state, item)
            except Exception as e:
                pass
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")
