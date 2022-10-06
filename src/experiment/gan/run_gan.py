from gan.gan_args import GanArgs
from gan.gan_bert import GanBert
from gan.optimizer_args import OptimizerArgs
from gan.schedular_args import SchedulerArgs

if __name__ == "__main__":
    gan_args = GanArgs(train_examples, test_examples=test_examples, model_name=BASE_MODEL_NAME)
    optimizer_args = OptimizerArgs(num_train_epochs=10)
    scheduler_args = SchedulerArgs()

    gan_bert = GanBert(gan_args, optimizer_args, scheduler_args)
    bert_model, tokenizer = gan_bert.train()
    bert_model.save_pretrained(MODEL_EXPORT_PATH)
    tokenizer.save_pretrained(MODEL_EXPORT_PATH)
    tokenizer.save_vocabulary(MODEL_EXPORT_PATH)
