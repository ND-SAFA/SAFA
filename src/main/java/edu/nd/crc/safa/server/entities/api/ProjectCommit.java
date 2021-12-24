package edu.nd.crc.safa.server.entities.api;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * The model used to commit a change to the versioning system.
 */
public class ProjectCommit {

    ProjectVersion commitVersion;
    ProjectChange<ArtifactAppEntity> artifacts;
    ProjectChange<TraceAppEntity> traces;

    public ProjectCommit() {
        artifacts = new ProjectChange<>();
        traces = new ProjectChange<>();

    }

    public ProjectCommit(ProjectVersion commitVersion) {
        this();
        this.commitVersion = commitVersion;
    }

    public ProjectVersion getCommitVersion() {
        return commitVersion;
    }

    public void setCommitVersion(ProjectVersion commitVersion) {
        this.commitVersion = commitVersion;
    }

    public ProjectChange<ArtifactAppEntity> getArtifacts() {
        return artifacts;
    }

    public void setArtifacts(ProjectChange<ArtifactAppEntity> artifacts) {
        this.artifacts = artifacts;
    }

    public ProjectChange<TraceAppEntity> getTraces() {
        return traces;
    }

    public void setTraces(ProjectChange<TraceAppEntity> traces) {
        this.traces = traces;
    }
}
