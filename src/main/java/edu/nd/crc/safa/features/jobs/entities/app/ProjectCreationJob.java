package edu.nd.crc.safa.features.jobs.entities.app;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.EntityVersionService;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.layout.entities.app.ProjectLayout;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public class ProjectCreationJob extends AbstractJob {
    /**
     * The project version of the
     */
    ProjectCommit projectCommit;
    /**
     * The entities created during job.
     */
    ProjectAppEntity projectAppEntity;
    /**
     * The service used for creating entities.
     */
    EntityVersionService entityVersionService;
    /**
     * Whether entities created should be treated as the complete set of entities
     */
    boolean asCompleteSet;

    public ProjectCreationJob(JobDbEntity jobDbEntity,
                              ServiceProvider serviceProvider,
                              ProjectCommit projectCommit) {
        super(jobDbEntity, serviceProvider);
        this.projectCommit = projectCommit;
        this.entityVersionService = serviceProvider.getEntityVersionService();
        this.asCompleteSet = ProjectVariables.PROJECT_CREATION_AS_COMPLETE_SET;// TODO: Use flag from request
    }

    public void savingArtifacts() throws SafaError {
        this.entityVersionService.addArtifactsAtVersionAndSaveErrors(
            projectCommit.getCommitVersion(),
            projectCommit.getArtifacts().getAdded(),
            this.asCompleteSet);
    }

    public void savingTraces() throws SafaError {
        this.entityVersionService.setTracesAtVersionAndSaveErrors(
            projectCommit.getCommitVersion(),
            projectCommit.getTraces().getAdded(),
            this.asCompleteSet);
    }

    public void generatingLayout() {
        AppEntityRetrievalService appEntityRetrievalService = serviceProvider.getAppEntityRetrievalService();
        this.projectAppEntity = appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(
            projectCommit.getCommitVersion()
        );
        ProjectLayout projectLayout = new ProjectLayout(projectAppEntity, serviceProvider);
        projectLayout.createLayoutForAllDocuments();
    }

    @Override
    public void done() {
        this.jobDbEntity.setCompletedEntityId(projectCommit.getCommitVersion().getVersionId());
        super.done();
    }
}
