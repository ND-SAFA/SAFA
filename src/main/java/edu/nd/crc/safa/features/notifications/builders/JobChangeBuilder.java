package edu.nd.crc.safa.features.notifications.builders;

import java.util.List;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

public class JobChangeBuilder extends AbstractEntityChangeBuilder {

    public JobChangeBuilder(SafaUser user, JobDbEntity job) {
        super(user.getUserId());
        String jobTopic = TopicCreator.getJobTopic(job.getId());
        this.getEntityChangeMessage().setTopic(jobTopic);
    }

    public JobChangeBuilder withJobUpdate(JobDbEntity job) {
        return (JobChangeBuilder) withEntityUpdate(Change.Entity.JOBS, List.of(job.getId()));
    }

    public JobChangeBuilder withJobDelete(JobDbEntity job) {
        return (JobChangeBuilder) withEntityDelete(Change.Entity.JOBS, List.of(job.getId()));
    }
}
