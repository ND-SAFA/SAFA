package edu.nd.crc.safa.features.layout.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.flatfiles.entities.common.ProjectEntityMaps;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.layout.generator.KlayLayoutGenerator;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

/**
 * Responsible for managing common layout on a project
 */
public class ProjectLayout {

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
    private final ProjectEntityMaps projectEntityMaps;

    public ProjectLayout(ProjectAppEntity projectAppEntity, ServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
        this.projectEntityMaps = new ProjectEntityMaps(projectAppEntity);
        this.project = this.serviceProvider
            .getProjectRepository()
            .findByProjectId(UUID.fromString(projectAppEntity.projectId));
        this.projectVersion = projectAppEntity.projectVersion;
    }

    /**
     * For each document,
     * - Generates layout according to its entities
     * - Persists layout for document
     * - Notify all users of project that all layouts have been updated
     */
    public void createLayoutForAllDocuments() {
        List<Document> projectDocuments = this.serviceProvider
            .getDocumentRepository()
            .findByProject(this.project);
        createLayoutForDocuments(projectDocuments, false);
        //TODO: Send update to update all layouts
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
    public void updateLayoutWithChanges(ProjectCommit projectCommit) {
        // Step - Extract artifact causing stale layouts
        List<ArtifactAppEntity> affectedArtifacts = new ArrayList<>();
        affectedArtifacts.addAll(projectCommit.getArtifacts().getAdded());
        affectedArtifacts.addAll(projectCommit.getArtifacts().getRemoved());

        // Step - Generate affected documents
        List<Document> affectedDocuments = retrieveAffectedDocuments(affectedArtifacts);

        // Step - Generate layout for those documents
        createLayoutForDocuments(affectedDocuments, true);
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

    private void createLayoutForDocuments(List<Document> documents, boolean sendNotification) {
        for (Document document : documents) {
            // Step - Get entities in document
            ProjectEntityMaps.Entities entities = this.projectEntityMaps.getEntitiesInDocument(document);
            List<ArtifactAppEntity> documentArtifacts = entities.getArtifacts();
            List<TraceAppEntity> documentTraces = entities.getTraces();

            // Step - Generate layout
            KlayLayoutGenerator layoutGenerator = new KlayLayoutGenerator(
                documentArtifacts, documentTraces);
            Map<String, LayoutPosition> artifact2position = layoutGenerator.layout();

            // Step - Persist new layout
            for (Map.Entry<String, LayoutPosition> artifact2pos : artifact2position.entrySet()) {
                createOrUpdateArtifactPosition(this.projectVersion, document, artifact2pos);
            }

            if (sendNotification) {
                // TODO: Send notification
            }
        }
    }

    private void createOrUpdateArtifactPosition(ProjectVersion projectVersion,
                                                Document document,
                                                Map.Entry<String, LayoutPosition> artifact2pos) {
        // Step - Retrieve necessary entries for ArtifactPosition
        ArtifactAppEntity artifactAppEntity = this.projectEntityMaps.getArtifactById(artifact2pos.getKey());
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
}
