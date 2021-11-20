package edu.nd.crc.safa.builders;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;

public class ProjectCommitBuilder {

    ProjectCommit projectCommit;

    public ProjectCommitBuilder(ProjectVersion projectVersion) {
        projectCommit = new ProjectCommit(projectVersion);
    }

    public static ProjectCommitBuilder withVersion(ProjectVersion projectVersion) {
        return (new ProjectCommitBuilder(projectVersion));
    }

    public ProjectCommitBuilder withAddedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        this.projectCommit.getArtifacts().getAdded().add(asArtifactAppEntity(artifactJson));
        return this;
    }

    public ProjectCommitBuilder withRemovedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        this.projectCommit.getArtifacts().getRemoved().add(asArtifactAppEntity(artifactJson));
        return this;
    }

    public ProjectCommitBuilder withModifiedArtifact(JSONObject artifactJson) throws JsonProcessingException {
        this.projectCommit.getArtifacts().getModified().add(asArtifactAppEntity(artifactJson));
        return this;
    }

    private ArtifactAppEntity asArtifactAppEntity(JSONObject json) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(json.toString(), ArtifactAppEntity.class);
    }

    public ProjectCommitBuilder withAddedTrace(TraceAppEntity trace) {
        this.projectCommit.getTraces().getAdded().add(trace);
        return this;
    }

    public ProjectCommitBuilder withRemovedTrace(TraceAppEntity trace) {
        this.projectCommit.getTraces().getRemoved().add(trace);
        return this;
    }

    public ProjectCommitBuilder withModifiedTrace(TraceAppEntity trace) {
        this.projectCommit.getTraces().getModified().add(trace);
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
}
