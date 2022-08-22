package features.memberships.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.HashMap;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;

import builders.CommitBuilder;
import org.json.JSONObject;

/**
 * Responsible for verifying that violating a permission returns a 403 response.
 */
public class TestViewPermissionViolation extends AbstractPermissionViolationTest {

    @Override
    protected JSONObject performViolatingAction() throws Exception {
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(Constants.artifact); // attempt to edit project
        return commitService.commitWithStatus(commitBuilder, status().is4xxClientError());
    }

    @Override
    protected ProjectRole getExpectedRole() {
        return ProjectRole.EDITOR;
    }

    static class Constants {
        private static final String type = "requirement";
        private static final String name = "R0";
        private static final String summary = "summary";
        private static final String body = "body";
        private static final DocumentType documentType = DocumentType.ARTIFACT_TREE;
        static final ArtifactAppEntity artifact = new ArtifactAppEntity(
            "",
            type,
            name,
            summary,
            body,
            documentType,
            new HashMap<>()
        );
    }
}
