package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceGenerationController;
import edu.nd.crc.safa.features.models.tgen.method.vsm.VSMController;
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
    GPT("gpt"),
    /**
     * Anthropic claude 1.3 model.
     */
    ANTHROPIC("anthropic"),
    /**
     * The VSM method. Used primarily for testing.
     */
    VSM("vsm");

    String statePath;

    BaseGenerationModels(String statePath) {
        this.statePath = statePath;
    }

    /**
     * Returns the base model associated with name.
     *
     * @param name The name of the model.
     * @return The base generation model with name.
     */
    public static BaseGenerationModels getModel(String name) {
        return name == null ? getDefault() : BaseGenerationModels.valueOf(name);
    }

    /**
     * Retrieves base generation model by id.
     *
     * @param modelId The UUID of the model.
     * @return The Base generation model.
     */
    public static BaseGenerationModels getModelById(UUID modelId) {
        ModelAppEntity model = getDefaultModels()
            .stream()
            .filter(m -> m.getId().equals(modelId))
            .findFirst().orElse(getDefaultModel());
        return model.getBaseModel();
    }

    /**
     * @return Returns the default model for search, tracing, and generation.
     */
    public static BaseGenerationModels getDefault() {
        return BaseGenerationModels.ANTHROPIC;
    }

    /**
     * @return Returns list of models available to user.
     */
    public static List<ModelAppEntity> getDefaultModels() {
        return List.of(
            getDefaultModel(),
            new ModelAppEntity(UUID.fromString("d3e7023e-a1b4-4636-847a-39e006b80d00"), "AutomotiveBert", BaseGenerationModels.AutomotiveBert),
            new ModelAppEntity(UUID.fromString("610e386a-5d58-49a8-85b4-322d683a8147"), "Natural Language Bert", BaseGenerationModels.NLBert),
            new ModelAppEntity(UUID.fromString("4d589342-18a0-4bc4-b530-c186dc2b0de9"), "Programming Language Bert", BaseGenerationModels.NLBert),
            new ModelAppEntity(UUID.fromString("6f94c777-04e8-406c-9dc3-3a19e417043b"), "TraceGPT", BaseGenerationModels.GPT)
        );
    }

    /**
     * @return Returns the default model.
     */
    public static ModelAppEntity getDefaultModel() {
        return new ModelAppEntity(UUID.fromString("2dfe434c-5449-4b33-8627-f5ac20667aca"), "Anthropic", BaseGenerationModels.ANTHROPIC);
    }

    /**
     * @return TGen controller for base generation method.
     */
    public TGen createTGenController() {
        BertMethodIdentifier bertId = new BertMethodIdentifier(this.toString(), this.getStatePath());
        return new TGen(bertId);
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

    @Override
    public String toString() {
        return this.name();
    }
}
