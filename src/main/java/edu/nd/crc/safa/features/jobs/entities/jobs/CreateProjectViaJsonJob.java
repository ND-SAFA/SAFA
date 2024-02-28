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
import edu.nd.crc.safa.features.permissions.checks.billing.HasUnlimitedCreditsCheck;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectOwner;

public class CreateProjectViaJsonJob extends CommitJob {
    private final ProjectAppEntity projectAppEntity;
    /**
     * Trace links to generate.
     */
    private final TGenRequestAppEntity tgenRequestAppEntity;

    public CreateProjectViaJsonJob(SafaUser user,
                                   JobDbEntity jobDbEntity,
                                   ProjectAppEntity projectAppEntity,
                                   ServiceProvider serviceProvider,
                                   TGenRequestAppEntity tgenRequestAppEntity) {
        super(user, jobDbEntity, serviceProvider, new ProjectCommitDefinition(), true);
        this.tgenRequestAppEntity = tgenRequestAppEntity;
        this.projectAppEntity = projectAppEntity;
    }

    @IJobStep(value = "Creating Project", position = 1)
    public void createProjectStep() {
        ProjectOwner owner =
            ProjectOwner.fromUUIDs(getServiceProvider(), projectAppEntity.getTeamId(),
                projectAppEntity.getOrgId(), getUser());
        createProjectAndCommit(owner, projectAppEntity.getName(), projectAppEntity.getDescription());
        ProjectVersion projectVersion = getProjectVersion();
        linkProjectToJob(projectVersion.getProject());
        this.projectAppEntity.setProjectVersion(projectVersion);
        this.tgenRequestAppEntity.setProjectVersion(projectVersion);

        getProjectCommitDefinition().addArtifacts(ModificationType.ADDED, this.projectAppEntity.getArtifacts());
        getProjectCommitDefinition().addTraces(ModificationType.ADDED, this.projectAppEntity.getTraces());
    }

    @IJobStep(value = "Generating Trace Links", position = 2)
    public void generateLinks(JobLogger logger) {
        if (this.tgenRequestAppEntity.getRequests().isEmpty()) {
            return;
        }

        PermissionService permissionService = getServiceProvider().getPermissionService();
        Project project = getProjectVersion().getProject();

        permissionService.requirePermission(ProjectPermission.GENERATE, project, getUser());
        permissionService.requireAdditionalCheck(new HasUnlimitedCreditsCheck(), project, getUser());

        ProjectAppEntity projectAppEntity = new ProjectAppEntity(getProjectCommitDefinition());

        List<TraceAppEntity> generatedTraces = this.getServiceProvider()
            .getTraceGenerationService()
            .generateTraceLinks(this.tgenRequestAppEntity, projectAppEntity);
        getProjectCommitDefinition().addTraces(ModificationType.ADDED, generatedTraces);
        logger.log("Links generated: %s", generatedTraces.size());
    }
}
