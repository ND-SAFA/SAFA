package unit.project;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class TestProjectRetrieval extends ApplicationBaseTest {
    @Test
    public void retrieveNoProjects() throws Exception {
        JSONArray response = sendGetWithArrayResponse(AppRoutes.Projects.getProjects, status().isOk());
        assertThat(response.length()).isEqualTo(0);
    }

    /**
     * Tests that a user is able to retrieve all the projects they own.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    public void retrieveMultipleProjects() throws Exception {
        SafaUser otherUser = new SafaUser();
        otherUser.setEmail("doesNotExist@gmail.com");
        otherUser.setPassword("somePassword");
        this.safaUserRepository.save(otherUser);

        dbEntityBuilder
            .newProject("firstProject")
            .newProject("secondProject")
            .newProject("other project", otherUser);
        JSONArray response = sendGetWithArrayResponse(AppRoutes.Projects.getProjects, status().isOk());
        assertThat(response.length()).isEqualTo(2);
    }

}
