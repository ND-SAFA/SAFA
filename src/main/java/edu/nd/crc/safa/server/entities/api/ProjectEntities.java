package edu.nd.crc.safa.server.entities.api;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Container for all entities related to a project including:
 * 1. Project identifying information
 * 2. Current project version
 * 3. Any errors occurring in the project.
 * 4. Any warnings about the current project version.
 */
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class ProjectEntities {

    /**
     * The FEND project name, description, artifacts, and traces.
     */
    ProjectAppEntity project;
    /**
     * The project version associated with artifacts, traces, warnings, and errors.
     */
    ProjectVersion projectVersion;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    Map<String, List<RuleName>> warnings;

    public ProjectEntities(ProjectAppEntity project,
                           ProjectVersion projectVersion) {
        this(project, projectVersion, new Hashtable<>());
    }
}
