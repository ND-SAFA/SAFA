package edu.nd.crc.safa.db.entities.application;

import java.util.List;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;

public class ProjectApplicationEntity {

    public String projectId;
    public String name;
    public String projectVersion;
    public List<ArtifactApplicationEntity> artifacts;
    public List<TraceApplicationEntity> traces;

    public ProjectApplicationEntity() {
    }

    public ProjectApplicationEntity(ProjectVersion projectVersion,
                                    List<ArtifactApplicationEntity> artifacts,
                                    List<TraceApplicationEntity> traces) {
        Project project = projectVersion.getProject();
        this.projectId = project.getProjectId().toString();
        this.projectVersion = String.valueOf(projectVersion.getVersionId());
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
