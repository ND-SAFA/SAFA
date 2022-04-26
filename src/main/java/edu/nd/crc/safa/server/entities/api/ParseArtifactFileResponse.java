package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;

public class ParseArtifactFileResponse implements ParseFileResponse {

    List<ArtifactAppEntity> artifacts;
    List<String> errors;

    public ParseArtifactFileResponse() {
        this.artifacts = new ArrayList<>();
        this.errors = new ArrayList<>();
    }

    public List<ArtifactAppEntity> getArtifacts() {
        return artifacts;
    }

    public void setArtifacts(List<ArtifactAppEntity> artifacts) {
        this.artifacts = artifacts;
    }

    public List<String> getErrors() {
        return errors;
    }

    public void setErrors(List<String> errors) {
        this.errors = errors;
    }
}
