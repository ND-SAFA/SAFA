package edu.nd.crc.safa.test.features.memberships.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.HashMap;
import java.util.Set;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.junit.jupiter.api.Test;

/**
 * Responsible for verifying that violating a permission returns a 403 response.
 */
public class TestProjectEditDataPermissionViolation extends AbstractPermissionViolationTest {

    @Test
    public void testEditProjectData() {
        test(() -> {
            CommitBuilder commitBuilder = CommitBuilder
                .withVersion(projectVersion)
                .withAddedArtifact(Constants.artifact); // attempt to edit project
            return commitService.commitWithStatus(commitBuilder, status().is4xxClientError());
        }, Set.of(ProjectPermission.EDIT_DATA));
    }

    static class Constants {
        private static final String type = "requirement";
        private static final String name = "R0";
        private static final String summary = "summary";
        private static final String body = "body";
        static final ArtifactAppEntity artifact = new ArtifactAppEntity(
            null,
            type,
            name,
            summary,
            body,
            new HashMap<>()
        );
    }
}
