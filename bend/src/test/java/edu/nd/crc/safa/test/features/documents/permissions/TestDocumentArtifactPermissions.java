package edu.nd.crc.safa.test.features.documents.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestDocumentArtifactPermissions extends AbstractPermissionViolationTest {

    private Document document;
    private Artifact artifact;

    @BeforeEach
    public void testSetup() {
        String documentName = "document";
        String typeName = "type";
        String artifactName = "artifact";

        document =
            dbEntityBuilder
                .newDocument(projectName, documentName, "description")
                .getDocument(projectName, documentName);

        artifact =
            dbEntityBuilder
                .newType(projectName, typeName)
                .newArtifact(projectName, typeName, artifactName)
                .newDocumentArtifact(projectName, 0, documentName, artifactName)
                .getArtifact(projectName, artifactName);
    }

    @Test
    public void testAddToDocument() {
        test(
            () -> SafaRequest
                .withRoute(AppRoutes.DocumentArtifact.ADD_ARTIFACTS_TO_DOCUMENT)
                .withVersion(projectVersion)
                .withDocument(document)
                .postWithJsonObject(new JSONArray(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

    @Test
    public void testRemoveFromDocument() {
        test(
            () -> SafaRequest
                .withRoute(AppRoutes.DocumentArtifact.REMOVE_ARTIFACT_FROM_DOCUMENT)
                .withVersion(projectVersion)
                .withDocument(document)
                .withArtifactId(artifact.getArtifactId())
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }
}
