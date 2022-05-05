package edu.nd.crc.safa.server.entities.api;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

/**
 * Container for all entities related to a project including:
 * 1. Project identifying information
 * 2. Current project version
 * 3. Any errors occurring in the project.
 * 4. Any warnings about the current project version.
 */
public class ProjectEntities {

    ProjectAppEntity project;
    ProjectVersion projectVersion;
    ProjectParsingErrors errors;
    Map<String, List<RuleName>> warnings;

    public ProjectEntities() {
    }

    public ProjectEntities(ProjectAppEntity project,
                           ProjectVersion projectVersion,
                           ProjectParsingErrors errors,
                           Map<String, List<RuleName>> warnings) {
        this.project = project;
        this.projectVersion = projectVersion;
        this.errors = errors;
        this.warnings = warnings;
    }

    /**
     * {@Link ProjectEntities#project}
     *
     * @return Front-end project object.
     */
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

    public ProjectParsingErrors getErrors() {
        return this.errors;
    }

    public void setErrors(ProjectParsingErrors errors) {
        this.errors = errors;
    }

    public Map<String, List<RuleName>> getWarnings() {
        return warnings;
    }

    public void setWarnings(Map<String, List<RuleName>> warnings) {
        this.warnings = warnings;
    }
}
