package edu.nd.crc.safa.server.responses;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

public class ProjectCreationResponse {
    ProjectAppEntity project;
    ProjectVersion projectVersion;
    ProjectErrors errors;
    Map<String, List<RuleName>> warnings;

    public ProjectCreationResponse(ProjectAppEntity project,
                                   ProjectVersion projectVersion,
                                   ProjectErrors errors,
                                   Map<String, List<RuleName>> warnings) {
        this.project = project;
        this.projectVersion = projectVersion;
        this.errors = errors;
        this.warnings = warnings;
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

    public Map<String, List<RuleName>> getWarnings() {
        return warnings;
    }

    public void setWarnings(Map<String, List<RuleName>> warnings) {
        this.warnings = warnings;
    }
}
