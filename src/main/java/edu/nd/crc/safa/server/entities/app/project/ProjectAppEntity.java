package edu.nd.crc.safa.server.entities.app.project;

import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.app.documents.DocumentAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import lombok.Getter;
import lombok.Setter;
import org.json.JSONObject;

/**
 * Represents the front-end model of a project.
 */
@Getter
@Setter
public class ProjectAppEntity {
    @NotNull
    public String projectId;
    @NotNull
    public String name;
    @NotNull
    public String description;
    @Valid
    public ProjectVersion projectVersion;
    @NotNull
    public List<@Valid @NotNull ArtifactAppEntity> artifacts;
    @NotNull
    public List<@Valid @NotNull TraceAppEntity> traces;
    public List<ProjectMemberAppEntity> members;
    public List<DocumentAppEntity> documents;
    public List<ArtifactType> artifactTypes;

    public ProjectAppEntity() {
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
        this.members = new ArrayList<>();
        this.documents = new ArrayList<>();
        this.artifactTypes = new ArrayList<>();
    }

    public ProjectAppEntity(ProjectVersion projectVersion,
                            List<ArtifactAppEntity> artifacts,
                            List<TraceAppEntity> traces,
                            List<ProjectMemberAppEntity> members,
                            List<DocumentAppEntity> documents,
                            List<ArtifactType> artifactTypes) {
        this();
        Project project = projectVersion.getProject();
        this.projectId = project.getProjectId().toString();
        this.projectVersion = projectVersion;
        this.name = project.getName();
        this.description = project.getDescription();
        this.artifacts = artifacts;
        this.traces = traces;
        this.members = members;
        this.documents = documents;
        this.artifactTypes = artifactTypes;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("projectId", this.projectId);
        json.put("name", this.name);
        json.put("artifacts", artifacts);
        json.put("traces", traces);
        return json.toString();
    }
}
