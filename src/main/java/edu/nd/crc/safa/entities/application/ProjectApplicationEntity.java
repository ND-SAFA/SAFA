package edu.nd.crc.safa.entities.application;

import java.util.List;

import edu.nd.crc.safa.entities.database.Project;

public class ProjectApplicationEntity {

    public String projectId;
    public String name;
    public List<ArtifactApplicationEntity> artifacts;
    public List<TraceApplicationEntity> traces;

    public ProjectApplicationEntity() {
    }

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

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
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
