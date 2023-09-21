package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class CreateProjectViaJsonJob extends CommitJob {
    private final ProjectAppEntity projectAppEntity;
    /**
     * Trace links to generate.
     */
    private final TGenRequestAppEntity TGenRequestAppEntity;

    public CreateProjectViaJsonJob(JobDbEntity jobDbEntity,
                                   ProjectAppEntity projectAppEntity,
                                   ServiceProvider serviceProvider,
                                   SafaUser user,
                                   TGenRequestAppEntity TGenRequestAppEntity) {
        super(jobDbEntity, serviceProvider, new ProjectCommitDefinition(user), true);
        this.TGenRequestAppEntity = TGenRequestAppEntity;
        this.projectAppEntity = projectAppEntity;
    }

    @IJobStep(value = "Creating Project", position = 1)
    public void createProjectStep() {
        createProjectAndCommit(getProjectCommitDefinition().getUser(),
            projectAppEntity.getName(),
            projectAppEntity.getDescription());
        ProjectVersion projectVersion = getProjectVersion();
        linkProjectToJob(projectVersion.getProject());
        this.projectAppEntity.setProjectVersion(projectVersion);
        this.TGenRequestAppEntity.setProjectVersion(projectVersion);

        getProjectCommitDefinition().addArtifacts(ModificationType.ADDED, this.projectAppEntity.getArtifacts());
        getProjectCommitDefinition().addTraces(ModificationType.ADDED, this.projectAppEntity.getTraces());
    }

    @IJobStep(value = "Generating Trace Links", position = 2)
    public void generateLinks(JobLogger logger) {
        TGenRequestAppEntity request = this.TGenRequestAppEntity;
        ProjectAppEntity projectAppEntity = new ProjectAppEntity(getProjectCommitDefinition());

        List<TraceAppEntity> generatedTraces = this.getServiceProvider()
            .getTraceGenerationService()
            .generateTraceLinks(request, projectAppEntity);
        getProjectCommitDefinition().addTraces(ModificationType.ADDED, generatedTraces);
        logger.log("Links generated: %s", generatedTraces.size());
    }
}
