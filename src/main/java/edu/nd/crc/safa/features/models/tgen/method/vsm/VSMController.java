package edu.nd.crc.safa.features.models.tgen.method.vsm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.models.tgen.entities.ArtifactLevel;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.models.tgen.entities.TracingPayload;
import edu.nd.crc.safa.features.models.tgen.generator.TraceLinkConstructor;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

/**
 * Vector Space Model using TF-IDF scores for evaluating document relevance
 */
public class VSMController implements ITraceLinkGeneration {
    private Map<String, Double> idf;

    @Override
    public List<TraceAppEntity> generateLinksWithState(String statePath,
                                                       boolean loadFromStorage,
                                                       TracingPayload tracingPayload) {
        //Note, VSM has not state (yet).
        return generateLinksWithBaselineState(tracingPayload);
    }

    /**
     * Generates set of trace links between source and target pairs of artifacts using the
     * vector-space model
     *
     * @param tracingPayload List of artifact levels defining set of source and target artifacts.
     * @return List of trace links.
     */
    @Override
    public List<TraceAppEntity> generateLinksWithBaselineState(TracingPayload tracingPayload) {
        List<TraceAppEntity> generatedLinks = new ArrayList<>();
        for (ArtifactLevel artifactLevel : tracingPayload.getArtifactLevels()) {
            Map<String, Collection<String>> sourceTokens = tokenizeArtifactAppEntities(artifactLevel.getSources());
            Map<String, Collection<String>> targetTokens = tokenizeArtifactAppEntities(artifactLevel.getTargets());
            TraceLinkConstructor<String, TraceAppEntity> traceLinkConstructor = (s, t, score) -> new TraceAppEntity()
                .asGeneratedTrace(score)
                .betweenArtifacts(s, t);
            generatedLinks.addAll(generateLinksFromTokens(sourceTokens, targetTokens, traceLinkConstructor));
        }

        return generatedLinks;
    }

    private <K, L> List<L> generateLinksFromTokens(Map<K, Collection<String>> sTokens,
                                                   Map<K, Collection<String>> tTokens,
                                                   TraceLinkConstructor<K, L> traceLinkConstructor) {
        VSMController vsm = new VSMController();
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

    private Map<String, Collection<String>> tokenizeArtifactAppEntities(List<ArtifactAppEntity> artifacts) {
        Map<String, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactAppEntity artifact : artifacts) {
            artifactTokens.put(artifact.getName(), getWordsInArtifactAppEntity(artifact));
        }
        return artifactTokens;
    }

    private void buildIndex(Collection<Collection<String>> docTokens) {
        Iterable<Map<String, Double>> tfs = TfIdf.tfs(docTokens);
        idf = TfIdf.idfFromTfs(tfs);
    }

    private List<String> getWordsInArtifactAppEntity(ArtifactAppEntity artifact) {
        String[] artifactWords = artifact.getBody().split(" ");
        return Arrays.asList(artifactWords);
    }

    private double getSimilarityScore(Collection<String> sTokens, Collection<String> tTokens) {
        Map<String, Double> vec1 = TfIdf.tfIdf(TfIdf.tf(sTokens), idf);
        Map<String, Double> vec2 = TfIdf.tfIdf(TfIdf.tf(tTokens), idf);
        return cosineSim(vec1, vec2);
    }

    private double cosineSim(Map<String, Double> vec1, Map<String, Double> vec2) {
        double acc = 0;
        double l1 = 0;
        double l2 = 0;
        for (Map.Entry<String, Double> entry : vec1.entrySet()) {
            String term = entry.getKey();
            if (vec2.containsKey(term)) {
                acc += entry.getValue() * entry.getValue();
            }
            l1 += entry.getValue() * entry.getValue();
        }
        for (Map.Entry<String, Double> entry : vec2.entrySet()) {
            l2 += entry.getValue() * entry.getValue();
        }
        double base = (Math.sqrt(l1) * Math.sqrt(l2));
        if (base == 0) {
            return 0;
        } else {
            return acc / base;
        }
    }
}

