package edu.nd.crc.safa.features.jobs.entities.jobs;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.hgen.HGenService;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.StringUtil;

/**
 * Generates trace links between artifacts defined in request.
 */
public class HGenJob extends CommitJob {
    /**
     * The request to generate trace links.
     */
    HGenRequest hGenRequest;
    /**
     * The project version to commit summaries and generated links to.
     */
    ProjectVersion projectVersion;

    public HGenJob(JobDbEntity jobDbEntity,
                   ServiceProvider serviceProvider,
                   ProjectCommit projectCommit,
                   HGenRequest hGenRequest) {
        super(jobDbEntity, serviceProvider, projectCommit);
        this.hGenRequest = hGenRequest;
        this.projectVersion = projectCommit.getCommitVersion();
    }

    public static String getJobName(HGenRequest request) {
        String result = StringUtil.join(request.getTargetTypes(), ",");
        return String.format("Generating artifacts: %s", result);
    }

    @IJobStep(value = "Summarizing Project", position = 1)
    public void summarizeProject() {
        Project project = this.projectVersion.getProject();
        ProjectSummaryService service = this.serviceProvider.getProjectSummaryService();
        ProjectAppEntity projectAppEntity =
            this.serviceProvider.getProjectRetrievalService().getProjectAppEntity(this.projectVersion);
        service.generateProjectSummary(project, projectAppEntity.getArtifacts(), this.getDbLogger());
    }

    @IJobStep(value = "Generating Artifacts", position = 2)
    public void generatingArtifacts() {
        HGenService hGenService = this.serviceProvider.getHGenService();
        String summary = this.projectVersion.getProject().getSpecification();
        this.hGenRequest.setSummary(summary);
        ProjectCommit projectCommit = hGenService.generateHierarchy(this.projectVersion, this.hGenRequest);
        this.setProjectCommit(projectCommit);
    }
}
