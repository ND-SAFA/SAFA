package edu.nd.crc.safa.features.summary;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.tgen.TGen;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;

import org.springframework.stereotype.Service;

/**
 * Provides API for summarizing content.
 */
@Service
public class SummaryService {
    /**
     * Generates summarize for artifacts.
     *
     * @param request The summarization request.
     * @return List of summaries.
     */
    public List<String> generateSummaries(SummarizeRequestDTO request) {
        BaseGenerationModels baseModel = request.getModel();
        TGen controller = baseModel.createTGenController();
        List<TGenSummaryArtifact> artifacts = new ArrayList<>();
        for (TGenSummaryArtifact artifact : request.getArtifacts()) {
            if (artifact.getId() == null) { // HOTFIX: set id to name. Name may not always be unique going forward.
                artifact.setId(artifact.getName());
            }
            TGenSummaryArtifactType artifactType = TGenSummaryArtifactType.getArtifactType(artifact.getName());
            artifact.setType(artifactType);
            artifacts.add(artifact);
        }
        TGenSummaryRequest tgenRequest = new TGenSummaryRequest(artifacts, request.getModel());
        TGenSummaryResponse response = controller.generateSummaries(tgenRequest);

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
    public List<ArtifactAppEntity> summarizeCodeArtifacts(List<ArtifactAppEntity> projectArtifacts) {
        List<ArtifactAppEntity> codeArtifacts = projectArtifacts
            .stream()
            .filter(a -> TGenSummaryArtifactType.isCode(a.getName()) && !a.hasSummary()).collect(Collectors.toList());
        if (codeArtifacts.isEmpty()) {
            return new ArrayList<>();
        }
        List<TGenSummaryArtifact> summaryArtifacts = codeArtifacts.stream().map(a -> new TGenSummaryArtifact(
            a.getId().toString(),
            a.getName(),
            a.getBody(),
            TGenSummaryArtifactType.getArtifactType(a.getName()))
        ).collect(Collectors.toList());
        List<String> summarizedArtifacts = this.generateSummaries(new SummarizeRequestDTO(summaryArtifacts));
        for (int i = 0; i < codeArtifacts.size(); i++) {
            String artifactSummary = summarizedArtifacts.get(i);
            ArtifactAppEntity artifact = codeArtifacts.get(i);
            artifact.setSummary(artifactSummary);
        }
        return codeArtifacts;
    }
}
