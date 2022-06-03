package edu.nd.crc.safa.server.entities.app.project;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.DocumentType;

import lombok.Data;

/**
 * Represents the JSON model that is used on the front-end application.
 */
@Data
public class ArtifactAppEntity implements IAppEntity {
    /**
     * UUID uniquely identifying artifact.
     */
    @NotNull
    public String id;
    /**
     * The user-defined identifier for the artifact.
     */
    @NotNull
    @NotEmpty
    public String name;
    /**
     * Summary of the artifact body used for short displays of what the
     * artifact contains.
     */
    @NotNull
    public String summary;
    /**
     * The string representation of an artifact's content. Could be string, code, or other
     * file type like JSON.
     */
    @NotNull
    public String body;
    /**
     * The name of the ArtifactType this pertains to.
     */
    @NotNull
    @NotEmpty
    public String type;
    /**
     * List of document Ids this artifact belongs to.
     */
    public List<String> documentIds;
    /**
     * Mapping of columns ids to column values for this artifact.
     */
    public Map<String, String> customFields;
    /**
     * The type of document this artifact is displayed in.
     */
    public DocumentType documentType = DocumentType.ARTIFACT_TREE;
    /**
     * For safety case nodes, the type of safety case node.
     */
    public SafetyCaseType safetyCaseType;
    /**
     * For FTA logic nodes,  the logical operator of this node.
     */
    public FTANodeType logicType;

    public ArtifactAppEntity() {
        this.id = "";
        this.name = "";
        this.body = "";
        this.summary = "";
        this.documentIds = new ArrayList<>();
        this.customFields = new Hashtable<>();
    }

    public ArtifactAppEntity(String artifactId,
                             String type,
                             String name,
                             String summary,
                             String body,
                             DocumentType documentType,
                             Map<String, String> customFields) {
        this();
        this.id = artifactId;
        this.type = type;
        this.name = name;
        this.summary = summary;
        this.body = body;
        this.documentType = documentType;
        this.customFields = customFields;
    }

    public void addDocumentId(String documentId) {
        this.documentIds.add(documentId);
    }

    public String getBaseEntityId() {
        return id;
    }

    public void setBaseEntityId(String id) {
        this.id = id;
    }
}
