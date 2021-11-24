package edu.nd.crc.safa.server.entities.app;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.ArtifactBody;

import org.json.JSONObject;

/**
 * Represents the JSON model that is used on the front-end application.
 */
public class ArtifactAppEntity {
    @NotNull
    public String id;
    @NotNull
    @NotEmpty
    public String name;
    @NotNull
    public String summary;
    @NotNull
    public String body;
    @NotNull
    @NotEmpty
    public String type;

    public ArtifactAppEntity() {
        this.id = "";
        this.name = "";
        this.body = "";
        this.summary = "";
    }

    public ArtifactAppEntity(String artifactId,
                             String type,
                             String name,
                             String summary,
                             String body) {
        this.id = artifactId;
        this.type = type;
        this.name = name;
        this.summary = summary;
        this.body = body;
    }

    public ArtifactAppEntity(ArtifactBody body) {
        this(body.getArtifact().getArtifactId().toString(),
            body.getTypeName(),
            body.getName(),
            body.getSummary(),
            body.getContent());
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

    public ArtifactAppEntity withName(String name) {
        this.name = name;
        return this;
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
