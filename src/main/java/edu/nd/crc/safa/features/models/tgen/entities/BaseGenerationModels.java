package edu.nd.crc.safa.features.models.tgen.entities;

import edu.nd.crc.safa.features.models.tgen.method.bert.BertMethodIdentifier;
import edu.nd.crc.safa.features.models.tgen.method.bert.TGen;
import edu.nd.crc.safa.features.models.tgen.method.vsm.VSMController;

import lombok.Getter;

/**
 * The algorithm for computing the similarity scores between a pair of artifacts.
 */
@Getter
public enum BaseGenerationModels {
    /**
     * The Bert model trained on automotive data.
     */
    AutomotiveBert("thearod5/automotive"),
    /**
     * Bert model trained on NL-NL trace links.
     */
    NLBert("thearod5/nl-bert"),
    /**
     * TBert as described in Traceability Transformed: Generating more Accurate Links with Pre-Trained BERT Models.
     */
    PLBert("thearod5/pl-bert"),
    /**
     * Vector-space-model with cosine similarity.
     */
    VSM("vsm"), //Not real state, placeholder.
    /**
     * OpenAI's GPT3.5 ada model trained on traceability links
     */
    GPT("gpt");

    String statePath;

    BaseGenerationModels(String statePath) {
        this.statePath = statePath;
    }

    public static BaseGenerationModels getDefault() {
        return BaseGenerationModels.VSM;
    }

    @Override
    public String toString() {
        return this.name();
    }

    /**
     * Constructs the bert model identifier for generation model.
     *
     * @return Model identifier.
     */
    public BertMethodIdentifier getBertMethodIdentifier() {
        if (this.equals(BaseGenerationModels.VSM)) {
            throw new UnsupportedOperationException("VSM does not use the bert method identifier.");
        }
        return new BertMethodIdentifier(this.toString(), this.getStatePath());
    }

    public TGen createTGenController() {
        return new TGen(this.getBertMethodIdentifier());
    }

    /**
     * Constructs a trace link generation controller for the base generation method.
     *
     * @return Trace link generation controller.
     */
    public ITraceGenerationController createController() {
        if (this == BaseGenerationModels.VSM) {
            return new VSMController();
        }
        return this.createTGenController();
    }
}
