package edu.nd.crc.safa.test.features.generation;

import static edu.nd.crc.safa.test.services.GenTestService.asGenArtifacts;

import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.summary.SummaryResponse;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.AbstractRemoteApiTest;
import edu.nd.crc.safa.test.server.TGenMockServer;
import edu.nd.crc.safa.test.services.GenTestService;

import lombok.Getter;

public abstract class GenerationalTest extends AbstractRemoteApiTest<TGenMockServer> {
    @Getter
    private final String projectSummary = "project-summary";
    private ProjectAppEntity projectAppEntity;

    @Override
    public TGenMockServer createServer() {
        return new TGenMockServer();
    }

    protected void createProject() throws Exception {
        String projectPath = ProjectPaths.Resources.Tests.DRONE_SLICE;
        ProjectVersion projectVersion = creationService.createProjectFromFiles(projectName, projectPath);
        this.projectAppEntity = retrievalService.getProjectAtVersion(projectVersion);
    }

    public ProjectVersion getProjectVersion() {
        assert this.projectAppEntity != null;
        return this.projectAppEntity.getProjectVersion();
    }

    protected void refreshProject() {
        ProjectVersion projectVersion = projectVersionRepository.findByVersionId(getProjectVersion().getVersionId());
        this.projectAppEntity = retrievalService.getProjectAtVersion(projectVersion);
    }

    public ProjectAppEntity getProject() {
        return this.projectAppEntity;
    }

    protected void mockProjectSummaryResponse() {
        mockProjectSummaryResponse(projectSummary);
    }

    protected void mockProjectSummaryResponse(String projectSummary) {
        List<GenerationArtifact> artifacts = asGenArtifacts(this);
        GenTestService.addSummaries(artifacts);
        SummaryResponse projectSummaryResponse = GenTestService.createProjectSummaryResponse(
            projectSummary,
            artifacts);
        getServer().setJobResponse(projectSummaryResponse);
    }
}
