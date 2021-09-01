package edu.nd.crc.safa.entities.application;

import edu.nd.crc.safa.entities.sql.ArtifactBody;

public class ArtifactApplicationEntity {
    public String name;
    public String summary;
    public String body;
    public String type;

    public ArtifactApplicationEntity() {
    }

    public ArtifactApplicationEntity(ArtifactBody body) {
        this.name = body.getName();
        this.summary = body.getSummary();
        this.body = body.getContent();
        this.type = body.getTypeName();
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
}
