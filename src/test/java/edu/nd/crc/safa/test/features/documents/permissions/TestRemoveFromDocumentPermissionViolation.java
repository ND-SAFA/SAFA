package edu.nd.crc.safa.test.features.documents.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;

public class TestRemoveFromDocumentPermissionViolation extends AbstractPermissionViolationTest {

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

    @Override
    protected JSONObject performViolatingAction() {
        return SafaRequest
            .withRoute(AppRoutes.DocumentArtifact.REMOVE_ARTIFACT_FROM_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(document)
            .withArtifactId(artifact.getArtifactId())
            .deleteWithJsonObject(status().is4xxClientError());
    }

    @Override
    protected Set<Permission> getExpectedPermissions() {
        return Set.of(ProjectPermission.EDIT_DATA);
    }
}
