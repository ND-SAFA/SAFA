package edu.nd.crc.safa.features.traces.vsm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.TraceLayer;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.traces.ITraceGenerationController;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

/**
 * Vector Space Model using TF-IDF scores for evaluating document relevance
 */
public class VSMController implements ITraceGenerationController {
    private Map<String, Double> idf;

    /**
     * Generates set of trace links between source and target pairs of artifacts using the
     * vector-space model
     *
     * @param generationDataset The dataset to trace.
     * @return List of trace links.
     */
    @Override
    public List<TraceAppEntity> generateLinks(GenerationDataset generationDataset, JobLogger jobLogger) {
        List<TraceAppEntity> generatedLinks = new ArrayList<>();
        for (TraceLayer layer : generationDataset.getLayers()) {
            Map<String, String> childLayer = generationDataset
                .getArtifacts(layer.getChild())
                .stream()
                .collect(Collectors.toMap(GenerationArtifact::getId, GenerationArtifact::getContent));
            Map<String, String> parentLayer = generationDataset
                .getArtifacts(layer.getParent())
                .stream()
                .collect(Collectors.toMap(GenerationArtifact::getId, GenerationArtifact::getContent));

            Map<String, Collection<String>> childTokens = tokenizeArtifactAppEntities(childLayer);
            Map<String, Collection<String>> parentTokens = tokenizeArtifactAppEntities(parentLayer);
            TraceLinkConstructor<String, TraceAppEntity> traceLinkConstructor = (s, t, score) ->
                new TraceAppEntity(s, t).asGeneratedTrace(score);
            generatedLinks.addAll(generateLinksFromTokens(childTokens, parentTokens, traceLinkConstructor));
        }

        return generatedLinks;
    }

    private <K, L> List<L> generateLinksFromTokens(Map<K, Collection<String>> sTokens,
                                                   Map<K, Collection<String>> tTokens,
                                                   TraceLinkConstructor<K, L> traceLinkConstructor) {
        this.buildIndex(tTokens.values());

        List<L> generatedLS = new ArrayList<>();
        for (Map.Entry<K, Collection<String>> source : sTokens.entrySet()) {
            for (Map.Entry<K, Collection<String>> target : tTokens.entrySet()) {
                double score = this.getSimilarityScore(source.getValue(), target.getValue());
                if (score > ProjectVariables.TRACE_THRESHOLD) {
                    L value = traceLinkConstructor.createTraceLink(source.getKey(), target.getKey(), score);
                    generatedLS.add(value);
                }
            }
        }
        return generatedLS;
    }

    private Map<String, Collection<String>> tokenizeArtifactAppEntities(Map<String, String> artifacts) {
        return artifacts
            .entrySet()
            .stream()
            .collect(Collectors.toMap(entry -> entry.getKey(),
                entry -> getWordsInArtifactAppEntity(entry.getValue())));
    }

    private void buildIndex(Collection<Collection<String>> docTokens) {
        Iterable<Map<String, Double>> tfs = TfIdf.tfs(docTokens);
        idf = TfIdf.idfFromTfs(tfs);
    }

    private List<String> getWordsInArtifactAppEntity(String content) {
        String[] artifactWords = content.split(" ");
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

