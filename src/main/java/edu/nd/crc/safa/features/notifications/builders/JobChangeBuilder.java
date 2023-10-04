package edu.nd.crc.safa.features.notifications.builders;

import java.util.List;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.users.entities.IUser;

public class JobChangeBuilder extends AbstractEntityChangeBuilder<JobChangeBuilder> {

    public JobChangeBuilder(IUser user, JobDbEntity job) {
        super(user.getUserId());
        String jobTopic = TopicCreator.getJobTopic(job.getId());
        this.getEntityChangeMessage().setTopic(jobTopic);
    }

    public JobChangeBuilder withJobUpdate(JobDbEntity job) {
        return (JobChangeBuilder) withEntityUpdate(NotificationEntity.JOBS, List.of(job.getId()));
    }

    public JobChangeBuilder withJobDelete(JobDbEntity job) {
        return (JobChangeBuilder) withEntityDelete(NotificationEntity.JOBS, List.of(job.getId()));
    }

    @Override
    protected JobChangeBuilder self() {
        return this;
    }
}
