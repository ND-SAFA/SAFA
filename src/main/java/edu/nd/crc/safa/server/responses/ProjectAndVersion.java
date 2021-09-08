package edu.nd.crc.safa.server.responses;

import edu.nd.crc.safa.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;

public class ProjectAndVersion {
    public ProjectAppEntity project;
    public ProjectVersion projectVersion;

    public ProjectAndVersion() {
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
}
