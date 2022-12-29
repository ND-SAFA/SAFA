import datetime
import time
from collections import namedtuple
from typing import Any, Dict, List, Optional, Union

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModel, get_constant_schedule_with_warmup

from config.override import overrides
from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from data.datasets.pre_train_dataset import PreTrainDataset
from data.datasets.trace_dataset import TraceDataset
from models.gan.discriminator import Discriminator
from models.gan.generator import Generator
from models.model_manager import ModelManager
from train.gan.gan_dataset_converter import GanDatasetConverter
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs


class GanTrainer(TraceTrainer):

    def __init__(self, args: TrainerArgs, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager,
                 **kwargs):
        """
        Generative Adviserial Network for training bert models.
        Github: https://github.com/crux82/ganbert-pytorch/blob/main/GANBERT_pytorch.ipynb
        """
        super().__init__(args, model_manager, trainer_dataset_manager, **kwargs)
        self.transformer = None

    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.train_dataset = self.to_gan_dataset(self.trainer_dataset_manager[DatasetRole.TRAIN],
                                                 self.trainer_dataset_manager[DatasetRole.PRE_TRAIN])
        if DatasetRole.EVAL in self.trainer_dataset_manager:
            self.eval_dataset = self.to_gan_dataset(self.trainer_dataset_manager[DatasetRole.EVAL])
        output = self.train(resume_from_checkpoint=checkpoint)
        return TraceTrainer.output_to_dict(output)

    @overrides(TraceTrainer)
    def train(self, resume_from_checkpoint: Optional[Union[str, bool]] = None,
              trial: Union["optuna.Trial", Dict[str, Any]] = None,
              ignore_keys_for_eval: Optional[List[str]] = None, **kwargs):
        device = GanTrainer.get_device()
        generator, discriminator, transformer = self.create_models()

        training_stats = []

        # Measure the total training time for the whole run.
        total_t0 = time.time()

        # models parameters
        transformer_vars = [i for i in transformer.parameters()]
        d_vars = transformer_vars + [v for v in discriminator.parameters()]
        g_vars = [v for v in generator.parameters()]

        # optimizer
        dis_optimizer = torch.optim.AdamW(d_vars, lr=self.trainer_args.learning_rate_discriminator)
        gen_optimizer = torch.optim.AdamW(g_vars, lr=self.trainer_args.learning_rate_generator)

        # scheduler
        if self.trainer_args.apply_scheduler:
            num_train_examples = len(self.train_dataset)
            num_train_steps = int(
                num_train_examples / self.trainer_args.train_batch_size * self.trainer_args.num_train_epochs)
            num_warmup_steps = int(num_train_steps * self.trainer_args.warmup_proportion)

            scheduler_d = get_constant_schedule_with_warmup(dis_optimizer,
                                                            num_warmup_steps=num_warmup_steps)
            scheduler_g = get_constant_schedule_with_warmup(gen_optimizer,
                                                            num_warmup_steps=num_warmup_steps)

        # For each epoch...
        for epoch_i in range(0, self.trainer_args.num_train_epochs):
            # ========================================
            #               Training
            # ========================================
            # Perform one full pass over the training set.
            print("")
            print('======== Epoch {:} / {:} ========'.format(epoch_i + 1, self.trainer_args.num_train_epochs))
            print('Training...')

            # Measure how long the training epoch takes.
            t0 = time.time()

            # Reset the total loss for this epoch.
            tr_g_loss = 0
            tr_d_loss = 0

            # Put the model into training mode.
            transformer.train()
            generator.train()
            discriminator.train()

            # For each batch of training data...
            for step, batch in enumerate(self.train_dataset):

                # Progress update every print_each_n_step batches.
                if step % self.trainer_args.print_each_n_step == 0 and not step == 0:
                    # Calculate elapsed time in minutes.
                    elapsed = self.format_time(time.time() - t0)

                    # Report progress.
                    print('  Batch {:>5,}  of  {:>5,}.    Elapsed: {:}.'.format(step, len(self.train_dataset), elapsed))

                # Unpack this training batch from our dataloader.
                b_input_ids = batch[0].to(device)
                b_input_mask = batch[1].to(device)
                b_labels = batch[2].to(device)
                b_label_mask = batch[3].to(device)

                real_batch_size = b_input_ids.shape[0]

                # Encode real data in the Transformer
                model_outputs = transformer(b_input_ids, attention_mask=b_input_mask)
                real_embeddings = model_outputs[-1]

                # Generate fake data that should have the same distribution of the ones
                # encoded by the transformer.
                # First noisy input are used in input to the Generator
                noise = torch.zeros(real_batch_size, self.trainer_args.noise_size, device=device).uniform_(0, 1)
                # Generate Fake data
                gen_embeddings = generator(noise)

                # Generate the output of the Discriminator for real and fake data.
                # First, we put together the output of the transformer and the generator
                dis_input = torch.cat([real_embeddings, gen_embeddings], dim=0)
                # Then, we select the output of the disciminator
                features, logits, probs = discriminator(dis_input)

                # Finally, we separate the discriminator's output for the real and fake
                # data
                features_list = torch.split(features, real_batch_size)
                dis_real_features = features_list[0]
                dis_fake_features = features_list[1]

                logits_list = torch.split(logits, real_batch_size)
                dis_real_logits = logits_list[0]
                dis_fake_logits = logits_list[1]

                probs_list = torch.split(probs, real_batch_size)
                dis_real_probs = probs_list[0]
                dis_fake_probs = probs_list[1]

                # ---------------------------------
                #  LOSS evaluation
                # ---------------------------------
                # Generator's LOSS estimation
                g_loss_d = -1 * torch.mean(torch.log(1 - dis_fake_probs[:, -1] + self.trainer_args.epsilon))
                g_feat_reg = torch.mean(
                    torch.pow(
                        torch.mean(dis_real_features, dim=0) - torch.mean(dis_fake_features, dim=0),
                        2))
                g_loss = g_loss_d + g_feat_reg

                # Disciminator's LOSS estimation
                logits = dis_real_logits[:, 0:-1]
                log_probs = F.log_softmax(logits, dim=-1)
                # The discriminator provides an output for labeled and unlabeled real data
                # so the loss evaluated for unlabeled data is ignored (masked)
                label2one_hot = torch.nn.functional.one_hot(b_labels, len(self.train_dataset))
                per_example_loss = -torch.sum(label2one_hot * log_probs, dim=-1)
                per_example_loss = torch.masked_select(per_example_loss, b_label_mask.to(device))
                labeled_example_count = per_example_loss.type(torch.float32).numel()

                # It may be the case that a batch does not contain labeled examples,
                # so the "supervised loss" in this case is not evaluated
                if labeled_example_count == 0:
                    dis_loss_supervised = 0
                else:
                    dis_loss_supervised = torch.div(torch.sum(per_example_loss.to(device)), labeled_example_count)

                dis_loss_unsupervised_real = -1 * torch.mean(
                    torch.log(1 - dis_real_probs[:, -1] + self.trainer_args.epsilon))
                dis_loss_unsupervised_fake = -1 * torch.mean(
                    torch.log(dis_fake_probs[:, -1] + self.trainer_args.epsilon))
                d_loss = dis_loss_supervised + dis_loss_unsupervised_real + dis_loss_unsupervised_fake

                # ---------------------------------
                #  OPTIMIZATION
                # ---------------------------------
                # Avoid gradient accumulation
                gen_optimizer.zero_grad()
                dis_optimizer.zero_grad()

                # Calculate weigth updates
                # retain_graph=True is required since the underlying graph will be deleted after backward
                g_loss.backward(retain_graph=True)
                d_loss.backward()

                # Apply modifications
                gen_optimizer.step()
                dis_optimizer.step()

                # A detail log of the individual losses
                # print("{0:.4f}\t{1:.4f}\t{2:.4f}\t{3:.4f}\t{4:.4f}".
                #      format(D_L_Supervised, D_L_unsupervised1U, D_L_unsupervised2U,
                #             g_loss_d, g_feat_reg))

                # Save the losses to print them later
                tr_g_loss += g_loss.item()
                tr_d_loss += d_loss.item()

                # Update the learning rate with the scheduler
                if self.trainer_args.apply_scheduler:
                    scheduler_d.step()
                    scheduler_g.step()

            # Calculate the average loss over all of the batches.
            avg_train_loss_g = tr_g_loss / len(self.train_dataset)
            avg_train_loss_d = tr_d_loss / len(self.train_dataset)

            # Measure how long this epoch took.
            training_time = self.format_time(time.time() - t0)

            print("")
            print("  Average training loss generetor: {0:.3f}".format(avg_train_loss_g))
            print("  Average training loss discriminator: {0:.3f}".format(avg_train_loss_d))
            print("  Training epcoh took: {:}".format(training_time))

            # ========================================
            #     TEST ON THE EVALUATION DATASET
            # ========================================
            # After the completion of each training epoch, measure our performance on
            # our test set.
            print("")
            print("Running Test...")

            t0 = time.time()

            # Put the model in evaluation mode--the dropout layers behave differently
            # during evaluation.
            transformer.eval()  # maybe redundant
            discriminator.eval()
            generator.eval()

            # Tracking variables
            total_test_accuracy = 0

            total_test_loss = 0
            nb_test_steps = 0

            all_preds = []
            all_labels_ids = []

            # loss
            nll_loss = torch.nn.CrossEntropyLoss(ignore_index=-1)

            if self.eval_dataset is None:
                continue
            # Evaluate data for one epoch
            for batch in self.eval_dataset:
                # Unpack this training batch from our dataloader.
                b_input_ids = batch[0].to(device)
                b_input_mask = batch[1].to(device)
                b_labels = batch[2].to(device)

                # Tell pytorch not to bother with constructing the compute graph during
                # the forward pass, since this is only needed for backprop (training).
                with torch.no_grad():
                    model_outputs = transformer(b_input_ids, attention_mask=b_input_mask)
                    real_embeddings = model_outputs[-1]
                    _, logits, probs = discriminator(real_embeddings)
                    ###log_probs = F.log_softmax(probs[:,1:], dim=-1)
                    filtered_logits = logits[:, 0:-1]
                    # Accumulate the test loss.
                    total_test_loss += nll_loss(filtered_logits, b_labels)

                # Accumulate the predictions and the input labels
                _, preds = torch.max(filtered_logits, 1)
                all_preds += preds.detach().cpu()
                all_labels_ids += b_labels.detach().cpu()

            # Report the final accuracy for this validation run.
            all_preds = torch.stack(all_preds).numpy()
            all_labels_ids = torch.stack(all_labels_ids).numpy()
            test_accuracy = np.sum(all_preds == all_labels_ids) / len(all_preds)
            print("  Accuracy: {0:.3f}".format(test_accuracy))

            # Calculate the average loss over all of the batches.
            avg_test_loss = total_test_loss / len(self.eval_dataset)
            avg_test_loss = avg_test_loss.item()

            # Measure how long the validation run took.
            test_time = self.format_time(time.time() - t0)

            print("  Test Loss: {0:.3f}".format(avg_test_loss))
            print("  Test took: {:}".format(test_time))

            # Record all statistics from this epoch.
            training_stats.append(
                {
                    'epoch': epoch_i + 1,
                    'Training Loss generator': avg_train_loss_g,
                    'Training Loss discriminator': avg_train_loss_d,
                    'Valid. Loss': avg_test_loss,
                    'Valid. Accur.': test_accuracy,
                    'Training Time': training_time,
                    'Test Time': test_time
                }
            )
        self.transformer = transformer
        Output = namedtuple('Output', ['stats'])
        output = Output(training_stats)
        return output

    def create_models(self):
        transformer = AutoModel.from_pretrained(self.model_manager.model_path)
        hidden_size = int(transformer.config.hidden_size)
        # Define the number and width of hidden layers
        hidden_levels_g = [hidden_size for i in range(0, self.trainer_args.n_hidden_layers_g)]
        hidden_levels_d = [hidden_size for i in range(0, self.trainer_args.n_hidden_layers_d)]

        # -------------------------------------------------
        #   Instantiate the Generator and Discriminator
        # -------------------------------------------------
        generator = Generator(noise_size=self.trainer_args.noise_size, output_size=hidden_size,
                              hidden_sizes=hidden_levels_g,
                              dropout_rate=self.trainer_args.out_dropout_rate)
        discriminator = Discriminator(input_size=hidden_size, hidden_sizes=hidden_levels_d,
                                      num_labels=len(self.train_dataset),
                                      dropout_rate=self.trainer_args.out_dropout_rate)

        # Put everything in the GPU if available
        if torch.cuda.is_available():
            generator.cuda()
            discriminator.cuda()
            transformer.cuda()
            if self.trainer_args.multi_gpu:
                transformer = torch.nn.DataParallel(transformer)
        return generator, discriminator, transformer

    def to_gan_dataset(self, trace_dataset: TraceDataset, pre_train_dataset: PreTrainDataset = None):
        """
        Extracts tensors from trace data containing different masks for architecture.
        :param trace_dataset: The data whose traces are converted to tensors.
        :param pre_train_dataset: The data whose text is used to create the distribution of words used
        by the generator
        :return: Dataloader containing tensors representing traces.
        """
        gan_dataset_converter = GanDatasetConverter(self.trainer_args,
                                                    trace_dataset,
                                                    pre_train_dataset=pre_train_dataset)
        return gan_dataset_converter.to_gan_dataset(self.model_manager)

    @staticmethod
    def format_time(elapsed: float):
        """
        Takes a time in seconds and returns a string hh:mm:ss
        :param elapsed: The number of seconds since the epoch time.
        :return: Formatted datatime.
        """
        elapsed_rounded = int(round(elapsed))  # Round to the nearest second.
        return str(datetime.timedelta(seconds=elapsed_rounded))  # Format as hh:mm:ss

    @staticmethod
    def get_device():
        """
        Returns the available device for running transformer.
        :return: GPU if available, CPU otherwise.
        """
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print('There are %d GPU(s) available.' % torch.cuda.device_count())
            print('We will use the GPU:', torch.cuda.get_device_name(0))
        else:
            print('No GPU available, using the CPU instead.')
            device = torch.device("cpu")
        return device
