package edu.nd.crc.safa.features.tgen.vsm;

import java.util.Collection;
import java.util.Map;

/**
 * Vector Space Model using TF-IDF scores for evaluating document relevance
 */

public class Controller implements ISimilarScoreCalculator {
    private Map<String, Double> idf;

    public void buildIndex(Collection<Collection<String>> docTokens) {
        Iterable<Map<String, Double>> tfs = TfIdf.tfs(docTokens);
        idf = TfIdf.idfFromTfs(tfs);
    }

    @Override
    public double getSimilarityScore(Collection<String> sTokens, Collection<String> tTokens) {
        Map<String, Double> vec1 = TfIdf.tfIdf(TfIdf.tf(sTokens), idf);
        Map<String, Double> vec2 = TfIdf.tfIdf(TfIdf.tf(tTokens), idf);
        return cosineSim(vec1, vec2);
    }

    public double cosineSim(Map<String, Double> vec1, Map<String, Double> vec2) {
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

