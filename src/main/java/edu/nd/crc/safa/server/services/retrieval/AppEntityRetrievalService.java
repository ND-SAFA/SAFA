package edu.nd.crc.safa.server.services.retrieval;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.DocumentAppEntity;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ProjectParsingErrors;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.FTAArtifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.artifacts.FTAArtifactRepository;
import edu.nd.crc.safa.server.repositories.artifacts.SafetyCaseArtifactRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentArtifactRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;
import edu.nd.crc.safa.server.repositories.projects.ProjectMembershipRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.WarningService;
import edu.nd.crc.safa.warnings.RuleName;

import org.springframework.beans.factory.annotation.Autowired;
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
public class AppEntityRetrievalService {

    private final DocumentRepository documentRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final ArtifactVersionRepository artifactVersionRepository;
    private final ArtifactTypeRepository artifactTypeRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final SafetyCaseArtifactRepository safetyCaseArtifactRepository;
    private final FTAArtifactRepository ftaArtifactRepository;
    private final CommitErrorRetrievalService commitErrorRetrievalService;
    private final WarningService warningService;

    @Autowired
    public AppEntityRetrievalService(DocumentRepository documentRepository,
                                     TraceLinkVersionRepository traceLinkVersionRepository,
                                     DocumentArtifactRepository documentArtifactRepository,
                                     ProjectMembershipRepository projectMembershipRepository,
                                     ArtifactVersionRepository artifactVersionRepository,
                                     ArtifactTypeRepository artifactTypeRepository,
                                     SafetyCaseArtifactRepository safetyCaseArtifactRepository,
                                     FTAArtifactRepository ftaArtifactRepository,
                                     CommitErrorRetrievalService commitErrorRetrievalService,
                                     WarningService warningService) {
        this.documentRepository = documentRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.documentArtifactRepository = documentArtifactRepository;
        this.artifactVersionRepository = artifactVersionRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.projectMembershipRepository = projectMembershipRepository;
        this.safetyCaseArtifactRepository = safetyCaseArtifactRepository;
        this.ftaArtifactRepository = ftaArtifactRepository;
        this.commitErrorRetrievalService = commitErrorRetrievalService;
        this.warningService = warningService;
    }

    /**
     * Finds project, artifact, traces, errors, and warnings related with given project version.
     *
     * @param projectVersion Version whose artifacts are used to generate warnings and error
     * @return ProjectCreationResponse containing all relevant project entities
     */
    public ProjectEntities retrieveProjectEntitiesAtProjectVersion(ProjectVersion projectVersion) {
        ProjectAppEntity projectAppEntity = this.retrieveProjectAppEntityAtProjectVersion(projectVersion);
        ProjectParsingErrors projectParsingErrors = this.commitErrorRetrievalService
            .collectionProjectErrors(projectVersion);
        Map<String, List<RuleName>> projectWarnings = this.retrieveWarningsInProjectVersion(projectVersion);
        return new ProjectEntities(projectAppEntity, projectVersion, projectParsingErrors, projectWarnings);
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
        List<ArtifactAppEntity> artifacts = getArtifactsInProjectVersion(projectVersion);
        List<String> artifactIds = artifacts.stream().map(ArtifactAppEntity::getId).collect(Collectors.toList());
        List<TraceAppEntity> traces = getTracesInProjectVersion(projectVersion, artifactIds);

        // Project Entities
        List<ProjectMemberAppEntity> projectMembers = getMembersInProject(project);
        List<DocumentAppEntity> documents = this.getDocumentsInProject(project);

        // Artifact types
        List<ArtifactType> artifactTypes = this.artifactTypeRepository.findByProject(project);

        return new ProjectAppEntity(projectVersion, artifacts, traces, projectMembers, documents, artifactTypes);
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
    public List<ArtifactAppEntity> getArtifactsInProjectVersion(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifactBodies = artifactVersionRepository
            .getVersionEntitiesByProjectVersion(projectVersion);
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        for (ArtifactVersion artifactVersion : artifactBodies) {
            artifacts.add(retrieveArtifactAppEntityInProjectVersion(projectVersion, artifactVersion));
        }
        return artifacts;
    }

    /**
     * Returns ArtifactAppEntity associated with ArtifactVersion in given project version with
     * any Safety Case or FTA information inserted into app entity.
     *
     * @param projectVersion  The project version associated with returned ArtifactAppEntity.
     * @param artifactVersion The artifact version used to populate the artifact.
     * @return The populated ArtifactAppEntity
     */
    public ArtifactAppEntity retrieveArtifactAppEntityInProjectVersion(ProjectVersion projectVersion,
                                                                       ArtifactVersion artifactVersion) {
        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(artifactVersion);

        Artifact artifact = artifactVersion.getArtifact();
        List<String> documentIds =
            this.documentArtifactRepository
                .findByProjectVersionAndArtifact(projectVersion, artifact)
                .stream()
                .map(da -> da.getDocument().getDocumentId().toString())
                .collect(Collectors.toList());
        artifactAppEntity.setDocumentIds(documentIds);

        switch (artifact.getDocumentType()) {
            case SAFETY_CASE:
                Optional<SafetyCaseArtifact> safetyCaseArtifactOptional =
                    this.safetyCaseArtifactRepository.findByArtifact(artifact);
                if (safetyCaseArtifactOptional.isPresent()) {
                    SafetyCaseArtifact safetyCaseArtifact = safetyCaseArtifactOptional.get();
                    artifactAppEntity.setDocumentType(DocumentType.SAFETY_CASE);
                    artifactAppEntity.setSafetyCaseType(safetyCaseArtifact.getSafetyCaseType());
                }
                //TODO: Throw error if not found?
                break;
            case FTA:
                Optional<FTAArtifact> ftaArtifactOptional = this.ftaArtifactRepository.findByArtifact(artifact);
                if (ftaArtifactOptional.isPresent()) {
                    FTAArtifact ftaArtifact = ftaArtifactOptional.get();
                    artifactAppEntity.setDocumentType(DocumentType.FTA);
                    artifactAppEntity.setLogicType(ftaArtifact.getLogicType());
                }
                break;
            default:
                break;
        }
        return artifactAppEntity;
    }

    /**
     * Returns the list of traces in the given project version.
     *
     * @param projectVersion The version of the project whose links are returned.
     * @return List of TraceAppEntity
     */
    public List<TraceAppEntity> getTracesInProjectVersion(ProjectVersion projectVersion) {
        List<ArtifactAppEntity> projectVersionArtifacts = getArtifactsInProjectVersion(projectVersion);
        List<String> projectVersionArtifactIds = projectVersionArtifacts
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());
        return getTracesInProjectVersion(projectVersion, projectVersionArtifactIds);
    }

    /**
     * Returns the list of traces currently active in given version.
     *
     * @param projectVersion      The project version whose traces are returned if existing in it.
     * @param existingArtifactIds List of artifact ids for those existing in given version.
     * @return List of trace links existing in given version at the time of calling this.
     */
    public List<TraceAppEntity> getTracesInProjectVersion(ProjectVersion projectVersion,
                                                          List<String> existingArtifactIds) {
        return this.traceLinkVersionRepository
            .getVersionEntitiesByProjectVersion(projectVersion)
            .stream()
            .map(TraceAppEntity::new)
            .filter(t -> existingArtifactIds.contains(t.sourceId)
                && existingArtifactIds.contains(t.targetId))
            .collect(Collectors.toList());
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
            .getVersionEntitiesByProjectVersion(projectVersion)
            .stream()
            .map(TraceAppEntity::new)
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
            List<String> artifactIds = this.documentArtifactRepository.findByDocument(document)
                .stream()
                .map(da -> da.getArtifact().getArtifactId().toString())
                .collect(Collectors.toList());
            DocumentAppEntity documentAppEntity = new DocumentAppEntity(document, artifactIds);
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
        List<ArtifactVersion> artifacts = artifactVersionRepository.getVersionEntitiesByProjectVersion(projectVersion);
        List<TraceLink> traceLinks =
            this.traceLinkVersionRepository
                .getVersionEntitiesByProjectVersion(projectVersion)
                .stream()
                .filter(t -> t.getApprovalStatus() == TraceApproval.APPROVED)
                .map(TraceLinkVersion::getTraceLink)
                .collect(Collectors.toList());
        return this.warningService.generateWarningsOnEntities(projectVersion.getProject(), artifacts, traceLinks);
    }
}
