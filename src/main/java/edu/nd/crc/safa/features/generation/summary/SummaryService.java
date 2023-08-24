package edu.nd.crc.safa.features.generation.summary;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.generation.api.GenerationApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides API for summarizing content.
 */
@AllArgsConstructor
@Service
public class SummaryService {
    private final GenerationApi generationApi;
    private final ArtifactService artifactService;

    /**
     * Generates summarize for artifacts.
     *
     * @param request The summarization request.
     * @return List of summaries.
     */
    public List<String> generateArtifactSummaries(SummarizeArtifactRequestDTO request) {
        return generateArtifactSummaries(request, null);
    }

    /**
     * Generates summaries for defined artifacts at specified version.
     *
     * @param request   The request containing artifacts and project version.
     * @param jobLogger The logger to store logs under.
     * @return List of artifact summaries in the same order as the order ids given.
     */
    public List<String> generateArtifactSummaries(SummarizeArtifactRequestDTO request, JobLogger jobLogger) {
        List<ArtifactAppEntity> artifactAppEntities = artifactService.getAppEntitiesById(request.getProjectVersion(),
            request.getArtifacts());
        List<GenerationArtifact> generationArtifacts = artifactAppEntities.stream().map(GenerationArtifact::new).collect(Collectors.toList());
        GenArtifactSummaryRequest tgenRequest = new GenArtifactSummaryRequest(generationArtifacts, request.getProjectSummary());
        return performGenArtifactSummaryRequest(tgenRequest, jobLogger);
    }

    /**
     * Filters code artifacts and summarizes their bodies, adding them to the summary field.
     *
     * @param projectArtifacts Set of all artifacts in project.
     * @return List of code artifacts with summaries populated.
     */
    public List<ArtifactAppEntity> addSummariesToCode(List<ArtifactAppEntity> projectArtifacts) {
        return addSummariesToCode(projectArtifacts, null);
    }

    public List<ArtifactAppEntity> addSummariesToCode(List<ArtifactAppEntity> projectArtifacts, JobLogger logger) {
        List<ArtifactAppEntity> codeArtifacts = projectArtifacts
            .stream()
            .filter(a -> TGenSummaryArtifactType.isCode(a.getName()) && !a.hasSummary()).collect(Collectors.toList());
        if (codeArtifacts.isEmpty()) {
            return new ArrayList<>();
        }
        // Summaries returned in same order so id is not considered.
        List<GenerationArtifact> generationArtifacts = codeArtifacts.stream().map(GenerationArtifact::new).collect(Collectors.toList());
        GenArtifactSummaryRequest request = new GenArtifactSummaryRequest(generationArtifacts);
        List<String> summarizedArtifacts = this.performGenArtifactSummaryRequest(request, logger);
        for (int i = 0; i < codeArtifacts.size(); i++) {
            String artifactSummary = summarizedArtifacts.get(i);
            ArtifactAppEntity artifact = codeArtifacts.get(i);
            artifact.setSummary(artifactSummary);
        }

        return codeArtifacts;
    }

    /**
     * Performs the generation request to summarize artifacts.
     *
     * @param request   The request containing artifacts to summarize and potentially a project summary.
     * @param jobLogger The logger to store logs under.
     * @return The list of summaries.
     */
    private List<String> performGenArtifactSummaryRequest(GenArtifactSummaryRequest request, JobLogger jobLogger) {
        TGenSummaryResponse response = this.generationApi.generateArtifactSummaries(request, jobLogger);
        List<String> summaries = new ArrayList<>();
        for (GenerationArtifact artifact : response.getArtifacts()) {
            summaries.add(artifact.getSummary());
        }
        return summaries;
    }
}
