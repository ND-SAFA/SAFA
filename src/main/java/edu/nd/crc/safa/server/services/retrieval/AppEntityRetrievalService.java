package edu.nd.crc.safa.server.services.retrieval;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.api.ProjectParsingErrors;
import edu.nd.crc.safa.server.entities.app.documents.DocumentAppEntity;
import edu.nd.crc.safa.server.entities.app.documents.DocumentColumnAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectMemberAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ApprovalStatus;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentArtifactRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentColumnRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.CurrentDocumentService;
import edu.nd.crc.safa.server.services.LayoutService;
import edu.nd.crc.safa.server.services.WarningService;
import edu.nd.crc.safa.warnings.RuleName;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
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
public class AppEntityRetrievalService {

    private final DocumentRepository documentRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final ArtifactTypeRepository artifactTypeRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final DocumentColumnRepository documentColumnRepository;
    private final CurrentDocumentService currentDocumentService;

    private final WarningService warningService;
    private final CommitErrorRetrievalService commitErrorRetrievalService;
    private final LayoutService layoutService;

    /**
     * Finds project, artifact, traces, errors, and warnings related with given project version.
     *
     * @param projectVersion Version whose artifacts are used to generate warnings and error
     * @return ProjectCreationResponse containing all relevant project entities
     */
    public ProjectAppEntity retrieveProjectEntitiesAtProjectVersion(ProjectVersion projectVersion) {
        ProjectAppEntity projectAppEntity = this.retrieveProjectAppEntityAtProjectVersion(projectVersion);
        Map<String, List<RuleName>> warnings = this.retrieveWarningsInProjectVersion(projectVersion);
        projectAppEntity.setWarnings(warnings);
        return projectAppEntity;
    }

    /**
     * Creates a project application entity containing the entities (e.g. traces, artifacts) from
     * the given version. Further, gathers the list of project members at the time of being called.
     *
     * @param projectVersion The point in the project whose entities are being retrieved.
     * @return ProjectAppEntity Entity containing project name, description, artifacts, and traces.
     */
    public ProjectAppEntity retrieveProjectAppEntityAtProjectVersion(ProjectVersion projectVersion) {

        Project project = projectVersion.getProject();

        // Versioned Entities
        List<ArtifactAppEntity> artifacts = retrieveArtifactsInProjectVersion(projectVersion);
        List<String> artifactIds = artifacts
            .stream()
            .map(ArtifactAppEntity::getBaseEntityId)
            .collect(Collectors.toList());
        List<TraceAppEntity> traces = retrieveTracesInProjectVersion(projectVersion, artifactIds);

        // Project Entities
        List<ProjectMemberAppEntity> projectMembers = getMembersInProject(project);

        // Documents
        List<DocumentAppEntity> documents = this.getDocumentsInProject(project);
        setDocumentLayouts(artifacts, traces, documents);

        // Current document
        String currentDocumentId = this.currentDocumentService.getCurrentDocumentId();

        // Artifact types
        List<ArtifactType> artifactTypes = this.artifactTypeRepository.findByProject(project);

        // Version errors
        ProjectParsingErrors errors = this.commitErrorRetrievalService.collectErrorsInVersion(projectVersion);

        // Layout
        Map<String, LayoutPosition> layout = this.layoutService.generateLayoutForArtifactTree(artifacts, traces);

        return new ProjectAppEntity(projectVersion,
            artifacts,
            traces,
            projectMembers,
            documents,
            currentDocumentId,
            artifactTypes,
            errors,
            layout);
    }

    public void setDocumentLayouts(List<ArtifactAppEntity> projectArtifacts,
                                   List<TraceAppEntity> projectTraces,
                                   List<DocumentAppEntity> documents) {
        Map<String, Map<String, LayoutPosition>> documentLayouts = this
            .layoutService
            .retrieveDocumentLayouts(projectArtifacts, projectTraces, documents);
        for (DocumentAppEntity documentAppEntity : documents) {
            documentAppEntity.setLayout(documentLayouts.get(documentAppEntity.getDocumentId().toString()));
        }
    }

    /**
     * Returns the list of members in the given project.
     *
     * @param project The project whose members are being retrieved.
     * @return The list of project member app entities.
     */
    public List<ProjectMemberAppEntity> getMembersInProject(Project project) {
        return this.projectMembershipRepository.findByProject(project)
            .stream()
            .map(ProjectMemberAppEntity::new)
            .collect(Collectors.toList());
    }

    /**
     * Returns the current list of artifacts in the version given.
     *
     * @param projectVersion The version whose artifacts are retrieved.
     * @return List of artifact app entities as saved in project version.
     */
    public List<ArtifactAppEntity> retrieveArtifactsInProjectVersion(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifactBodies = artifactVersionRepository
            .retrieveVersionEntitiesByProjectVersion(projectVersion);
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        for (ArtifactVersion artifactVersion : artifactBodies) {
            ArtifactAppEntity artifactAppEntity = this.artifactVersionRepository
                .retrieveAppEntityFromVersionEntity(artifactVersion);
            artifacts.add(artifactAppEntity);
        }
        return artifacts;
    }

    /**
     * Returns the list of traces in the given project version.
     *
     * @param projectVersion The version of the project whose links are returned.
     * @return List of TraceAppEntity
     */
    public List<TraceAppEntity> retrieveTracesInProjectVersion(ProjectVersion projectVersion) {
        List<ArtifactAppEntity> projectVersionArtifacts = retrieveArtifactsInProjectVersion(projectVersion);
        List<String> projectVersionArtifactIds = projectVersionArtifacts
            .stream()
            .map(ArtifactAppEntity::getBaseEntityId)
            .collect(Collectors.toList());
        return retrieveTracesInProjectVersion(projectVersion, projectVersionArtifactIds);
    }

    /**
     * Returns the list of traces currently active in given version.
     *
     * @param projectVersion      The project version whose traces are returned if existing in it.
     * @param existingArtifactIds List of artifact ids for those existing in given version.
     * @return List of trace links existing in given version at the time of calling this.
     */
    public List<TraceAppEntity> retrieveTracesInProjectVersion(ProjectVersion projectVersion,
                                                               List<String> existingArtifactIds) {
        return this.traceLinkVersionRepository
            .retrieveAppEntitiesByProjectVersion(projectVersion)
            .stream()
            .filter(t -> existingArtifactIds.contains(t.sourceId)
                && existingArtifactIds.contains(t.targetId)
                && t.approvalStatus != ApprovalStatus.DECLINED)
            .collect(Collectors.toList());
        //TODO: Look at absorbing filter method into the retrieval method by default.
    }

    /**
     * Returns list of traces current active in project version containing
     * source or target as given artifact.
     *
     * @param projectVersion The project version used to retrieve active links.
     * @param artifactName   The artifact to be used to query links.
     * @return List of traces active in version and associated with artifact
     */
    public List<TraceAppEntity> getTracesInProjectVersionRelatedToArtifact(
        ProjectVersion projectVersion,
        String artifactName
    ) {
        return this.traceLinkVersionRepository
            .retrieveAppEntitiesByProjectVersion(projectVersion)
            .stream()
            .filter(t -> artifactName.equals(t.sourceName) || artifactName.equals(t.targetName))
            .collect(Collectors.toList());
    }

    /**
     * Returns list of documents in given project
     *
     * @param project The projects whose documents are returned.
     * @return List of documents in project.
     */
    public List<DocumentAppEntity> getDocumentsInProject(Project project) {
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        List<DocumentAppEntity> documentAppEntities = new ArrayList<>();
        for (Document document : projectDocuments) {
            // Retrieve linked artifact Ids
            List<String> artifactIds = this.documentArtifactRepository.findByDocument(document)
                .stream()
                .map(da -> da.getArtifact().getArtifactId().toString())
                .collect(Collectors.toList());
            //TODO: Retrieve artifact positions
            DocumentAppEntity documentAppEntity = new DocumentAppEntity(document, artifactIds, new Hashtable<>());

            // Retrieve FMEA columns
            if (document.getType() == DocumentType.FMEA) {
                List<DocumentColumnAppEntity> documentColumns = this.documentColumnRepository
                    .findByDocumentOrderByTableColumnIndexAsc(document)
                    .stream()
                    .map(DocumentColumnAppEntity::new)
                    .collect(Collectors.toList());
                documentAppEntity.setColumns(documentColumns);
            }

            documentAppEntities.add(documentAppEntity);
        }
        return documentAppEntities;
    }

    /**
     * Returns mapping of artifact name to the list of violations it is inhibiting.
     *
     * @param projectVersion - Finds violations in artifact tree at time of this version
     * @return A mapping of  artifact name's to their resulting violations
     */
    public Map<String, List<RuleName>> retrieveWarningsInProjectVersion(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifacts = artifactVersionRepository
            .retrieveVersionEntitiesByProjectVersion(projectVersion);
        List<TraceLink> traceLinks =
            this.traceLinkVersionRepository
                .retrieveVersionEntitiesByProjectVersion(projectVersion)
                .stream()
                .filter(t -> t.getApprovalStatus() == ApprovalStatus.APPROVED)
                .map(TraceLinkVersion::getTraceLink)
                .collect(Collectors.toList());
        return this.warningService.generateWarningsOnEntities(projectVersion.getProject(), artifacts, traceLinks);
    }
}
