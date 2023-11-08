package edu.nd.crc.safa.test.features.generation;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.generation.tgen.TGenResponse;
import edu.nd.crc.safa.features.generation.tgen.entities.ArtifactLevelRequest;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.generation.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.test.services.GenTestService;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.junit.jupiter.api.Test;

class TestTGen extends GenerationalTest {
    private final String childName = "FullMissionPlan.java";
    private final String parentName = "RE-541";
    private final String explanation = "explanation";
    private final double score = 0.7;
    private final String childType = "code";
    private final String parentType = "requirements";

    /**
     * Tests that client is able to generate trace links
     */
    @Test
    void testGenerateTraceLinks() throws Exception {
        createProject();

        mockProjectSummaryResponse();
        mockTGenResponse();

        TGenRequestAppEntity request = createTGenRequest();

        JobAppEntity job = this.rootBuilder.request(c -> c.generative().performTGen(request)).get();

        refreshProject();

        List<TraceAppEntity> generatedTraces = CommonProjectRequests.getGeneratedLinks(getProjectVersion());
        assertThat(generatedTraces).hasSize(1);

        verifyGeneratedLink(generatedTraces.get(0));
        GenTestService.verifyJobAssociatedWithProject(this, job);
    }

    private TGenRequestAppEntity createTGenRequest() {
        TGenRequestAppEntity request = new TGenRequestAppEntity();
        request.setRequests(List.of(createTracingRequest()));
        request.setProjectVersion(getProjectVersion());
        return request;
    }

    private ArtifactLevelRequest createArtifactLevelRequest() {
        ArtifactLevelRequest artifactLevel = new ArtifactLevelRequest();
        artifactLevel.setSource(childType);
        artifactLevel.setTarget(parentType);
        return artifactLevel;
    }

    private TracingRequest createTracingRequest() {
        TracingRequest tracingRequest = new TracingRequest();
        tracingRequest.setArtifactLevels(List.of(createArtifactLevelRequest()));
        return tracingRequest;
    }

    private void mockTGenResponse() {
        TGenResponse response = new TGenResponse();
        response.setPredictions(List.of(getGeneratedLink()));
        getServer().setJobResponse(response);
    }

    private void verifyGeneratedLink(TraceAppEntity link) {
        assertThat(link.getScore()).isEqualTo(score);
        assertThat(link.getTargetName()).isEqualTo(parentName);
        assertThat(link.getSourceName()).isEqualTo(childName);
        assertThat(link.getExplanation()).isEqualTo(explanation);
        assertThat(link.getApprovalStatus()).isEqualTo(ApprovalStatus.UNREVIEWED);
        assertThat(link.getTraceType()).isEqualTo(TraceType.GENERATED);
    }

    private GenerationLink getGeneratedLink() {
        GenerationLink link = new GenerationLink();
        link.setSource(childName);
        link.setTarget(parentName);
        link.setExplanation(explanation);
        link.setScore(score);
        return link;
    }
}
