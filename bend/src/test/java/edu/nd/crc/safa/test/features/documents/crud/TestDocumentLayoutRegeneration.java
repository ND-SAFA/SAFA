package edu.nd.crc.safa.test.features.documents.crud;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.junit.jupiter.api.Test;

/**
 * Test that editing an artifact will trigger layout regenerations in affected documents.
 */
class TestDocumentLayoutRegeneration extends ApplicationBaseTest {
    /**
     * The version of the layout to verify.
     */
    ProjectVersion projectVersion;
    /**
     * The project who layout this test verifies.
     */
    ProjectAppEntity project;

    @Test
    void testDocumentLayoutRegeneration() throws Exception {
        // Step - Create project
        this.projectVersion = this.creationService.createProjectWithNewVersion(projectName);

        // Step - Create small project
        createSmallProject();

        this.projectVersion = this.dbEntityBuilder.newVersionWithReturn(projectName);

        // Step - Create document
        createDocument();

        // Step - Modify default document
        addThirdDocument();

        // Step - Retrieve project
        this.project = retrievalService.getProjectAtVersion(projectVersion);

        // VP - Verify default document layout
        verifyProjectLayout();

        // VP - Verify document layout was regenerated
        verifyDocumentLayout();
    }

    private void verifyProjectLayout() {
        layoutTestService.verifyLayout(project.getLayout(), getProjectArtifactIds());
    }

    private void verifyDocumentLayout() {
        layoutTestService.verifyLayout(project.getDocuments().get(0).getLayout(), getDocumentArtifactIds());
    }

    private List<UUID> getProjectArtifactIds() {
        List<UUID> documentArtifactIds = getDocumentArtifactIds();
        documentArtifactIds.add(Constants.artifact3.getId());
        return documentArtifactIds;
    }

    private List<UUID> getDocumentArtifactIds() {
        return new ArrayList<>(List.of(
            Constants.artifact1.getId(),
            Constants.artifact2.getId()));
    }

    void createSmallProject() throws Exception {
        this.commitService.commit(
            CommitBuilder.withVersion(this.projectVersion)
                .withAddedArtifact(Constants.artifact1)
                .withAddedArtifact(Constants.artifact2)
                .withAddedTrace(Constants.traceAppEntity)
        );
    }

    void createDocument() throws Exception {
        DocumentAppEntity documentAppEntity = Constants.document;
        documentAppEntity.getArtifactIds().addAll(List.of(
            Constants.artifact1.getId(),
            Constants.artifact2.getId()));
        this.creationService.createOrUpdateDocument(projectVersion, documentAppEntity);
    }

    void addThirdDocument() throws Exception {
        this.commitService.commit(
            CommitBuilder
                .withVersion(this.projectVersion)
                .withAddedArtifact(Constants.artifact3)
        );
    }

    static class Constants {
        static final String type = "requirement";
        static final String a1name = "R0";
        static final String a2name = "R1";
        static final String a3name = "R2";
        static final String summary = "this is a summary";
        static final String body = "this is a body";
        static ArtifactAppEntity artifact1 = new ArtifactAppEntity(
            null,
            type,
            a1name,
            summary,
            body,
            new HashMap<>()
        );
        static ArtifactAppEntity artifact2 = new ArtifactAppEntity(
            null,
            type,
            a2name,
            summary,
            body,
            new HashMap()
        );
        static ArtifactAppEntity artifact3 = new ArtifactAppEntity(
            null,
            type,
            a3name,
            summary,
            body,
            new HashMap()
        );
        static TraceAppEntity traceAppEntity = new TraceAppEntity(
            null,
            a1name,
            null,
            a2name,
            null,
            ApprovalStatus.APPROVED,
            1,
            TraceType.MANUAL,
            true,
            null
        );
        static DocumentAppEntity document = new DocumentAppEntity(
            null,
            "document-name",
            "document-description",
            new ArrayList<>(),
            new HashMap<>()
        );
    }

}
