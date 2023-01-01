package edu.nd.crc.safa.features.projects.services;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.services.AttributeService;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.services.CurrentDocumentService;
import edu.nd.crc.safa.features.documents.services.DocumentService;
import edu.nd.crc.safa.features.errors.services.CommitErrorRetrievalService;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.layout.services.ArtifactPositionService;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.memberships.services.MemberService;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.services.ModelService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectParsingErrors;
import edu.nd.crc.safa.features.rules.parser.RuleName;
import edu.nd.crc.safa.features.rules.services.WarningService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.services.TraceService;
import edu.nd.crc.safa.features.types.TypeAppEntity;
import edu.nd.crc.safa.features.types.TypeService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
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
@AllArgsConstructor
public class ProjectRetrievalService {

    private final ArtifactService artifactService;
    private final TraceService traceService;
    private final MemberService memberService;
    private final DocumentService documentService;
    private final CurrentDocumentService currentDocumentService;
    private final TypeService typeService;
    private final ArtifactPositionService artifactPositionService;
    private final WarningService warningService;
    private final CommitErrorRetrievalService commitErrorRetrievalService;
    private final ModelService modelService;
    private final AttributeService attributeService;

    /**
     * Creates a project application entity containing the entities (e.g. traces, artifacts) from
     * the given version. Further, gathers the list of project members at the time of being called.
     *
     * @param projectVersion The point in the project whose entities are being retrieved.
     * @return ProjectAppEntity Entity containing project name, description, artifacts, and traces.
     */
    public ProjectAppEntity getProjectAppEntity(ProjectVersion projectVersion) {
        // Versioned Entities
        ProjectEntities entities = retrieveProjectEntitiesAtProjectVersion(projectVersion);

        // Project Entities
        List<ProjectMemberAppEntity> projectMembers = this.memberService.getAppEntities(projectVersion);

        // Documents
        List<DocumentAppEntity> documents = this.documentService.getAppEntities(projectVersion);

        // Current document
        String currentDocumentId = this.currentDocumentService.getCurrentDocumentId();

        // Artifact types
        List<TypeAppEntity> artifactTypes = this.typeService.getAppEntities(projectVersion);

        // Version errors
        ProjectParsingErrors errors = this.commitErrorRetrievalService.collectErrorsInVersion(projectVersion);

        // Artifact warnings
        Map<UUID, List<RuleName>> warnings = this.warningService.retrieveWarningsInProjectVersion(projectVersion);

        // Layout
        Map<UUID, LayoutPosition> layout = artifactPositionService.retrieveDocumentLayout(projectVersion, null);

        List<ModelAppEntity> models = this.modelService.getUserModels();

        List<CustomAttributeAppEntity> attributes = this.attributeService
            .getAttributeEntitiesForProject(projectVersion.getProject(), Sort.by("label"));

        return new ProjectAppEntity(projectVersion,
            entities.getArtifacts(),
            entities.getTraces(),
            projectMembers,
            documents,
            currentDocumentId,
            artifactTypes,
            warnings,
            errors,
            layout,
            models,
            attributes);
    }

    /**
     * Retrieves artifact and trace links in given version.
     *
     * @param projectVersion The version of the entities to retrieve.
     * @return {@link ProjectEntities} Artifacts and trace links at given version.
     */
    public ProjectEntities retrieveProjectEntitiesAtProjectVersion(ProjectVersion projectVersion) {
        List<ArtifactAppEntity> artifacts = this.artifactService
            .getAppEntities(projectVersion);
        List<UUID> artifactIds = artifacts
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());
        List<TraceAppEntity> traces = this.traceService
            .retrieveActiveTraces(projectVersion, artifactIds);
        return new ProjectEntities(artifacts, traces);
    }
}
