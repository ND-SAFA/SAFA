package edu.nd.crc.safa.features.generation.summary;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

/**
 * Provides API for summarizing content.
 */
@AllArgsConstructor
@Service
public class SummaryService {
    private final GenApi genApi;
    private final ArtifactService artifactService;

    @NotNull
    private static List<ArtifactAppEntity> getArtifactAppEntities(List<ArtifactAppEntity> artifactAppEntities, List<GenerationArtifact> summarizedArtifacts) {
        Map<String, ArtifactAppEntity> artifactNameMap =
            ProjectDataStructures.createArtifactNameMap(artifactAppEntities);
        for (GenerationArtifact generationArtifact : summarizedArtifacts) {
            String artifactName = generationArtifact.getId();
            if (!artifactNameMap.containsKey(artifactName)) {
                System.out.println("Unable to find artifact:" + artifactName);
                continue;
            }
            String summary = generationArtifact.getSummary();
            if (summary == null) {
                System.out.println("Summary was null: " + artifactName);
                continue;
            }
            artifactNameMap.get(artifactName).setSummary(summary);
        }
        return artifactNameMap.values().stream().toList();
    }

    /**
     * Generates summarize for artifacts.
     *
     * @param request The summarization request.
     * @return List of summaries.
     */
    public List<ArtifactAppEntity> generateArtifactSummaries(SummarizeArtifactRequestDTO request) {
        return generateArtifactSummaries(request, null);
    }

    /**
     * Generates summaries for defined artifacts at specified version.
     *
     * @param request   The request containing artifacts and project version.
     * @param jobLogger The logger to store logs under.
     * @return List of artifact summaries in the same order as the order ids given.
     */
    public List<ArtifactAppEntity> generateArtifactSummaries(SummarizeArtifactRequestDTO request,
                                                             JobLogger jobLogger) {
        List<ArtifactAppEntity> artifactAppEntities = artifactService.getAppEntitiesByIds(request.getProjectVersion(),
            request.getArtifacts());
        System.out.println("Initial entities:\n" + artifactAppEntities);
        List<GenerationArtifact> generationArtifacts = artifactAppEntities.stream().map(GenerationArtifact::new)
            .collect(Collectors.toList());
        SummaryRequest tgenRequest = new SummaryRequest(generationArtifacts,
            request.getProjectSummary());
        List<GenerationArtifact> summarizedArtifacts = performGenArtifactSummaryRequest(tgenRequest, jobLogger);
        return getArtifactAppEntities(artifactAppEntities, summarizedArtifacts);
    }

    /**
     * Filters code artifacts and summarizes their bodies, adding them to the summary field.
     *
     * @param projectArtifacts Set of all artifacts in project.
     * @param projectSummary   The project summary to include while summarizing artifacts.
     * @return List of code artifacts with summaries populated.
     */
    public List<ArtifactAppEntity> addSummariesToCode(List<ArtifactAppEntity> projectArtifacts, String projectSummary) {
        return addSummariesToCode(projectArtifacts, projectSummary, null);
    }

    /**
     * Summarizes code artifacts without summaries.
     *
     * @param projectArtifacts Set of artifacts possibly containing code.
     * @param projectSummary   The project summary to include in the summarization.
     * @param logger           The logger used to store logs to.
     * @return List of summarized code artifacts. Project artifacts are also updated.
     */
    public List<ArtifactAppEntity> addSummariesToCode(List<ArtifactAppEntity> projectArtifacts,
                                                      String projectSummary,
                                                      JobLogger logger) {
        List<ArtifactAppEntity> codeArtifacts = projectArtifacts
            .stream()
            .filter(a -> a.isCode() && !a.hasSummary()).collect(Collectors.toList());

        if (codeArtifacts.isEmpty()) {
            return new ArrayList<>();
        }

        Map<String, ArtifactAppEntity> artifactMap = ProjectDataStructures.createArtifactNameMap(projectArtifacts);

        // Summaries returned in same order so id is not considered.
        List<GenerationArtifact> generationArtifacts = codeArtifacts
            .stream()
            .map(GenerationArtifact::new)
            .collect(Collectors.toList());
        SummaryRequest request = new SummaryRequest(generationArtifacts, projectSummary);
        List<GenerationArtifact> summarizedArtifacts = this.performGenArtifactSummaryRequest(request, logger);

        for (GenerationArtifact generationArtifact : summarizedArtifacts) {
            String artifactName = generationArtifact.getId();
            ArtifactAppEntity artifact = artifactMap.get(artifactName);
            artifact.setSummary(generationArtifact.getSummary());
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
    private List<GenerationArtifact> performGenArtifactSummaryRequest(SummaryRequest request,
                                                                      JobLogger jobLogger) {
        SummaryResponse response = this.genApi.generateArtifactSummaries(request, jobLogger);
        return response.getArtifacts();
    }
}
