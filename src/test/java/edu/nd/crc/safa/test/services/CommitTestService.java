package edu.nd.crc.safa.test.services;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;

/**
 * Responsible for providing utilities related to committing
 */
public class CommitTestService {
    static ObjectMapper objectMapper = ObjectMapperConfig.create();

    public static ProjectCommitDefinition commit(CommitBuilder commitBuilder) {
        try {
            ProjectCommitDefinition commitRequest = commitBuilder.get();
            JSONObject commitJson = commitWithStatus(commitBuilder, status().is2xxSuccessful());
            ProjectCommitDefinition commitResponse = objectMapper.readValue(commitJson.toString(), ProjectCommitDefinition.class);

            for (ArtifactAppEntity artifact : commitResponse.getArtifactList(ModificationType.ADDED)) {
                commitRequest.getArtifact(ModificationType.ADDED, artifact.getName()).setId(artifact.getId());
            }

            return commitResponse;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static JSONObject commitWithStatus(CommitBuilder commitBuilder, ResultMatcher expectedStatus) {
        ProjectVersion commitVersion = commitBuilder.get().getCommitVersion();
        return SafaRequest
            .withRoute(AppRoutes.Commits.COMMIT_CHANGE)
            .withVersion(commitVersion)
            .postWithJsonObject(commitBuilder.asJson(), expectedStatus);
    }
}
