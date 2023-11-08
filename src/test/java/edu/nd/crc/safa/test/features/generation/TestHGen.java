package edu.nd.crc.safa.test.features.generation;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.TraceLayer;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.hgen.HGenResponse;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.test.services.GenTestService;

import org.junit.jupiter.api.Test;

class TestHGen extends GenerationalTest {
    private final String sourceType = "code";
    private final String targetType = "user story";
    private final String generatedArtifactName = "generated-artifact";

    /**
     * Tests that code in project is summarized and updated during HGEN call.
     */
    @Test
    void testSingleArtifactGenerated() throws Exception {
        createProject();

        mockProjectSummaryResponse();
        mockHGenResponse();

        JobAppEntity job = this.rootBuilder
            .request(r -> r.generative().performHGen(getProjectVersion(), createHGenRequest())).get();

        refreshProject();
        verifyGeneratedArtifact();
        GenTestService.verifyJobAssociatedWithProject(this, job);
    }

    private void mockHGenResponse() {
        HGenResponse hgenResponse = createHGenResponse();
        getServer().setJobResponse(hgenResponse);
    }

    private HGenRequest createHGenRequest() {
        HGenRequest hgenRequest = new HGenRequest();
        hgenRequest.setTargetTypes(List.of(targetType));
        hgenRequest.setArtifacts(getProject()
            .getByArtifactType(sourceType)
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList()));
        return hgenRequest;
    }

    private HGenResponse createHGenResponse() {
        List<GenerationArtifact> artifacts = createGeneratedArtifacts();
        HGenResponse hgenResponse = new HGenResponse();
        hgenResponse.setArtifacts(artifacts);
        hgenResponse.setLayers(List.of(new TraceLayer("code", targetType)));
        return hgenResponse;
    }

    private List<GenerationArtifact> createGeneratedArtifacts() {
        ArtifactAppEntity a = new ArtifactAppEntity();
        a.setName(generatedArtifactName);
        a.setBody(GenTestService.createArtifactBody(a));
        a.setType(targetType);
        return List.of(new GenerationArtifact(a));
    }

    private void verifyGeneratedArtifact() {
        List<ArtifactAppEntity> generatedArtifacts = getProject().getByArtifactType(targetType);
        assertEquals(1, generatedArtifacts.size());
        ArtifactAppEntity generatedArtifact = generatedArtifacts.get(0);
        assertEquals(generatedArtifactName, generatedArtifact.getName());
        assertEquals(GenTestService.createArtifactBody(generatedArtifact), generatedArtifact.getBody());
    }
}
