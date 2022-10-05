class SchedulerArgs:
    """
    Arguments to the scheduler.
    TODO : Describe what a scheduler does.
    """

    def __init__(self, apply_scheduler=False, warmup_proportion=0.1):
        self.apply_scheduler = apply_scheduler
        self.warmup_proportion = warmup_proportion
