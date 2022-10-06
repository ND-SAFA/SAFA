import datetime
import time

import numpy as np
import torch
import torch.nn.functional as F
from transformers import get_constant_schedule_with_warmup

from gan.gan_args import GanArgs
from gan.gan_builder import GanBuilder
from gan.optimizer_args import OptimizerArgs
from gan.schedular_args import SchedulerArgs


class GanBert:
    """
    Generative Adviserial Network for training bert models.
    Github: https://github.com/crux82/ganbert-pytorch/blob/main/GANBERT_pytorch.ipynb
    """

    def __init__(self, args: GanArgs, optimizer_args: OptimizerArgs, scheduler_args: SchedulerArgs):
        self.args = args
        self.optimizer_args = optimizer_args
        self.scheduler_args = scheduler_args

    def train(self):
        # Step - Build Gan
        gan_builder = GanBuilder(self.args, self.optimizer_args)
        generator, discriminator, transformer, dataset, tokenizer, device = gan_builder.build()

        # Step - Load dataset from args
        train_dataloader, test_dataloader, train_examples = dataset.build()

        training_stats = []

        # Measure the total training time for the whole run.
        total_t0 = time.time()

        # models parameters
        transformer_vars = [i for i in transformer.parameters()]
        d_vars = transformer_vars + [v for v in discriminator.parameters()]
        g_vars = [v for v in generator.parameters()]

        # optimizer
        dis_optimizer = torch.optim.AdamW(d_vars, lr=self.optimizer_args.learning_rate_discriminator)
        gen_optimizer = torch.optim.AdamW(g_vars, lr=self.optimizer_args.learning_rate_generator)

        # scheduler
        if self.scheduler_args.apply_scheduler:
            num_train_examples = len(train_examples)
            num_train_steps = int(num_train_examples / self.args.batch_size * self.optimizer_args.num_train_epochs)
            num_warmup_steps = int(num_train_steps * self.scheduler_args.warmup_proportion)

            scheduler_d = get_constant_schedule_with_warmup(dis_optimizer,
                                                            num_warmup_steps=num_warmup_steps)
            scheduler_g = get_constant_schedule_with_warmup(gen_optimizer,
                                                            num_warmup_steps=num_warmup_steps)

        # For each epoch...
        for epoch_i in range(0, self.optimizer_args.num_train_epochs):
            # ========================================
            #               Training
            # ========================================
            # Perform one full pass over the training set.
            print("")
            print('======== Epoch {:} / {:} ========'.format(epoch_i + 1, self.optimizer_args.num_train_epochs))
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
            for step, batch in enumerate(train_dataloader):

                # Progress update every print_each_n_step batches.
                if step % self.args.print_each_n_step == 0 and not step == 0:
                    # Calculate elapsed time in minutes.
                    elapsed = self.format_time(time.time() - t0)

                    # Report progress.
                    print('  Batch {:>5,}  of  {:>5,}.    Elapsed: {:}.'.format(step, len(train_dataloader), elapsed))

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
                noise = torch.zeros(real_batch_size, self.args.noise_size, device=device).uniform_(0, 1)
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
                g_loss_d = -1 * torch.mean(torch.log(1 - dis_fake_probs[:, -1] + self.optimizer_args.epsilon))
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
                label2one_hot = torch.nn.functional.one_hot(b_labels, len(dataset.label_list))
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
                    torch.log(1 - dis_real_probs[:, -1] + self.optimizer_args.epsilon))
                dis_loss_unsupervised_fake = -1 * torch.mean(
                    torch.log(dis_fake_probs[:, -1] + self.optimizer_args.epsilon))
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
                if self.scheduler_args.apply_scheduler:
                    scheduler_d.step()
                    scheduler_g.step()

            # Calculate the average loss over all of the batches.
            avg_train_loss_g = tr_g_loss / len(train_dataloader)
            avg_train_loss_d = tr_d_loss / len(train_dataloader)

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

            # Evaluate data for one epoch
            for batch in test_dataloader:
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
            avg_test_loss = total_test_loss / len(test_dataloader)
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
        return transformer, tokenizer

    @staticmethod
    def format_time(elapsed):
        """
        Takes a time in seconds and returns a string hh:mm:ss
        :param elapsed: TODO
        :return:
        """
        # Round to the nearest second.
        elapsed_rounded = int(round(elapsed))
        # Format as hh:mm:ss
        return str(datetime.timedelta(seconds=elapsed_rounded))
