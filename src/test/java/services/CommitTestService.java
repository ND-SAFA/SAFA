package services;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;

/**
 * Responsible for providing utilities related to committing
 */
public class CommitTestService {
    public JSONObject commit(CommitBuilder commitBuilder) throws Exception {
        return commitWithStatus(commitBuilder, status().is2xxSuccessful());
    }

    private JSONObject commitWithStatus(CommitBuilder commitBuilder, ResultMatcher expectedStatus) throws Exception {
        ProjectVersion commitVersion = commitBuilder.get().getCommitVersion();
        return SafaRequest
            .withRoute(AppRoutes.Commits.COMMIT_CHANGE)
            .withVersion(commitVersion)
            .postWithJsonObject(commitBuilder.asJson(), expectedStatus);
    }
}
