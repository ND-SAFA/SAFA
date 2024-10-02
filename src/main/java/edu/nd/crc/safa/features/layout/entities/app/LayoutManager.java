package edu.nd.crc.safa.features.layout.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.AbstractProjectCommit;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.layout.generator.KlayLayoutGenerator;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
                         ProjectVersion projectVersion,
                         SafaUser user) {
        //TODO: Remove use dep
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
            .forEach(this::generateDocumentLayout);
    }

    /**
     * 1. Generates list of affected documents
     * 2. For each document:
     * - generate new layout
     * - persist layout
     * - notify users of document that new layout exists
     *
     * @param projectCommitDefinition The changes to the artifact tree to calculate layout changes.
     */
    public void generateLayoutUpdates(AbstractProjectCommit projectCommitDefinition) {
        // Step - Extract artifact causing stale layouts
        List<ArtifactAppEntity> affectedArtifacts = new ArrayList<>();
        affectedArtifacts.addAll(projectCommitDefinition.getArtifacts().getAdded());
        affectedArtifacts.addAll(projectCommitDefinition.getArtifacts().getRemoved());

        // Step - Generate affected documents
        List<Document> affectedDocuments = retrieveAffectedDocuments(affectedArtifacts);

        // Step - Generate layout for those documents
        for (Document affectedDocument : affectedDocuments) {
            generateDocumentLayout(affectedDocument);
        }

        // Step - Generate layout for default document
        generateDefaultDocumentLayout();
    }

    /**
     * Creates layout for given document
     *
     * @param document Document whose layout will be generated.
     * @return Map of artifact id to their layout position.
     */
    public Map<UUID, LayoutPosition> generateDocumentLayout(Document document) {
        // Step - Get entities in document
        ProjectEntities entities = this.projectEntities.getEntitiesInDocument(document);

        // Step - Generate layout
        Map<UUID, LayoutPosition> artifact2position = generateLayout(entities);

        // Step - Persist layout
        createOrUpdateArtifactPositions(document, artifact2position);

        return artifact2position;
    }

    /**
     * Generates the layout for the default document.
     *
     * @return Map of artifact Id to its position in default document.
     */
    public Map<UUID, LayoutPosition> generateDefaultDocumentLayout() {
        Map<UUID, LayoutPosition> layout = generateLayout(this.projectEntities);
        createOrUpdateArtifactPositions(null, layout);
        return layout;
    }

    private List<Document> retrieveAffectedDocuments(List<ArtifactAppEntity> affectedArtifacts) {
        List<UUID> affectedDocumentIds = new ArrayList<>();
        List<Document> affectedDocuments = new ArrayList<>();
        affectedArtifacts.forEach(artifactAppEntity -> {
            for (UUID documentId : artifactAppEntity.getDocumentIds()) {
                if (!affectedDocumentIds.contains(documentId)) {
                    Optional<Document> documentOptional =
                        this.serviceProvider.getDocumentRepository().findById(documentId);
                    assert documentOptional.isPresent();
                    affectedDocuments.add(documentOptional.get());
                    affectedDocumentIds.add(documentId);
                }
            }
        });
        return affectedDocuments;
    }

    private void createOrUpdateArtifactPositions(Document document,
                                                 Map<UUID, LayoutPosition> layout) {
        // Step - Persist new layout
        for (Map.Entry<UUID, LayoutPosition> artifact2pos : layout.entrySet()) {
            createOrUpdateArtifactPosition(document, artifact2pos);
        }
    }

    private void createOrUpdateArtifactPosition(Document document,
                                                Map.Entry<UUID, LayoutPosition> artifact2pos) {
        // Step - Retrieve necessary entries for ArtifactPosition
        UUID artifactId = artifact2pos.getKey();
        ArtifactAppEntity artifactAppEntity = this.projectEntities.getArtifactById(artifactId);
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

    private Map<UUID, LayoutPosition> generateLayout(ProjectEntities entities) {
        List<ArtifactAppEntity> documentArtifacts = entities.getArtifacts();
        List<TraceAppEntity> documentTraces = entities.getTraces();
        return generateLayout(documentArtifacts, documentTraces);
    }

    private Map<UUID, LayoutPosition> generateLayout(List<ArtifactAppEntity> artifacts,
                                                     List<TraceAppEntity> traces) {
        // Step - Generate layout
        KlayLayoutGenerator layoutGenerator = new KlayLayoutGenerator(
            artifacts, traces);
        return layoutGenerator.layout();
    }
}
