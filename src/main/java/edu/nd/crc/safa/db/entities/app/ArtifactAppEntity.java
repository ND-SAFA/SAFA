package edu.nd.crc.safa.db.entities.app;

import edu.nd.crc.safa.db.entities.sql.ArtifactBody;

public class ArtifactAppEntity {
    public String name;
    public String summary;
    public String body;
    public String type;

    public ArtifactAppEntity() {
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
}
