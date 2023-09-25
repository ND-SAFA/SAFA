package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import org.javatuples.Pair;

@Getter(AccessLevel.PROTECTED)
@Setter(AccessLevel.PROTECTED)
public abstract class GenerationJob extends CommitJob {
    private ProjectAppEntity projectAppEntity;
    private String projectSummary;

    protected GenerationJob(SafaUser user,
                            JobDbEntity jobDbEntity,
                            ServiceProvider serviceProvider,
                            ProjectCommitDefinition projectCommitDefinition) {
        super(user, jobDbEntity, serviceProvider, projectCommitDefinition, false);
    }

    /**
     * Retrieves project entities associated with project in commit.
     */
    @IJobStep(value = "Retrieving Project", position = 1)
    public void retrieveProject() {
        ProjectRetrievalService projectRetrievalService = this.getServiceProvider().getProjectRetrievalService();
        this.projectAppEntity = projectRetrievalService.getProjectAppEntity(
            this.getJobDbEntity().getUser(),
            getProjectVersion());
    }

    /**
     * Creates the project summary used across all generational jobs.
     */
    @IJobStep(value = "Summarizing Project Entities", position = 2)
    public void summarizeProjectEntities() {
        ProjectSummaryService service = this.getServiceProvider().getProjectSummaryService();
        Pair<String, List<ArtifactAppEntity>> summarizedEntities =
            service.summarizeProjectEntities(this.getUser(),
                getProjectVersion(),
                projectAppEntity.getArtifacts(),
                this.getDbLogger());
        this.projectSummary = summarizedEntities.getValue0();
        this.projectAppEntity.setArtifacts(summarizedEntities.getValue1());
    }
}
