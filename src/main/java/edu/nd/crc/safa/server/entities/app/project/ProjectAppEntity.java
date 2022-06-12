package edu.nd.crc.safa.server.entities.app.project;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import javax.annotation.Nullable;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.api.ProjectParsingErrors;
import edu.nd.crc.safa.server.entities.app.documents.DocumentAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.warnings.RuleName;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Represents the front-end model of a project.
 */
@Data
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
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    public List<ProjectMemberAppEntity> members;
    @Nullable
    public String currentDocumentId;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    public List<@Valid @NotNull DocumentAppEntity> documents;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    public List<@Valid @NotNull ArtifactType> artifactTypes;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    Map<String, List<@Valid @NotNull RuleName>> warnings;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    ProjectParsingErrors errors;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    Map<String, LayoutPosition> layout;

    public ProjectAppEntity() {
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
        this.members = new ArrayList<>();
        this.documents = new ArrayList<>();
        this.artifactTypes = new ArrayList<>();
        this.warnings = new Hashtable<>();
        this.errors = new ProjectParsingErrors();
    }

    public ProjectAppEntity(ProjectVersion projectVersion,
                            List<ArtifactAppEntity> artifacts,
                            List<TraceAppEntity> traces,
                            List<ProjectMemberAppEntity> members,
                            List<DocumentAppEntity> documents,
                            @Nullable String currentDocumentId,
                            List<ArtifactType> artifactTypes,
                            ProjectParsingErrors errors,
                            Map<String, LayoutPosition> layout) {
        this();
        Project project = projectVersion.getProject();
        this.projectId = project.getProjectId().toString();
        this.name = project.getName();
        this.description = project.getDescription();
        this.projectVersion = projectVersion;
        this.artifacts = artifacts;
        this.traces = traces;
        this.members = members;
        this.documents = documents;
        this.currentDocumentId = currentDocumentId;
        this.artifactTypes = artifactTypes;
        this.errors = errors;
        this.layout = layout;
    }
}
