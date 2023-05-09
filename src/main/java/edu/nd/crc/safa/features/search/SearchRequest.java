package edu.nd.crc.safa.features.search;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import javax.annotation.Nullable;
import javax.validation.constraints.NotNull;

import lombok.Data;

@Data
public class SearchRequest {
    /**
     * The type of information to predict traces to.
     */
    @NotNull
    SearchMode mode;
    /**
     * Used in "prompt" mode.
     * This string of text will be treated as an artifact to predict links from.
     */
    @Nullable
    String prompt;
    /**
     * Used in "artifacts" mode.
     * These artifacts will be used as the base to predict links from.
     */
    @Nullable
    List<UUID> artifactIds;
    /**
     * Used in "artifactTypes" mode.
     * All artifacts of these types will be used as the base to predict links from.
     */
    @Nullable
    List<String> artifactTypes;
    /**
     * What type(s) of artifacts to predict links from the search artifacts to.
     */
    @NotNull
    List<String> searchTypes;
    /**
     * How many of the top predictions to include. Defaults to 5.
     */
    int maxResults = 5;
    /**
     * What other type(s) of artifacts should I import,
     * if they have existing links to the artifacts retrieved with the search artifacts + `searchTypes` artifacts.
     */
    @Nullable
    List<String> relatedTypes = new ArrayList<>();
    /**
     * The model to predict links with. Defaults to current best model.
     */
    @Nullable
    String model;
    /**
     * The prompt used to decide whether two artifacts should be traced.
     */
    @Nullable
    String tracingPrompt;
}
