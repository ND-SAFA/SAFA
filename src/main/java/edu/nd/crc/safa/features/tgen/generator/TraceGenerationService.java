package edu.nd.crc.safa.features.tgen.generator;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.SafaRequestBuilder;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.tgen.TBert;
import edu.nd.crc.safa.features.tgen.entities.ArtifactTypeTraceGenerationRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationMethod;
import edu.nd.crc.safa.features.tgen.vsm.Controller;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;

import lombok.AllArgsConstructor;
import org.apache.commons.lang3.NotImplementedException;
import org.springframework.stereotype.Service;

/**
 * Responsible for generating trace links for given projects.
 */
@Service
@AllArgsConstructor
public class TraceGenerationService {
    private static final String DELIMITER = "*";
    private final SafaRequestBuilder safaRequestBuilder;

    public List<TraceAppEntity> generateTraceLinks(List<ArtifactAppEntity> artifacts,
                                                   List<ArtifactTypeTraceGenerationRequestDTO> artifactTypeTraceGenerationRequestDTOS) throws IOException, InterruptedException {
        List<TraceAppEntity> generatedLinks = new ArrayList<>();

        for (ArtifactTypeTraceGenerationRequestDTO request : artifactTypeTraceGenerationRequestDTOS) {
            String sourceArtifactType = request.getSourceTypeName();
            String targetArtifactType = request.getTargetTypeName();

            List<ArtifactAppEntity> sourceArtifacts = artifacts
                .stream()
                .filter(a -> a.getType().equalsIgnoreCase(sourceArtifactType))
                .collect(Collectors.toList());
            List<ArtifactAppEntity> targetArtifacts = artifacts
                .stream()
                .filter(a -> a.getType().equalsIgnoreCase(targetArtifactType))
                .collect(Collectors.toList());
            List<TraceAppEntity> generatedLinkInRequest;
            TraceGenerationMethod traceGenerationMethod = request.getTraceGenerationMethod();
            switch (traceGenerationMethod) {
                case VSM:
                    generatedLinkInRequest = this.generateLinksBetweenArtifactAppEntities(
                        sourceArtifacts,
                        targetArtifacts);
                    break;
                case TBERT:
                    TBert tBert = new TBert(safaRequestBuilder);
                    generatedLinkInRequest = tBert.predict(sourceArtifacts, targetArtifacts);
                    break;
                default:
                    throw new NotImplementedException("Trace method not implemented:" + traceGenerationMethod);
            }
            generatedLinks.addAll(generatedLinkInRequest);
        }
        return generatedLinks;
    }

    public List<TraceAppEntity> filterDuplicateGeneratedLinks(List<TraceAppEntity> manualLinks,
                                                              List<TraceAppEntity> generatedLinks) {
        List<String> approvedLinks = manualLinks.stream()
            .filter(link -> link.getApprovalStatus().equals(ApprovalStatus.APPROVED))
            .map(link -> link.getSourceName() + DELIMITER + link.getTargetName())
            .collect(Collectors.toList());

        return generatedLinks
            .stream()
            .filter(t -> {
                String tId = t.getSourceName() + DELIMITER + t.getTargetName();
                return !approvedLinks.contains(tId);
            })
            .collect(Collectors.toList());
    }

    public List<TraceAppEntity> generateLinksBetweenArtifactAppEntities(List<ArtifactAppEntity> sourceDocs,
                                                                        List<ArtifactAppEntity> targetDocs) {
        Map<String, Collection<String>> sourceTokens = tokenizeArtifactAppEntities(sourceDocs);
        Map<String, Collection<String>> targetTokens = tokenizeArtifactAppEntities(targetDocs);
        TraceLinkConstructor<String, TraceAppEntity> traceLinkConstructor = (s, t, score) -> new TraceAppEntity()
            .asGeneratedTrace(score)
            .betweenArtifacts(s, t);
        return generateLinksFromTokens(sourceTokens, targetTokens, traceLinkConstructor);
    }

    private <K, L> List<L> generateLinksFromTokens(Map<K, Collection<String>> sTokens,
                                                   Map<K, Collection<String>> tTokens,
                                                   TraceLinkConstructor<K, L> traceLinkConstructor) {
        Controller vsm = new Controller();
        vsm.buildIndex(tTokens.values());

        List<L> generatedLS = new ArrayList<>();
        for (Map.Entry<K, Collection<String>> source : sTokens.entrySet()) {
            for (Map.Entry<K, Collection<String>> target : tTokens.entrySet()) {
                double score = vsm.getSimilarityScore(source.getValue(), target.getValue());
                if (score > ProjectVariables.TRACE_THRESHOLD) {
                    L value = traceLinkConstructor.createTraceLink(source.getKey(), target.getKey(), score);
                    generatedLS.add(value);
                }
            }
        }
        return generatedLS;
    }

    public Map<String, Collection<String>> tokenizeArtifactAppEntities(List<ArtifactAppEntity> artifacts) {
        Map<String, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactAppEntity artifact : artifacts) {
            artifactTokens.put(artifact.getName(), getWordsInArtifactAppEntity(artifact));
        }
        return artifactTokens;
    }

    private List<String> getWordsInArtifactAppEntity(ArtifactAppEntity artifact) {
        String[] artifactWords = artifact.getBody().split(" ");
        return Arrays.asList(artifactWords);
    }
}
