package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.app.ErrorApplicationEntity;

/**
 * Container for errors occurring while parsing a project organized by the
 * activities they can occur in.
 */
public class ProjectParsingErrors {
    List<ErrorApplicationEntity> tim;
    List<ErrorApplicationEntity> artifacts;
    List<ErrorApplicationEntity> traces;

    public ProjectParsingErrors() {
        this.tim = new ArrayList<>();
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
    }

    public ProjectParsingErrors(List<ErrorApplicationEntity> tim,
                                List<ErrorApplicationEntity> artifacts,
                                List<ErrorApplicationEntity> traces) {
        this.tim = tim;
        this.artifacts = artifacts;
        this.traces = traces;
    }

    public List<ErrorApplicationEntity> getTim() {
        return this.tim;
    }

    public void setTim(List<ErrorApplicationEntity> tim) {
        this.tim = tim;
    }

    public List<ErrorApplicationEntity> getArtifacts() {
        return this.artifacts;
    }

    public void setArtifacts(List<ErrorApplicationEntity> artifacts) {
        this.artifacts = artifacts;
    }

    public List<ErrorApplicationEntity> getTraces() {
        return this.traces;
    }

    public void setTraces(List<ErrorApplicationEntity> traces) {
        this.traces = traces;
    }

    public List<ErrorApplicationEntity> getAllErrors() {
        List<ErrorApplicationEntity> allErrors = new ArrayList<>();
        allErrors.addAll(this.tim);
        allErrors.addAll(this.artifacts);
        allErrors.addAll(this.traces);
        return allErrors;
    }
}
