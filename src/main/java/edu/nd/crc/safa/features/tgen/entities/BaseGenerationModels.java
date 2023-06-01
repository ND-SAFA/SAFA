package edu.nd.crc.safa.features.tgen.entities;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceGenerationController;
import edu.nd.crc.safa.features.models.tgen.method.vsm.VSMController;
import edu.nd.crc.safa.features.tgen.TGen;
import edu.nd.crc.safa.features.tgen.method.BertMethodIdentifier;

import lombok.Getter;

/**
 * The algorithm for computing the similarity scores between a pair of artifacts.
 */
@Getter
public enum BaseGenerationModels {

    /**
     * The Bert model trained on automotive data.
     */
    AutomotiveBert("b0c13c32-03d6-43bc-90df-2679c6affae3", "thearod5/automotive-bert", "Automotive BERT"),
    /**
     * Bert model trained on NL-NL trace links.
     */
    NLBert("610e386a-5d58-49a8-85b4-322d683a8147", "thearod5/nl-bert", "Natural Language BERT"),
    /**
     * TBert as described in Traceability Transformed: Generating more Accurate Links with Pre-Trained BERT Models.
     */
    PLBert("4d589342-18a0-4bc4-b530-c186dc2b0de9", "thearod5/pl-bert", "Programming Language BERT"),
    /**
     * OpenAI's GPT3.5 ada model trained on traceability links
     */
    GPT("6f94c777-04e8-406c-9dc3-3a19e417043b", "gpt", "GPT3"),
    /**
     * Anthropic claude 1.3 model.
     */
    ANTHROPIC("d3e7023e-a1b4-4636-847a-39e006b80d00", "anthropic", "Claude"),
    /**
     * The VSM method. Used primarily for testing.
     */
    VSM("00efc62f-afcc-4345-a843-b59dfa28ef5d", "vsm", "Vector Space Model");

    /**
     * Unique identifier for each model.
     */
    UUID id;
    /**
     * The path to load state from.
     */
    String statePath;
    /**
     * The display name of the model.
     */
    String name;

    /**
     * The job to log tgen logs under.
     */
    JobAppEntity job;

    BaseGenerationModels(String id, String statePath, String name) {
        this.id = UUID.fromString(id);
        this.statePath = statePath;
        this.name = name;
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
        return BaseGenerationModels.GPT;
    }

    /**
     * @return Returns list of models available to user.
     */
    public static List<ModelAppEntity> getDefaultModels() {
        return Arrays.stream(BaseGenerationModels.values()).map(ModelAppEntity::new).collect(Collectors.toList());
    }

    /**
     * @return Returns the default model.
     */
    public static ModelAppEntity getDefaultModel() {
        return new ModelAppEntity(BaseGenerationModels.GPT);
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
