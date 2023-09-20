package edu.nd.crc.safa.test.features.generation;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.TraceLayer;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.hgen.HGenResponse;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryResponse;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

class TestHGen extends AbstractGenerationTest {
    String targetType = "user story";
    String generatedArtifactName = "generated-artifact";

    @Test
    void testSummariesSet() throws Exception {
        String projectSummary = "project-summary";
        String sourceType = "code";

        ProjectVersion projectVersion = creationService.createProjectFromFiles(
            projectName,
            ProjectPaths.Resources.Tests.DRONE_SLICE
        );

        ProjectAppEntity projectAppEntity = retrievalService.getProjectAtVersion(projectVersion);

        ProjectSummaryResponse projectSummaryResponse = new ProjectSummaryResponse();
        List<GenerationArtifact> summarizedArtifacts = createGenerationArtifactsWithSummaries(
            projectAppEntity.getArtifacts());
        projectSummaryResponse.setArtifacts(summarizedArtifacts);
        projectSummaryResponse.setSummary(projectSummary);

        setProjectSummaryResponse(projectSummaryResponse);
        setHGenResponse(createHGenResponse(projectAppEntity));

        HGenRequest hgenRequest = new HGenRequest();
        hgenRequest.setTargetTypes(List.of(targetType));
        hgenRequest.setArtifacts(projectAppEntity
            .getByArtifactType(sourceType)
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList()));

        SafaRequest
            .withRoute(AppRoutes.HGen.GENERATE)
            .withVersion(projectVersion)
            .postWithJsonObject(hgenRequest);

//        ProjectAppEntity newProject = retrievalService.getProjectAtVersion(projectVersion);
//        List<ArtifactAppEntity> updatedCodeArtifacts = newProject
//            .getArtifacts().stream().filter(ArtifactAppEntity::isCode).collect(Collectors.toList());
//        updatedCodeArtifacts.forEach(a -> {
//            String artifactSummary = createArtifactSummary(a);
//            assertEquals(artifactSummary, a.getSummary());
//        });
//
//        List<ArtifactAppEntity> generatedArtifacts = newProject.getByArtifactType(targetType);
//        assertEquals(1, generatedArtifacts.size());
//        ArtifactAppEntity generatedArtifact = generatedArtifacts.get(0);
//        assertEquals(generatedArtifactName, generatedArtifact.getName());
//        assertEquals(createArtifactBody(generatedArtifact), generatedArtifact.getBody());
    }

    private List<GenerationArtifact> createGenerationArtifactsWithSummaries(List<ArtifactAppEntity> artifacts) {
        return artifacts
            .stream()
            .map(a -> {
                String artifactSummary = createArtifactSummary(a);
                a.setSummary(artifactSummary);
                return new GenerationArtifact(a);
            }).collect(Collectors.toList());
    }

    public HGenResponse createHGenResponse(ProjectAppEntity projectAppEntity) {
        List<GenerationArtifact> artifacts = createGeneratedArtifacts();
        HGenResponse hgenResponse = new HGenResponse();
        hgenResponse.setArtifacts(artifacts);
        hgenResponse.setLayers(List.of(new TraceLayer("code", targetType)));
        return hgenResponse;
    }

    public List<GenerationArtifact> createGeneratedArtifacts() {
        ArtifactAppEntity a = new ArtifactAppEntity();
        a.setName(generatedArtifactName);
        a.setBody(createArtifactBody(a));
        a.setType(targetType);
        return List.of(new GenerationArtifact(a));
    }

    private String createArtifactSummary(ArtifactAppEntity a) {
        return String.format("artifact-summary: %s", a.getName());
    }

    private String createArtifactBody(ArtifactAppEntity a) {
        return String.format("artifact-body: %s", a.getName());
    }
}
