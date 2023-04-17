package edu.nd.crc.safa.features.models.tgen.entities;

/**
 * The algorithm for computing the similarity scores between a pair of artifacts.
 */
public enum BaseGenerationModels {
    /**
     * The Bert model trained on automotive data.
     */
    AutomotiveBert,
    /**
     * Bert model trained on NL-NL trace links.
     */
    NLBert,
    /**
     * TBert as described in Traceability Transformed: Generating more Accurate Links with Pre-Trained BERT Models.
     */
    PLBert,
    /**
     * Vector-space-model with cosine similarity.
     */
    VSM,
    /**
     * OpenAI's GPT3.5 ada model trained on traceability links
     */
    GPT;

    public static BaseGenerationModels getDefault() {
        return BaseGenerationModels.VSM;
    }

    @Override
    public String toString() {
        return this.name();
    }
}
