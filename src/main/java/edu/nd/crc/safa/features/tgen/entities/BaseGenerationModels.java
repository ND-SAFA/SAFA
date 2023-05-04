package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.tgen.method.BertMethodIdentifier;
import edu.nd.crc.safa.features.tgen.method.TGen;

import lombok.Getter;

/**
 * The algorithm for computing the similarity scores between a pair of artifacts.
 */
@Getter
public enum BaseGenerationModels {
    /**
     * The Bert model trained on automotive data.
     */
    AutomotiveBert("thearod5/automotive-bert"),
    /**
     * Bert model trained on NL-NL trace links.
     */
    NLBert("thearod5/nl-bert"),
    /**
     * TBert as described in Traceability Transformed: Generating more Accurate Links with Pre-Trained BERT Models.
     */
    PLBert("thearod5/pl-bert"),
    /**
     * OpenAI's GPT3.5 ada model trained on traceability links
     */
    GPT("gpt");

    String statePath;

    BaseGenerationModels(String statePath) {
        this.statePath = statePath;
    }

    public static BaseGenerationModels getDefault() {
        return BaseGenerationModels.GPT;
    }

    /**
     * @return Returns list of models available to user.
     */
    public static List<ModelAppEntity> getDefaultModels() {
        return List.of(
            getDefaultModel(),
            new ModelAppEntity(UUID.randomUUID(), "AutomotiveBert", BaseGenerationModels.AutomotiveBert),
            new ModelAppEntity(UUID.randomUUID(), "Natural Language Bert", BaseGenerationModels.NLBert),
            new ModelAppEntity(UUID.randomUUID(), "Programming Language Bert", BaseGenerationModels.NLBert)
        );
    }

    /**
     * @return Returns the default model.
     */
    public static ModelAppEntity getDefaultModel() {
        return new ModelAppEntity(UUID.randomUUID(), "TraceGPT", BaseGenerationModels.GPT);
    }

    /**
     * @return TGen controller for base generation method.
     */
    public TGen createTGenController() {
        BertMethodIdentifier bertId = new BertMethodIdentifier(this.toString(), this.getStatePath());
        return new TGen(bertId);
    }

    @Override
    public String toString() {
        return this.name();
    }
}
