package edu.nd.crc.safa.features.generation.search;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import jakarta.annotation.Nullable;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class SearchRequest {
    /**
     * The type of information to predict traces to.
     */
    @NotNull
    private SearchMode mode;
    /**
     * Used in "prompt" mode.
     * This string of text will be treated as an artifact to predict links from.
     */
    @Nullable
    private String prompt;
    /**
     * Used in "artifacts" mode.
     * These artifacts will be used as the base to predict links from.
     */
    @Nullable
    private List<UUID> artifactIds;
    /**
     * Used in "artifactTypes" mode.
     * All artifacts of these types will be used as the base to predict links from.
     */
    @Nullable
    private List<String> artifactTypes;
    /**
     * What type(s) of artifacts to predict links from the search artifacts to.
     */
    @NotNull
    private List<String> searchTypes;
    /**
     * How many of the top predictions to include. Defaults to 5.
     */
    private int maxResults = 5;
    /**
     * What other type(s) of artifacts should I import,
     * if they have existing links to the artifacts retrieved with the search artifacts + `searchTypes` artifacts.
     */
    @Nullable
    private List<String> relatedTypes = new ArrayList<>();

    public void setRelatedTypes(List<String> relatedTypes) {
        if (relatedTypes == null) {
            relatedTypes = new ArrayList<>();
        }
        this.relatedTypes = relatedTypes;
    }
}
