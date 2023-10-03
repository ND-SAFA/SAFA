package edu.nd.crc.safa.test.features.projects.crud;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
class TestProjectRetrievalCommonRequests extends ApplicationBaseTest {
    @Test
    void retrieveNoProjects() throws Exception {
        JSONArray response = SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonArray();
        assertThat(response.length()).isZero(); // sample project
    }

    /**
     * Tests that a user is able to retrieve all the projects they own.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    void retrieveMultipleProjects() throws Exception {
        SafaUser otherUser = safaUserService.createUser("doesNotExist@gmail.com", "somePassword");

        dbEntityBuilder
            .newProject("firstProject")
            .newProject("secondProject")
            .newProject("other project", otherUser);
        JSONArray response = SafaRequest.withRoute(AppRoutes.Projects.GET_PROJECTS).getWithJsonArray();
        assertThat(response.length()).isEqualTo(2); // firstProject, secondProject, and default sample project.
    }

}
