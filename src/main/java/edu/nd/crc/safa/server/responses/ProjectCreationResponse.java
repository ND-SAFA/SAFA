package edu.nd.crc.safa.server.responses;

import edu.nd.crc.safa.db.entities.app.ProjectAppEntity;

public class ProjectCreationResponse {
    ProjectAppEntity project;
    ProjectErrors errors;

    public ProjectCreationResponse(ProjectAppEntity project, ProjectErrors errors) {
        this.project = project;
        this.errors = errors;
    }

    public ProjectAppEntity getProject() {
        return this.project;
    }

    public void setProject(ProjectAppEntity project) {
        this.project = project;
    }

    public ProjectErrors getErrors() {
        return this.errors;
    }

    public void setErrors(ProjectErrors errors) {
        this.errors = errors;
    }
}
