package edu.nd.crc.safa.server.entities.app;

import java.util.ArrayList;
import java.util.List;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.ArtifactVersion;

import org.json.JSONObject;

/**
 * Represents the JSON model that is used on the front-end application.
 */
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
     * The type of document this artifact is displayed in.
     */
    DocumentType documentType = DocumentType.ARTIFACT_TREE;

    public ArtifactAppEntity() {
        this.id = "";
        this.name = "";
        this.body = "";
        this.summary = "";
        this.documentIds = new ArrayList<>();
    }

    public ArtifactAppEntity(String artifactId,
                             String type,
                             String name,
                             String summary,
                             String body) {
        this();
        this.id = artifactId;
        this.type = type;
        this.name = name;
        this.summary = summary;
        this.body = body;
    }

    public ArtifactAppEntity(ArtifactVersion body) {
        this(body.getArtifact().getArtifactId().toString(),
            body.getTypeName(),
            body.getName(),
            body.getSummary(),
            body.getContent());
    }

    public DocumentType getDocumentType() {
        return documentType;
    }

    public void setDocumentType(DocumentType documentType) {
        this.documentType = documentType;
    }

    public List<String> getDocumentIds() {
        return documentIds;
    }

    public void setDocumentIds(List<String> documentIds) {
        this.documentIds = documentIds;
    }

    public void addDocumentId(String documentId) {
        this.documentIds.add(documentId);
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSummary() {
        return this.summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getBody() {
        return this.body;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("artifactId", id);
        json.put("name", name);
        json.put("summary", summary);
        json.put("body", body);
        json.put("type", type);
        return json.toString();
    }
}
