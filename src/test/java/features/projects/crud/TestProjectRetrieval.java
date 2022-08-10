package features.projects.crud;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import features.base.ApplicationBaseTest;
import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
class TestProjectRetrieval extends ApplicationBaseTest {
    @Test
    void retrieveNoProjects() throws Exception {
        JSONArray response = SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonArray();
        assertThat(response.length()).isZero();
    }

    /**
     * Tests that a user is able to retrieve all the projects they own.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    void retrieveMultipleProjects() throws Exception {
        SafaUser otherUser = new SafaUser();
        otherUser.setEmail("doesNotExist@gmail.com");
        otherUser.setPassword("somePassword");
        this.safaUserRepository.save(otherUser);

        dbEntityBuilder
            .newProject("firstProject")
            .newProject("secondProject")
            .newProject("other project", otherUser);
        JSONArray response = SafaRequest.withRoute(AppRoutes.Projects.GET_PROJECTS).getWithJsonArray();
        assertThat(response.length()).isEqualTo(2);
    }

}
