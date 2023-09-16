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
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import org.javatuples.Pair;

@Getter(AccessLevel.PROTECTED)
@Setter(AccessLevel.PROTECTED)
public abstract class GenerationJob extends CommitJob {
    private ProjectAppEntity projectAppEntity;
    private ProjectVersion projectVersion;
    private String projectSummary;

    protected GenerationJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider,
                            ProjectCommitDefinition projectCommitDefinition) {
        super(jobDbEntity, serviceProvider, projectCommitDefinition);
    }

    @IJobStep(value = "Retrieve Project", position = 1)
    public void retrieveProject() {
        this.projectVersion = this.getProjectCommitDefinition().getCommitVersion();
        ProjectRetrievalService projectRetrievalService = this.getServiceProvider().getProjectRetrievalService();
        this.projectAppEntity = projectRetrievalService.getProjectAppEntity(
            this.getJobDbEntity().getUser(),
            projectVersion);
    }

    @IJobStep(value = "Create Project Summary", position = 2, requiredGeneration = true)
    public void summarizeProjectEntities() {
        ProjectSummaryService service = this.getServiceProvider().getProjectSummaryService();
        Pair<String, List<ArtifactAppEntity>> summarizedEntities = service.summarizeProjectEntities(this.projectVersion,
            projectAppEntity.getArtifacts(),
            this.getDbLogger());
        this.projectSummary = summarizedEntities.getValue0();
        this.projectAppEntity.setArtifacts(summarizedEntities.getValue1());
    }
}
