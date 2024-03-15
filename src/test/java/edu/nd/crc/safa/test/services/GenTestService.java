package edu.nd.crc.safa.test.services;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.summary.SummaryResponse;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

public class GenTestService {
    public static List<GenerationArtifact> asGenArtifacts(GenerationalTest test) {
        return asGenArtifacts(test
            .getProject()
            .getArtifacts());
    }

    public static List<GenerationArtifact> asGenArtifacts(List<ArtifactAppEntity> artifacts) {
        return artifacts
            .stream()
            .map(GenerationArtifact::new)
            .collect(Collectors.toList());
    }

    public static void addSummaries(List<GenerationArtifact> artifacts) {
        artifacts.forEach(a -> {
            String artifactSummary = createArtifactSummary(a);
            a.setSummary(artifactSummary);
        });
    }

    public static SummaryResponse createProjectSummaryResponse(String projectSummary,
                                                               List<GenerationArtifact> artifacts) {
        SummaryResponse projectSummaryResponse = new SummaryResponse();
        projectSummaryResponse.setSummary(projectSummary);
        projectSummaryResponse.setArtifacts(artifacts);
        return projectSummaryResponse;
    }

    public static String createArtifactSummary(ArtifactAppEntity a) {
        return createArtifactSummary(a.getName());
    }

    public static String createArtifactSummary(GenerationArtifact a) {
        return createArtifactSummary(a.getId());
    }

    public static String createArtifactBody(ArtifactAppEntity a) {
        return String.format("artifact-body: %s", a.getName());
    }

    private static String createArtifactSummary(String name) {
        return String.format("artifact-summary: %s", name);
    }

    public static void verifyJobAssociatedWithProject(GenerationalTest test, JobAppEntity serverJob) throws Exception {
        Project project = test.getProjectVersion().getProject();
        List<JobAppEntity> jobs = CommonProjectRequests.getProjectJobs(project);
        assertEquals(1, jobs.size());
        JobAppEntity job = jobs.get(0);
        assertEquals(serverJob.getId(), job.getId());
    }
}
