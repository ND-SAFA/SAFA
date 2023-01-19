import os.path

import torch
from accelerate import Accelerator
from transformers import AutoModel, Trainer, TrainingArguments


def use_accelerator():
    accelerator = Accelerator()
    optimizer = torch.optim.Adam(model.parameters())
    my_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.99)
    my_model, my_optimizer = accelerator.prepare(model, optimizer)

    # Register the LR scheduler
    accelerator.register_for_checkpointing(my_scheduler)

    # Save the starting state
    accelerator.save_state(test_path)


if __name__ == "__main__":
    test_path = "~/desktop/safa/test"
    base_model = "bert-base-uncased"

    test_path = os.path.expanduser(test_path)
    checkpoint_path = os.path.join(test_path, "checkpoint-0")
    model = AutoModel.from_pretrained(checkpoint_path)

    training_arguments = TrainingArguments(output_dir=checkpoint_path)
    trainer = Trainer(model, training_arguments)
    trainer._load_from_checkpoint(checkpoint_path)
    # trainer.create_optimizer()
    # trainer.create_scheduler(420)
    trainer._save_checkpoint(model, None)
    # trainer.save_model()
