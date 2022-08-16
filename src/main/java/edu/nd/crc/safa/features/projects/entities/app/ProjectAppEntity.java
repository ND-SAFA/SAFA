package edu.nd.crc.safa.features.projects.entities.app;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import javax.annotation.Nullable;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.types.TypeAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Represents the front-end model of a project.
 */
@Data
public class ProjectAppEntity implements IAppEntity {
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
    public List<@Valid @NotNull TypeAppEntity> artifactTypes;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    Map<String, List<@Valid @NotNull RuleName>> warnings;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    ProjectParsingErrors errors;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    Map<String, LayoutPosition> layout;

    public ProjectAppEntity() {
        this.name = "";
        this.description = "";
        this.artifacts = new ArrayList<>();
        this.traces = new ArrayList<>();
        this.members = new ArrayList<>();
        this.documents = new ArrayList<>();
        this.artifactTypes = new ArrayList<>();
        this.warnings = new Hashtable<>();
        this.errors = new ProjectParsingErrors();
        this.layout = new Hashtable<>();
    }

    public ProjectAppEntity(ProjectVersion projectVersion,
                            List<ArtifactAppEntity> artifacts,
                            List<TraceAppEntity> traces,
                            List<ProjectMemberAppEntity> members,
                            List<DocumentAppEntity> documents,
                            @Nullable String currentDocumentId,
                            List<TypeAppEntity> artifactTypes,
                            Map<String, List<@Valid @NotNull RuleName>> warnings,
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
        this.warnings = warnings;
        this.errors = errors;
        this.layout = layout;
    }

    public List<String> getArtifactNames() {
        return this.artifacts
            .stream()
            .map(ArtifactAppEntity::getName)
            .collect(Collectors.toList());
    }

    @Override
    public String getBaseEntityId() {
        return this.projectId;
    }

    @Override
    public void setBaseEntityId(String id) {
        this.projectId = id;
    }
}
