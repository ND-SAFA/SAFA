package services;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;
import requests.SafaRequest;

/**
 * Responsible for providing utilities related to committing
 */
public class CommitTestService {
    ObjectMapper objectMapper = new ObjectMapper();

    public ProjectCommit commit(CommitBuilder commitBuilder) throws Exception {
        ProjectCommit commitRequest = commitBuilder.get();
        JSONObject commitJson = commitWithStatus(commitBuilder, status().is2xxSuccessful());
        ProjectCommit commitResponse = objectMapper.readValue(commitJson.toString(), ProjectCommit.class);

        for (ArtifactAppEntity artifact : commitResponse.getArtifactList(ModificationType.ADDED)) {
            commitRequest.getArtifact(ModificationType.ADDED, artifact.getName()).setId(artifact.getId());
        }

        return commitResponse;
    }

    public JSONObject commitWithStatus(CommitBuilder commitBuilder, ResultMatcher expectedStatus) throws Exception {
        ProjectVersion commitVersion = commitBuilder.get().getCommitVersion();
        return SafaRequest
            .withRoute(AppRoutes.Commits.COMMIT_CHANGE)
            .withVersion(commitVersion)
            .postWithJsonObject(commitBuilder.asJson(), expectedStatus);
    }
}
