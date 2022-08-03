package edu.nd.crc.safa.features.commits.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import lombok.Getter;
import lombok.Setter;

/**
 * The model used to commit a change to the versioning system.
 */
@Getter
@Setter
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

    public void addRemovedTraces(List<TraceAppEntity> tracesToDelete) {
        List<TraceAppEntity> modifiedTraces = this.getTraces().getRemoved();
        List<TraceAppEntity> newTraces = tracesToDelete.stream()
            .filter(t -> !modifiedTraces.contains(t))
            .collect(Collectors.toList());
        newTraces.addAll(modifiedTraces);
        this.getTraces().setRemoved(newTraces);
    }
}
