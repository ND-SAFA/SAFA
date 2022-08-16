package edu.nd.crc.safa.features.layout.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.common.ProjectEntities;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.layout.generator.KlayLayoutGenerator;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

/**
 * Responsible for managing common layout on a project
 */
public class LayoutManager {

    /**
     * Project identifier
     */
    private final Project project;
    /**
     * Project version whose positions are associated with.
     */
    private final ProjectVersion projectVersion;
    /**
     * Service providing allowing the persistence of changes.
     */
    private final ServiceProvider serviceProvider;
    /**
     * Common data
     */
    private final ProjectEntities projectEntities;

    public LayoutManager(ServiceProvider serviceProvider,
                         ProjectVersion projectVersion) {
        if (projectVersion == null) {
            throw new IllegalArgumentException("Project version is null.");
        }
        if (projectVersion.getProject() == null) {
            throw new IllegalArgumentException("Project within project version is null.");
        }
        this.projectVersion = projectVersion;
        this.project = projectVersion.getProject();
        this.projectEntities = serviceProvider
            .getProjectRetrievalService()
            .retrieveProjectEntitiesAtProjectVersion(projectVersion);
        this.serviceProvider = serviceProvider;
    }

    /**
     * For each document,
     * - Generates layout according to its entities
     * - Persists layout for document
     * - Notify all users of project that all layouts have been updated
     */
    public void generateLayoutForProject() {
        generateDefaultDocumentLayout();
        this.serviceProvider
            .getDocumentRepository()
            .findByProject(this.project)
            .forEach(d -> generateDocumentLayout(d, false));
        this.serviceProvider
            .getNotificationService()
            .broadcastProjectLayoutMessage(projectVersion);
    }

    /**
     * 1. Generates list of affected documents
     * 2. For each document:
     * - generate new layout
     * - persist layout
     * - notify users of document that new layout exists
     *
     * @param projectCommit The changes to the artifact tree to calculate layout changes.
     */
    public void generateLayoutUpdates(ProjectCommit projectCommit) {
        // Step - Extract artifact causing stale layouts
        List<ArtifactAppEntity> affectedArtifacts = new ArrayList<>();
        affectedArtifacts.addAll(projectCommit.getArtifacts().getAdded());
        affectedArtifacts.addAll(projectCommit.getArtifacts().getRemoved());

        // Step - Generate affected documents
        List<Document> affectedDocuments = retrieveAffectedDocuments(affectedArtifacts);

        // Step - Generate layout for those documents
        for (Document affectedDocument : affectedDocuments) {
            generateDocumentLayout(affectedDocument, true);
        }

        // Step - Generate layout for default document
        generateDefaultDocumentLayout();
    }

    /**
     * Creates layout for given document
     *
     * @param document         Document whose layout will be generated.
     * @param sendNotification Whether to send notification to subscribers
     * @return Map of artifact id to their layout position.
     */
    public Map<String, LayoutPosition> generateDocumentLayout(Document document, boolean sendNotification) {
        // Step - Get entities in document
        ProjectEntities entities = this.projectEntities.getEntitiesInDocument(document);

        // Step - Generate layout
        Map<String, LayoutPosition> artifact2position = generateLayout(entities);

        // Step - Persist layout
        createOrUpdateArtifactPositions(document, artifact2position);

        // Step - Notify document subscribers that layout has been generated
        if (sendNotification) {
            this.serviceProvider
                .getNotificationService()
                .broadcastDocumentLayoutMessage(projectVersion, document.getDocumentId());
        }

        return artifact2position;
    }

    private void generateDefaultDocumentLayout() {
        Map<String, LayoutPosition> layout = generateLayout(this.projectEntities);
        createOrUpdateArtifactPositions(null, layout);
    }

    private List<Document> retrieveAffectedDocuments(List<ArtifactAppEntity> affectedArtifacts) {
        List<String> affectedDocumentIds = new ArrayList<>();
        List<Document> affectedDocuments = new ArrayList<>();
        affectedArtifacts.forEach(artifactAppEntity -> {
            for (String documentIdString : artifactAppEntity.getDocumentIds()) {
                if (!affectedDocumentIds.contains(documentIdString)) {
                    UUID documentId = UUID.fromString(documentIdString);
                    Optional<Document> documentOptional =
                        this.serviceProvider.getDocumentRepository().findById(documentId);
                    assert documentOptional.isPresent();
                    affectedDocuments.add(documentOptional.get());
                    affectedDocumentIds.add(documentIdString);
                }
            }
        });
        return affectedDocuments;
    }

    private void createOrUpdateArtifactPositions(Document document,
                                                 Map<String, LayoutPosition> layout) {
        // Step - Persist new layout
        for (Map.Entry<String, LayoutPosition> artifact2pos : layout.entrySet()) {
            createOrUpdateArtifactPosition(document, artifact2pos);
        }
    }

    private void createOrUpdateArtifactPosition(Document document,
                                                Map.Entry<String, LayoutPosition> artifact2pos) {
        // Step - Retrieve necessary entries for ArtifactPosition
        ArtifactAppEntity artifactAppEntity = this.projectEntities.getArtifactById(artifact2pos.getKey());
        LayoutPosition layoutPosition = artifact2pos.getValue();

        // Step - Create artifact position
        ArtifactPosition artifactPosition = this.serviceProvider
            .getArtifactPositionService()
            .createOrUpdateArtifactPosition(projectVersion, artifactAppEntity, layoutPosition, document);

        // Step - Save artifact position
        this.serviceProvider
            .getArtifactPositionRepository()
            .save(artifactPosition);
    }

    private Map<String, LayoutPosition> generateLayout(ProjectEntities entities) {
        List<ArtifactAppEntity> documentArtifacts = entities.getArtifacts();
        List<TraceAppEntity> documentTraces = entities.getTraces();
        return generateLayout(documentArtifacts, documentTraces);
    }

    private Map<String, LayoutPosition> generateLayout(List<ArtifactAppEntity> artifacts,
                                                       List<TraceAppEntity> traces) {
        // Step - Generate layout
        KlayLayoutGenerator layoutGenerator = new KlayLayoutGenerator(
            artifacts, traces);
        return layoutGenerator.layout();
    }
}
