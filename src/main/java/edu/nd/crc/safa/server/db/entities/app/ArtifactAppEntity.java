package edu.nd.crc.safa.server.db.entities.app;

import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;

import org.json.JSONObject;

public class ArtifactAppEntity {
    @NotNull
    public String name;

    @NotNull
    public String summary;

    @NotNull
    public String body;

    @NotNull
    public String type;

    public ArtifactAppEntity() {
        this.body = "";
        this.summary = "";
    }

    public ArtifactAppEntity(ArtifactBody body) {
        this(body.getTypeName(), body.getName(), body.getSummary(), body.getContent());
    }

    public ArtifactAppEntity(String type,
                             String name,
                             String summary,
                             String body) {
        this.type = type;
        this.name = name;
        this.summary = summary;
        this.body = body;
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
        json.put("name", name);
        json.put("summary", summary);
        json.put("body", body);
        json.put("type", type);
        return json.toString();
    }
}
