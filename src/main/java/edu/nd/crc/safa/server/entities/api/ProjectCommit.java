package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * The model used to commit a change to the versioning system.
 */
public class ProjectCommit {

    ProjectVersion commitVersion;
    ProjectChange<ArtifactAppEntity> artifacts;
    ProjectChange<TraceAppEntity> traces;
    List<CommitError> errors;
    boolean failOnError;

    public ProjectCommit() {
        this.artifacts = new ProjectChange<>();
        this.traces = new ProjectChange<>();
        this.errors = new ArrayList<>();
        this.failOnError = true;
    }

    public ProjectCommit(ProjectVersion commitVersion, boolean failOnError) {
        this();
        this.commitVersion = commitVersion;
        this.failOnError = failOnError;
    }

    public ProjectCommit(ProjectVersion projectVersion,
                         ProjectChange<ArtifactAppEntity> artifacts,
                         ProjectChange<TraceAppEntity> traces,
                         List<CommitError> errors,
                         boolean failOnError) {
        this();
        this.commitVersion = projectVersion;
        this.artifacts = artifacts;
        this.traces = traces;
        this.errors = errors;
        this.failOnError = failOnError;
    }

    public boolean isFailOnError() {
        return failOnError;
    }

    public void setFailOnError(boolean failOnError) {
        this.failOnError = failOnError;
    }

    public List<CommitError> getErrors() {
        return errors;
    }

    public void setErrors(List<CommitError> errors) {
        this.errors = errors;
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

    public void addTraceToDelete(List<TraceAppEntity> tracesToAdd) {
        List<TraceAppEntity> tracesToDelete = this.getTraces().getRemoved();
        List<TraceAppEntity> newTraces = tracesToAdd.stream()
            .filter(t -> !tracesToDelete.contains(t))
            .collect(Collectors.toList());
        newTraces.addAll(tracesToDelete);
        this.getTraces().setRemoved(newTraces);
    }
}
