package edu.nd.crc.safa.features.summary;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.tgen.TGen;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides API for summarizing content.
 */
@AllArgsConstructor
@Service
public class SummaryService {
    SafaRequestBuilder safaRequestBuilder;

    /**
     * Generates summarize for artifacts.
     *
     * @param request The summarization request.
     * @return List of summaries.
     */
    public List<String> generateSummaries(SummarizeRequestDTO request) {
        return generateSummaries(request, null);
    }

    public List<String> generateSummaries(SummarizeRequestDTO request, JobLogger jobLogger) {
        List<TGenSummaryArtifact> artifacts = new ArrayList<>();
        for (TGenSummaryArtifact artifact : request.getArtifacts()) {
            if (artifact.getId() == null) { // For non-artifacts, ad-hoc id is created for them.
                artifact.setId(artifact.getName());
            }
            TGenSummaryArtifactType artifactType = TGenSummaryArtifactType.getArtifactType(artifact.getName());
            artifact.setType(artifactType);
            artifacts.add(artifact);
        }
        TGen tgen = new TGen(safaRequestBuilder);
        TGenSummaryRequest tgenRequest = new TGenSummaryRequest(artifacts, request.getModel());
        TGenSummaryResponse response = tgen.generateSummaries(tgenRequest, jobLogger);

        List<String> summaries = new ArrayList<>();
        for (TGenSummaryArtifact artifact : response.getArtifacts().values()) {
            summaries.add(artifact.getContent());
        }
        return summaries;
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
        List<TGenSummaryArtifact> summaryArtifacts = codeArtifacts.stream().map(a -> new TGenSummaryArtifact(
            a.getTraceableId(), // avoid using id if artifact is not yet created.
            a.getName(),
            a.getBody(),
            TGenSummaryArtifactType.getArtifactType(a.getName()))
        ).collect(Collectors.toList());
        List<String> summarizedArtifacts = this.generateSummaries(new SummarizeRequestDTO(summaryArtifacts), logger);
        for (int i = 0; i < codeArtifacts.size(); i++) {
            String artifactSummary = summarizedArtifacts.get(i);
            ArtifactAppEntity artifact = codeArtifacts.get(i);
            artifact.setSummary(artifactSummary);
        }

        return codeArtifacts;
    }
}
