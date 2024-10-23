package edu.nd.crc.safa.features.artifacts.entities;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * Represents the JSON model that is used on the front-end application.
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class ArtifactAppEntity implements IAppEntity {
    /**
     * UUID uniquely identifying artifact.
     */
    private UUID id;

    /**
     * The user-defined identifier for the artifact.
     */
    @NotNull
    @NotEmpty
    private String name;

    /**
     * Summary of the artifact body used for short displays of what the
     * artifact contains.
     */
    @NotNull
    private String summary;

    /**
     * The string representation of an artifact's content. Could be string, code, or other
     * file type like JSON.
     */
    @NotNull
    private String body;

    /**
     * The name of the ArtifactType this pertains to.
     */
    @NotNull
    @NotEmpty
    private String type;

    /**
     * Mapping of columns ids to column values for this artifact.
     */
    private Map<String, JsonNode> attributes = new HashMap<>();

    /**
     * List of document Ids this artifact belongs to.
     */
    private List<UUID> documentIds = new ArrayList<>();

    public ArtifactAppEntity() {
        this.name = "";
        this.body = "";
        this.summary = "";
        this.attributes = new HashMap<>();
    }

    public ArtifactAppEntity(UUID artifactId,
                             String type,
                             String name,
                             String summary,
                             String body,
                             Map<String, JsonNode> attributes) {
        this();
        this.id = artifactId;
        this.type = type;
        this.name = name;
        this.summary = summary;
        this.body = body;
        this.attributes = attributes;
    }

    public ArtifactAppEntity(GenerationArtifact artifact) {
        this.name = artifact.getId();
        this.body = artifact.getContent();
        this.summary = artifact.getSummary();
        this.type = artifact.getLayerId();
        if (this.summary == null) {
            this.summary = ""; // Enforces constraint that summary must be some defined string.
        }
    }

    public void addDocumentId(UUID documentId) {
        this.documentIds.add(documentId);
    }

    @JsonIgnore
    public boolean hasSummary() {
        return this.summary != null && this.summary.length() > 0;
    }

    /**
     * Returns the tracing string that best represents this artifact.
     *
     * @return String representing artifact content.
     */
    @JsonIgnore
    public String getTraceString() {
        if (this.hasSummary()) {
            return this.summary;
        } else {
            return this.body;
        }
    }

    /**
     * Returns whether this artifact represents a code file based on its file extension.
     *
     * @return True if the artifact is code, false otherwise.
     */
    @JsonProperty(value = "isCode", access = JsonProperty.Access.READ_ONLY)
    public boolean isCode() {
        return FileUtilities.isCodeFile(Path.of(this.name));
    }

    @JsonIgnore
    public List<String> getMissingRequiredFields() {
        List<String> missingFields = new ArrayList<>();
        if (name == null || name.isBlank()) {
            missingFields.add("name");
        }
        if (body == null) {
            missingFields.add("body");
        }
        if (type == null || type.isBlank()) {
            missingFields.add("type");
        }

        return missingFields;
    }

    /**
     * Makes it impossible to set a summary to null.
     *
     * @param summary The summary to set artifact to.
     */
    public void setSummary(String summary) {
        if (summary == null) {
            summary = "";
        }
        this.summary = summary;
    }
}
