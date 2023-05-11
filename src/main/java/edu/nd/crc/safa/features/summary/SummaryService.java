package edu.nd.crc.safa.features.summary;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.method.TGen;

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
        Map<String, TGenSummaryArtifact> artifacts = new HashMap<>();
        for (TGenSummaryArtifact artifact : request.getArtifacts()) {
            artifacts.put(UUID.randomUUID().toString(), artifact);
        }
        TGenSummaryRequest tgenRequest = new TGenSummaryRequest(artifacts, request.getModel());
        TGenSummaryResponse response = controller.generateSummaries(tgenRequest);

        List<String> summaries = new ArrayList<>();
        for (TGenSummaryArtifact artifact : response.getArtifacts().values()) {
            summaries.add(artifact.getContent());
        }
        return summaries;
    }
}
