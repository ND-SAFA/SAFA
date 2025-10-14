package edu.nd.crc.safa.features.traces.vsm;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Term frequency-Inverse document frequency.
 * Find source at https://github.com/wpm/tfidf
 */
class TfIdf {

    /**
     * Term frequency for a single document
     *
     * @param document bag of terms
     * @param type     natural or logarithmic
     * @param <T>      term type
     * @return map of terms to their term frequencies
     */
    public static <T> Map<T, Double> tf(Collection<T> document, TfType type) {
        Map<T, Double> term2score = new HashMap<>();
        for (T t : document) {
            term2score.put(t, term2score.getOrDefault(t, 0.0) + 1);
        }
        if (type != TfType.NATURAL) {
            for (Map.Entry<T, Double> entry : term2score.entrySet()) {
                double score = entry.getValue();
                switch (type) {
                    case LOGARITHM:
                        score = 1 + Math.log(score);
                        break;
                    case BOOLEAN:
                        score = score == 0.0 ? 0.0 : 1.0;
                        break;
                    default:
                }
                term2score.put(entry.getKey(), score);
            }
        }
        return term2score;
    }

    /**
     * Natural term frequency for a single document
     *
     * @param document bag of terms
     * @param <T>      term type
     * @return map of terms to their term frequencies
     */
    public static <T> Map<T, Double> tf(Collection<T> document) {
        return tf(document, TfType.NATURAL);
    }

    /**
     * Term frequencies for a set of documents
     *
     * @param documents sequence of documents, each of which is a bag of terms
     * @param type      natural or logarithmic
     * @param <T>       term type
     * @return sequence of map of terms to their term frequencies
     */
    public static <T> Iterable<Map<T, Double>> tfs(Iterable<Collection<T>> documents, TfType type) {
        List<Map<T, Double>> tfs = new ArrayList<>();
        for (Collection<T> document : documents) {
            tfs.add(tf(document, type));
        }
        return tfs;
    }

    /**
     * Natural term frequencies for a set of documents
     *
     * @param documents sequence of documents, each of which is a bag of terms
     * @param <T>       term type
     * @return sequence of map of terms to their term frequencies
     */
    public static <T> Iterable<Map<T, Double>> tfs(Iterable<Collection<T>> documents) {
        return tfs(documents, TfType.NATURAL);
    }

    /**
     * Inverse document frequency for a set of documents
     *
     * @param documentVocabularies sets of terms which appear in the documents
     * @param smooth               smooth the counts by treating the document set as if it contained an additional
     *                             document with every term in the vocabulary
     * @param addOne               add one to idf values to prevent divide by zero errors in tf-idf
     * @param <T>                  term type
     * @return map of terms to their inverse document frequency
     */
    public static <T> Map<T, Double> idf(Iterable<Iterable<T>> documentVocabularies,
                                         boolean smooth, boolean addOne) {
        Map<T, Integer> df = new HashMap<>();
        int d = smooth ? 1 : 0;
        int a = addOne ? 1 : 0;
        int n = d;
        for (Iterable<T> documentVocabulary : documentVocabularies) {
            n += 1;
            for (T t : documentVocabulary) {
                df.put(t, df.getOrDefault(t, d) + 1);
            }
        }
        Map<T, Double> idf = new HashMap<>();
        for (Map.Entry<T, Integer> e : df.entrySet()) {
            T t = e.getKey();
            double f = e.getValue();
            idf.put(t, Math.log(n / f) + a);
        }
        return idf;
    }

    /**
     * Smoothed, add-one inverse document frequency for a set of documents
     *
     * @param documentVocabularies sets of terms which appear in the documents
     * @param <T>                  term type
     * @return map of terms to their inverse document frequency
     */
    public static <T> Map<T, Double> idf(Iterable<Iterable<T>> documentVocabularies) {
        return idf(documentVocabularies, true, true);
    }

    /**
     * tf-idf for a document
     *
     * @param tf            term frequencies of the document
     * @param idf           inverse document frequency for a set of documents
     * @param normalization none or cosine
     * @param <T>           term type
     * @return map of terms to their tf-idf values
     */
    public static <T> Map<T, Double> tfIdf(Map<T, Double> tf, Map<T, Double> idf,
                                           Normalization normalization) {
        Map<T, Double> tfIdf = new HashMap<>();
        for (Map.Entry<T, Double> entry : tf.entrySet()) {
            T t = entry.getKey();
            if (idf.containsKey(entry.getKey())) {
                tfIdf.put(t, tf.get(t) * idf.get(t));
            }
        }
        if (normalization == Normalization.COSINE) {
            double n = 0.0;
            for (double x : tfIdf.values()) {
                n += x * x;
            }
            n = Math.sqrt(n);

            for (Map.Entry<T, Double> entry : tfIdf.entrySet()) {
                tfIdf.put(entry.getKey(), entry.getValue() / n);
            }
        }
        return tfIdf;
    }

    /**
     * Un-normalized tf-idf for a document
     *
     * @param tf  term frequencies of the document
     * @param idf inverse document frequency for a set of documents
     * @param <T> term type
     * @return map of terms to their tf-idf values
     */
    public static <T> Map<T, Double> tfIdf(Map<T, Double> tf, Map<T, Double> idf) {
        return tfIdf(tf, idf, Normalization.NONE);
    }

    /**
     * Utility to build inverse document frequencies from a set of term frequencies
     *
     * @param tfs    term frequencies for a set of documents
     * @param smooth smooth the counts by treating the document set as if it contained an additional
     *               document with every term in the vocabulary
     * @param addOne add one to idf values to prevent divide by zero errors in tf-idf
     * @param <T>    term type
     * @return map of terms to their tf-idf values
     */
    public static <T> Map<T, Double> idfFromTfs(Iterable<Map<T, Double>> tfs, boolean smooth, boolean addOne) {
        return idf(new KeySetIterable<>(tfs), smooth, addOne);
    }

    /**
     * Utility to build smoothed, add-one inverse document frequencies from a set of term frequencies
     *
     * @param tfs term frequencies for a set of documents
     * @param <T> term type
     * @return map of terms to their tf-idf values
     */
    public static <T> Map<T, Double> idfFromTfs(Iterable<Map<T, Double>> tfs) {
        return idfFromTfs(tfs, true, true);
    }

    /**
     * Word count method used for term frequencies
     */
    public enum TfType {
        /**
         * Term frequency
         */
        NATURAL,
        /**
         * Log term frequency plus 1
         */
        LOGARITHM,
        /**
         * 1 if term is present, 0 if it is not
         */
        BOOLEAN
    }

    /**
     * Normalization of the tf-idf vector
     */
    public enum Normalization {
        /**
         * Do not normalize the vector
         */
        NONE,
        /**
         * Normalize by the vector elements added in quadrature
         */
        COSINE
    }

    /**
     * Iterator over the key sets of a set of maps.
     *
     * @param <K> map key type
     * @param <V> map value type
     */
    private static class KeySetIterable<K, V> implements Iterable<Iterable<K>> {
        private final Iterator<Map<K, V>> maps;

        public KeySetIterable(Iterable<Map<K, V>> maps) {
            this.maps = maps.iterator();
        }

        @Override
        public Iterator<Iterable<K>> iterator() {
            return new Iterator<Iterable<K>>() {
                @Override
                public boolean hasNext() {
                    return maps.hasNext();
                }

                @Override
                public Iterable<K> next() {
                    return maps.next().keySet();
                }
            };
        }
    }
}
