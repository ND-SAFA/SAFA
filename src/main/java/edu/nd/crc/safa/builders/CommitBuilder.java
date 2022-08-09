package edu.nd.crc.safa.builders;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;

/**
 * Provides an API for building commits using the builder design pattern.
 */
public class CommitBuilder {

    private final ProjectCommit projectCommit;

    public CommitBuilder(ProjectVersion projectVersion) {
        projectCommit = new ProjectCommit(projectVersion, true);
    }

    public static CommitBuilder withVersion(ProjectVersion projectVersion) {
        return (new CommitBuilder(projectVersion));
    }

    public CommitBuilder withAddedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        this.projectCommit.getArtifacts().getAdded().add(asArtifactAppEntity(artifactJson));
        return this;
    }

    public CommitBuilder withRemovedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        this.projectCommit.getArtifacts().getRemoved().add(asArtifactAppEntity(artifactJson));
        return this;
    }

    public CommitBuilder withModifiedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        this.projectCommit.getArtifacts().getModified().add(asArtifactAppEntity(artifactJson));
        return this;
    }

    public CommitBuilder withAddedTrace(JSONObject json) throws JsonProcessingException {
        this.projectCommit.getTraces().getAdded().add(asTraceAppEntity(json));
        return this;
    }

    public CommitBuilder withModifiedTrace(TraceAppEntity traceAppEntity) {
        this.projectCommit.getTraces().getModified().add(traceAppEntity);
        return this;
    }

    public JSONObject asJson() throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        String commitString = objectMapper.writeValueAsString(this.projectCommit);
        return new JSONObject(commitString);
    }

    public ProjectCommit get() {
        return this.projectCommit;
    }

    private ArtifactAppEntity asArtifactAppEntity(JSONObject json) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(json.toString(), ArtifactAppEntity.class);
    }

    private TraceAppEntity asTraceAppEntity(JSONObject json) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(json.toString(), TraceAppEntity.class);
    }
}
