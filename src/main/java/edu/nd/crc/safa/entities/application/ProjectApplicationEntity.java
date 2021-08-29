package edu.nd.crc.safa.responses;

import java.util.List;

import edu.nd.crc.safa.entities.Project;

public class ProjectApplicationEntity {
    String projectId;
    String name;
    List<ArtifactApplicationEntity> artifacts;
    List<TraceApplicationEntity> traces;

    public ProjectApplicationEntity(Project project,
                                    List<ArtifactApplicationEntity> artifacts,
                                    List<TraceApplicationEntity> traces) {
        this.projectId = project.getProjectId().toString();
        this.name = project.getName();
        this.artifacts = artifacts;
        this.traces = traces;
    }

    public String getProjectId() {
        return this.projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public List<ArtifactApplicationEntity> getArtifacts() {
        return this.artifacts;
    }

    public void setArtifacts(List<ArtifactApplicationEntity> artifacts) {
        this.artifacts = artifacts;
    }

    public List<TraceApplicationEntity> getTraces() {
        return this.traces;
    }

    public void setTraces(List<TraceApplicationEntity> traces) {
        this.traces = traces;
    }
}
