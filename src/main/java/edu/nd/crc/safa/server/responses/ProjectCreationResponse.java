package edu.nd.crc.safa.server.responses;

import edu.nd.crc.safa.server.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;

public class ProjectCreationResponse {
    ProjectAppEntity project;
    ProjectVersion projectVersion;
    ProjectErrors errors;

    public ProjectCreationResponse(ProjectAppEntity project,
                                   ProjectVersion projectVersion,
                                   ProjectErrors errors) {
        this.project = project;
        this.projectVersion = projectVersion;
        this.errors = errors;
    }

    public ProjectAppEntity getProject() {
        return this.project;
    }

    public void setProject(ProjectAppEntity project) {
        this.project = project;
    }

    public ProjectVersion getProjectVersion() {
        return this.projectVersion;
    }

    public void setProjectVersion(ProjectVersion projectVersion) {
        this.projectVersion = projectVersion;
    }

    public ProjectErrors getErrors() {
        return this.errors;
    }

    public void setErrors(ProjectErrors errors) {
        this.errors = errors;
    }
}
