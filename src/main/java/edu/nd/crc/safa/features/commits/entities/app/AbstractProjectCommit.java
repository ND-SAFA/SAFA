package edu.nd.crc.safa.features.commits.entities.app;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.validation.Valid;
import lombok.Data;

@Data
public class AbstractProjectCommit {
    private List<CommitError> errors = new ArrayList<>();
    private boolean failOnError = false;
    private SafaUser user;
    private ProjectVersion commitVersion;
    private ProjectChange<@Valid ArtifactAppEntity> artifacts = new ProjectChange<>();
    private ProjectChange<@Valid TraceAppEntity> traces = new ProjectChange<>();

    public void addErrors(List<CommitError> errors) {
        this.errors.addAll(errors);
    }
}
