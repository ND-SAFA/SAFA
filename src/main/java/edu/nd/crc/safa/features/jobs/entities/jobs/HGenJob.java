package edu.nd.crc.safa.features.jobs.entities.jobs;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.GenerationPerformedEvent;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.StringUtil;

/**
 * Generates trace links between artifacts defined in request.
 */
public class HGenJob extends CommitJob {
    /**
     * The request to generate trace links.
     */
    private final HGenRequest hGenRequest;
    /**
     * The project version to commit summaries and generated links to.
     */
    private final ProjectVersion projectVersion;
    /**
     * The project entities used to construct request to generation server.
     */
    private ProjectAppEntity projectAppEntity;

    public HGenJob(SafaUser user,
                   JobDbEntity jobDbEntity,
                   ServiceProvider serviceProvider,
                   ProjectCommitDefinition projectCommitDefinition,
                   HGenRequest hGenRequest) {
        super(user, jobDbEntity, serviceProvider, projectCommitDefinition, false);
        this.hGenRequest = hGenRequest;
        this.projectVersion = projectCommitDefinition.getCommitVersion();
    }

    public static String getJobName(HGenRequest request) {
        String result = StringUtil.join(request.getTargetTypes(), ",");
        return String.format("Generating artifacts: %s", result);
    }

    @IJobStep(value = "Retrieving Project", position = 1)
    public void retrieveProjectEntities() {
        this.projectAppEntity =
            getServiceProvider().getProjectRetrievalService().getProjectAppEntity(
                this.getUser(),
                this.projectVersion
            );
    }

    @IJobStep(value = "Summarizing Project Entities", position = 2)
    public void summarizingProjectEntities() {
        this.getServiceProvider().getProjectSummaryService().summaryProjectAppEntity(
            this.getUser(),
            this.projectAppEntity,
            getDbLogger(),
            false
        );
        this.hGenRequest.setSummary(this.projectAppEntity.getSpecification());
    }

    @IJobStep(value = "Generating Artifacts", position = 3)
    public void generatingArtifacts() {
        ProjectCommitDefinition projectCommitDefinition = this.getServiceProvider().getHGenService()
            .generateHierarchy(
                this.projectVersion,
                this.hGenRequest,
                this.getDbLogger()
            );
        this.setProjectCommitDefinition(projectCommitDefinition);
    }

    @Override
    public void afterJob(boolean success) throws Exception {
        super.afterJob(success);

        if (success) {
            getServiceProvider().getEventPublisher()
                .publishEvent(new GenerationPerformedEvent(this, getUser(), projectVersion, hGenRequest));
        }
    }
}
