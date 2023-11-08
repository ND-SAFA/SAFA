package edu.nd.crc.safa.test.features.memberships.crud;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.test.common.AbstractSharingTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
class TestProjectRetrievalWithSharingCommonRequests extends AbstractSharingTest {

    /**
     * Tests that a user is able to retrieve all the projects they own.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    void sharedProjectAppearsInGetProjects() throws Exception {
        // Step - Login as other user
        this.rootBuilder
            .authorize(a -> a.loginUser(Sharee.email, Sharee.password, true, this));

        // Step - Get projects for user who got shared with
        JSONArray projects = SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonArray();

        assertThat(projects.length())
            .as("Sharee has single project shared with them")
            .isEqualTo(1);

        String projectName = projects.getJSONObject(0).getString("name");
        assertThat(projectName)
            .as("Project shared is correct ")
            .isEqualTo(projectName);
    }
}
