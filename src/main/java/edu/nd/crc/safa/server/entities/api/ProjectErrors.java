package edu.nd.crc.safa.server.entities.api;

import java.util.List;

import edu.nd.crc.safa.server.entities.app.ErrorApplicationEntity;

public class ProjectErrors {
    List<ErrorApplicationEntity> tim;
    List<ErrorApplicationEntity> artifacts;
    List<ErrorApplicationEntity> traces;

    public ProjectErrors(List<ErrorApplicationEntity> tim,
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
}
