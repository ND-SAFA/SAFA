package edu.nd.crc.safa.builders;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
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
        return withAddedArtifact(asArtifactAppEntity(artifactJson));
    }

    public CommitBuilder withAddedArtifact(ArtifactAppEntity artifact) {
        this.projectCommit.addArtifact(ModificationType.ADDED, artifact);
        return this;
    }

    public CommitBuilder withRemovedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        return withRemovedArtifact(asArtifactAppEntity(artifactJson));
    }

    public CommitBuilder withRemovedArtifact(ArtifactAppEntity artifact) {
        this.projectCommit.addArtifact(ModificationType.REMOVED, artifact);
        return this;
    }

    public CommitBuilder withModifiedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        return withModifiedArtifact(asArtifactAppEntity(artifactJson));
    }

    public CommitBuilder withModifiedArtifact(ArtifactAppEntity artifact) {
        this.projectCommit.addArtifact(ModificationType.MODIFIED, artifact);
        return this;
    }

    public CommitBuilder withAddedTrace(JSONObject traceJson) throws JsonProcessingException {
        this.projectCommit.addTrace(ModificationType.ADDED, asTraceAppEntity(traceJson));
        return this;
    }

    public CommitBuilder withModifiedTrace(TraceAppEntity traceAppEntity) {
        this.projectCommit.addTrace(ModificationType.MODIFIED, traceAppEntity);
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
