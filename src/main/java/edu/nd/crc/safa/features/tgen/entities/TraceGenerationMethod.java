package edu.nd.crc.safa.features.tgen.entities;

/**
 * The algorithm for computing the similarity scores between a pair of artifacts.
 */
public enum TraceGenerationMethod {
    /**
     * TBert as described in Traceability Transformed: Generating more Accurate Links with Pre-Trained BERT Models.
     */
    TBERT,
    /**
     * Vector-space-model with cosine similarity.
     */
    VSM;

    public static TraceGenerationMethod getMethodWithDefault(String name, TraceGenerationMethod defaultMethod) {
        for (TraceGenerationMethod method : TraceGenerationMethod.values()) {
            if (method.name().equals(name)) {
                return method;
            }
        }
        return defaultMethod;
    }

    public static TraceGenerationMethod getDefault() {
        return TraceGenerationMethod.VSM;
    }

    @Override
    public String toString() {
        return this.name();
    }
}
