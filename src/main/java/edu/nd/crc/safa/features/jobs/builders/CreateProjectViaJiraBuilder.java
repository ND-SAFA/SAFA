package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AccessLevel;
import lombok.Getter;

/**
 * Builds job for pulling issues from JIRA and updating project.
 */
public class CreateProjectViaJiraBuilder extends AbstractJobBuilder {
    @Getter(AccessLevel.PROTECTED)
    private JiraIdentifier jiraIdentifier;

    public CreateProjectViaJiraBuilder(
        ServiceProvider serviceProvider,
        JiraIdentifier jiraIdentifier,
        SafaUser user
    ) {
        super(serviceProvider, user);
        this.jiraIdentifier = jiraIdentifier;
    }

    @Override
    protected AbstractJob constructJobForWork() {
        // Step - Create jira project creation job
        return new CreateProjectViaJiraJob(
            this.getJobDbEntity(),
            getServiceProvider(),
            this.jiraIdentifier,
            this.getUser()
        );
    }

    @Override
    protected String getJobName() {
        return CreateProjectViaJiraJob.createJobName(this.jiraIdentifier);
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return CreateProjectViaJiraJob.class;
    }
}
