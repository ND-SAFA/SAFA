package edu.nd.crc.safa.features.projects.entities.app;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.errors.entities.app.ErrorApplicationEntity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

/**
 * Container for errors occurring while parsing a project organized by the
 * activities they can occur in.
 */
@AllArgsConstructor
@Getter
@Setter
public class ProjectParsingErrors {
    private List<ErrorApplicationEntity> tim;
    private List<ErrorApplicationEntity> artifacts;
    private List<ErrorApplicationEntity> traces;

    public ProjectParsingErrors() {
        this.tim = new ArrayList<>();
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
    }
}
