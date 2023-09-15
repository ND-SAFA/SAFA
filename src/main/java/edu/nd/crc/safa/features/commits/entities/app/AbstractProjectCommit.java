package edu.nd.crc.safa.features.commits.entities.app;

import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.Data;

@Data
public class AbstractProjectCommit {
    protected ProjectVersion commitVersion;
    protected ProjectChange<@Valid ArtifactAppEntity> artifacts = new ProjectChange<>();
    protected ProjectChange<@Valid TraceAppEntity> traces = new ProjectChange<>();
    protected List<CommitError> errors = new ArrayList<>();
    protected boolean failOnError = true;
    protected SafaUser user;

    public void addErrors(List<CommitError> errors) {
        this.errors.addAll(errors);
    }
}
