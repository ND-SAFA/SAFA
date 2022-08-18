package edu.nd.crc.safa.features.tgen.generator;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.tgen.vsm.Controller;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for generating trace links for given projects.
 */
@Service
@NoArgsConstructor
public class TraceGenerationService {

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
            artifactTokens.put(artifact.name, getWordsInArtifactAppEntity(artifact));
        }
        return artifactTokens;
    }

    private List<String> getWordsInArtifactAppEntity(ArtifactAppEntity artifact) {
        String[] artifactWords = artifact.getBody().split(" ");
        return Arrays.asList(artifactWords);
    }
}
