package edu.nd.crc.safa.features.projects.entities.app;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.annotation.Nullable;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.entities.AttributeLayoutAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Represents the front-end model of a project.
 */
@Data
public class ProjectAppEntity implements IAppEntity {
    private UUID projectId;

    private LocalDateTime lastEdited;

    @NotNull
    private String name;

    @NotNull
    private String description;

    @Valid
    private ProjectVersion projectVersion;

    @NotNull
    private List<@Valid @NotNull ArtifactAppEntity> artifacts;

    @NotNull
    private List<@Valid @NotNull TraceAppEntity> traces;

    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    private List<ProjectMemberAppEntity> members;

    @Nullable
    private String currentDocumentId;

    private List<@Valid @NotNull DocumentAppEntity> documents;

    private List<@Valid @NotNull TypeAppEntity> artifactTypes;

    private Map<UUID, List<@Valid @NotNull RuleName>> warnings;

    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    private ProjectParsingErrors errors;

    private Map<UUID, LayoutPosition> layout;

    private List<CustomAttributeAppEntity> attributes;

    private List<AttributeLayoutAppEntity> attributeLayouts;

    private Map<UUID, SubtreeAppEntity> subtrees;

    private List<TraceMatrixAppEntity> traceMatrices;

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
        this.attributes = new ArrayList<>();
        this.attributeLayouts = new ArrayList<>();
        this.subtrees = new HashMap<>();
        this.traceMatrices = new ArrayList<>();
        this.lastEdited = LocalDateTime.now();
    }

    public ProjectAppEntity(ProjectVersion projectVersion,
                            List<ArtifactAppEntity> artifacts,
                            List<TraceAppEntity> traces,
                            List<ProjectMemberAppEntity> members,
                            List<DocumentAppEntity> documents,
                            @Nullable String currentDocumentId,
                            List<TypeAppEntity> artifactTypes,
                            Map<UUID, List<@Valid @NotNull RuleName>> warnings,
                            ProjectParsingErrors errors,
                            Map<UUID, LayoutPosition> layout,
                            List<CustomAttributeAppEntity> attributes,
                            List<AttributeLayoutAppEntity> attributeLayouts,
                            Map<UUID, SubtreeAppEntity> subtrees,
                            List<TraceMatrixAppEntity> traceMatrices) {
        Project project = projectVersion.getProject();
        this.projectId = project.getProjectId();
        this.lastEdited = project.getLastEdited();
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
        this.attributes = attributes;
        this.attributeLayouts = attributeLayouts;
        this.subtrees = subtrees;
        this.traceMatrices = traceMatrices;
    }

    public ProjectAppEntity(ProjectCommitDefinition projectCommitDefinition) {
        this.artifacts = projectCommitDefinition.getArtifacts().getAdded();
        this.traces = projectCommitDefinition.getTraces().getAdded();
        this.projectVersion = projectCommitDefinition.getCommitVersion();
    }

    @JsonIgnore
    public static List<ArtifactAppEntity> filterByArtifactType(List<ArtifactAppEntity> artifacts, String artifactType) {
        return artifacts.stream().filter(a -> a.getType().equalsIgnoreCase(artifactType)).collect(Collectors.toList());
    }

    public List<String> getArtifactNames() {
        return this.artifacts
            .stream()
            .map(ArtifactAppEntity::getName)
            .collect(Collectors.toList());
    }

    @Override
    public UUID getId() {
        return this.projectId;
    }

    @Override
    public void setId(UUID id) {
        this.projectId = id;
    }

    @JsonIgnore
    public List<ArtifactAppEntity> getByArtifactType(String artifactType) {
        return filterByArtifactType(this.artifacts, artifactType);
    }
}
