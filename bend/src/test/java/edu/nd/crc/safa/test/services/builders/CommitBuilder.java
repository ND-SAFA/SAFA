package edu.nd.crc.safa.test.services.builders;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;

/**
 * Provides an API for building commits using the builder design pattern.
 */
public class CommitBuilder {

    private final ProjectCommitDefinition projectCommitDefinition;

    public CommitBuilder(ProjectVersion projectVersion) {
        projectCommitDefinition = new ProjectCommitDefinition(null, projectVersion, true);
    }

    public static CommitBuilder withVersion(ProjectVersion projectVersion) {
        return (new CommitBuilder(projectVersion));
    }

    public CommitBuilder withAddedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        return withAddedArtifact(asArtifactAppEntity(artifactJson));
    }

    public CommitBuilder withAddedArtifact(ArtifactAppEntity artifact) {
        this.projectCommitDefinition.addArtifact(ModificationType.ADDED, artifact);
        return this;
    }

    public CommitBuilder withRemovedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        return withRemovedArtifact(asArtifactAppEntity(artifactJson));
    }

    public CommitBuilder withRemovedArtifact(ArtifactAppEntity artifact) {
        this.projectCommitDefinition.addArtifact(ModificationType.REMOVED, artifact);
        return this;
    }

    public CommitBuilder withModifiedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        return withModifiedArtifact(asArtifactAppEntity(artifactJson));
    }

    public CommitBuilder withModifiedArtifact(ArtifactAppEntity artifact) {
        this.projectCommitDefinition.addArtifact(ModificationType.MODIFIED, artifact);
        return this;
    }

    public CommitBuilder withAddedTrace(JSONObject traceJson) throws JsonProcessingException {
        return withAddedTrace(asTraceAppEntity(traceJson));
    }

    public CommitBuilder withAddedTrace(TraceAppEntity trace) {
        this.projectCommitDefinition.addTrace(ModificationType.ADDED, trace);
        return this;
    }

    public CommitBuilder withModifiedTrace(TraceAppEntity traceAppEntity) {
        this.projectCommitDefinition.addTrace(ModificationType.MODIFIED, traceAppEntity);
        return this;
    }

    public CommitBuilder withRemovedTrace(TraceAppEntity traceAppEntity) {
        this.projectCommitDefinition.addTrace(ModificationType.REMOVED, traceAppEntity);
        return this;
    }

    public JSONObject asJson() {
        try {
            ObjectMapper objectMapper = ObjectMapperConfig.create();
            String commitString = objectMapper.writeValueAsString(this.projectCommitDefinition);
            return new JSONObject(commitString);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public ProjectCommitDefinition get() {
        return this.projectCommitDefinition;
    }

    private ArtifactAppEntity asArtifactAppEntity(JSONObject json) throws JsonProcessingException {
        ObjectMapper objectMapper = ObjectMapperConfig.create();
        return objectMapper.readValue(json.toString(), ArtifactAppEntity.class);
    }

    private TraceAppEntity asTraceAppEntity(JSONObject json) throws JsonProcessingException {
        ObjectMapper objectMapper = ObjectMapperConfig.create();
        return objectMapper.readValue(json.toString(), TraceAppEntity.class);
    }
}
