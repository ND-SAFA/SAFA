package edu.nd.crc.safa.features.artifacts.entities;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.Data;

/**
 * Represents the JSON model that is used on the front-end application.
 */
@Data
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
     * The type of document this artifact is displayed in.
     */
    private DocumentType documentType = DocumentType.ARTIFACT_TREE;

    /**
     * For safety case nodes, the type of safety case node.
     */
    private SafetyCaseType safetyCaseType;

    /**
     * For FTA logic nodes,  the logical operator of this node.
     */
    private FTAType logicType;

    /**
     * List of document Ids this artifact belongs to.
     */
    private List<UUID> documentIds = new ArrayList<>();

    public ArtifactAppEntity() {
        this.name = "";
        this.body = "";
        this.summary = "";
    }

    public ArtifactAppEntity(UUID artifactId,
                             String type,
                             String name,
                             String summary,
                             String body,
                             DocumentType documentType,
                             Map<String, JsonNode> attributes) {
        this();
        this.id = artifactId;
        this.type = type;
        this.name = name;
        this.summary = summary;
        this.body = body;
        this.documentType = documentType;
        this.attributes = attributes;
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
     * Attempts to create a unique identifier from the id or name of the artifact.
     *
     * @return Returns some unique identifier to artifact.
     */
    @JsonIgnore
    public String getTraceableId() {
        if (this.id != null) {
            return this.id.toString();
        } else {
            return this.name;
        }
    }

    /**
     * Returns whether this artifact represents a code file based on its file extension.
     *
     * @return True if the artifact is code, false otherwise.
     */
    public boolean isCode() {
        return FileUtilities.isCodeFile(Path.of(this.name));
    }
}
