package edu.nd.crc.safa.server.responses;

import edu.nd.crc.safa.db.entities.application.ProjectApplicationEntity;

public class ProjectCreationResponse {
    ProjectApplicationEntity project;
    ProjectErrors errors;

    public ProjectCreationResponse(ProjectApplicationEntity project, ProjectErrors errors) {
        this.project = project;
        this.errors = errors;
    }

    public ProjectApplicationEntity getProject() {
        return this.project;
    }

    public void setProject(ProjectApplicationEntity project) {
        this.project = project;
    }

    public ProjectErrors getErrors() {
        return this.errors;
    }

    public void setErrors(ProjectErrors errors) {
        this.errors = errors;
    }
}
