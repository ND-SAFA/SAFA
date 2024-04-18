package edu.nd.crc.safa.features.projects.services;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.attributes.entities.AttributeLayoutAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.services.AttributeLayoutService;
import edu.nd.crc.safa.features.attributes.services.AttributeService;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.services.CurrentDocumentService;
import edu.nd.crc.safa.features.documents.services.DocumentService;
import edu.nd.crc.safa.features.errors.services.CommitErrorRetrievalService;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.layout.services.ArtifactPositionService;
import edu.nd.crc.safa.features.memberships.services.MembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectParsingErrors;
import edu.nd.crc.safa.features.projects.entities.app.SubtreeAppEntity;
import edu.nd.crc.safa.features.projects.graph.ProjectGraph;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.rules.services.WarningService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.traces.services.TraceMatrixService;
import edu.nd.crc.safa.features.traces.services.TraceService;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.context.annotation.Scope;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

/**
 * Responsible for all providing an API to retrieve and collect AppEntities including:
 * 1. ProjectEntities
 * 2. ProjectAppEntity
 * 3. ProjectMemberAppEntity
 * 4. ArtifactAppEntity
 * 5. TraceAppEntity
 * 6. DocumentAppEntity
 * 7. ProjectWarnings
 */
@Service
@Scope("singleton")
@RequiredArgsConstructor
public class ProjectRetrievalService {

    private final ArtifactService artifactService;
    private final TraceService traceService;
    private final MembershipService membershipService;
    private final DocumentService documentService;
    private final CurrentDocumentService currentDocumentService;
    private final TypeService typeService;
    private final ArtifactPositionService artifactPositionService;
    private final WarningService warningService;
    private final CommitErrorRetrievalService commitErrorRetrievalService;
    private final AttributeService attributeService;
    private final AttributeLayoutService attributeLayoutService;
    private final SafaUserService safaUserService;
    private final TraceMatrixService traceMatrixService;

    @Setter(onMethod = @__({@Autowired, @Lazy}))
    private ProjectService projectService;

    /**
     * Creates a project application entity containing the entities (e.g. traces, artifacts) from
     * the given version. Further, gathers the list of project members at the time of being called.
     *
     * @param projectVersion The point in the project whose entities are being retrieved.
     * @param user           The user making the request
     * @return ProjectAppEntity Entity containing project name, description, artifacts, and traces.
     */
    public ProjectAppEntity getProjectAppEntity(SafaUser user, ProjectVersion projectVersion) {
        // Versioned Entities
        ProjectEntities entities = retrieveProjectEntitiesAtProjectVersion(projectVersion, user);

        // Project Entities
        List<MembershipAppEntity> projectMembers = this.membershipService.getAppEntities(projectVersion, user);

        // Documents
        List<DocumentAppEntity> documents = this.documentService.getAppEntities(projectVersion, user);

        // Current document
        String currentDocumentId = this.currentDocumentService.getCurrentDocumentId(user);

        // Artifact types
        List<TypeAppEntity> artifactTypes = this.typeService.getAppEntities(projectVersion, user);

        // Version errors
        ProjectParsingErrors errors = this.commitErrorRetrievalService.collectErrorsInVersion(projectVersion);

        // Artifact warnings
        Map<UUID, List<RuleName>> warnings
            = this.warningService.retrieveWarningsForAppEntities(projectVersion.getProject(), entities);

        // Layout
        Map<UUID, LayoutPosition> layout = artifactPositionService.retrieveDocumentLayout(projectVersion, null);

        List<CustomAttributeAppEntity> attributes = this.attributeService
            .getAttributeEntitiesForProject(projectVersion.getProject(), Sort.by("label"));

        List<AttributeLayoutAppEntity> attributeLayouts =
            this.attributeLayoutService.getAppEntities(projectVersion, user);

        ProjectGraph graph = new ProjectGraph(entities);
        Map<UUID, SubtreeAppEntity> subtrees = graph.getSubtreeInfo();

        List<TraceMatrixAppEntity> traceMatrices = traceMatrixService.getAppEntities(projectVersion, user);

        List<String> permissions = projectService.getUserPermissions(projectVersion.getProject(), user)
            .stream()
            .filter(permission -> permission instanceof ProjectPermission)
            .map(Permission::getName)
            .collect(Collectors.toUnmodifiableList());

        return new ProjectAppEntity(
            projectVersion,
            entities.getArtifacts(),
            entities.getTraces(),
            projectMembers,
            documents,
            currentDocumentId,
            artifactTypes,
            warnings,
            errors,
            layout,
            attributes,
            attributeLayouts,
            subtrees,
            traceMatrices,
            permissions);
    }

    /**
     * Creates a project application entity containing the entities (e.g. traces, artifacts) from
     * the given version. Further, gathers the list of project members at the time of being called.
     *
     * @param projectVersion The point in the project whose entities are being retrieved.
     * @return ProjectAppEntity Entity containing project name, description, artifacts, and traces.
     */
    public ProjectAppEntity getProjectAppEntity(ProjectVersion projectVersion) {
        return getProjectAppEntity(safaUserService.getCurrentUser(), projectVersion);
    }

    /**
     * Retrieves artifact and trace links in given version.
     *
     * @param projectVersion The version of the entities to retrieve.
     * @param user           The user making the request
     * @return {@link ProjectEntities} Artifacts and trace links at given version.
     */
    public ProjectEntities retrieveProjectEntitiesAtProjectVersion(ProjectVersion projectVersion, SafaUser user) {
        List<ArtifactAppEntity> artifacts = this.artifactService
            .getAppEntities(projectVersion, user);
        List<UUID> artifactIds = artifacts
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());
        List<TraceAppEntity> traces = this.traceService
            .retrieveActiveTraces(projectVersion, artifactIds);
        return new ProjectEntities(artifacts, traces);
    }
}
