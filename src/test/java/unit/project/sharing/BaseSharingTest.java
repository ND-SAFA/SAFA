package unit.project.sharing;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.accounts.SafaUser;

import org.junit.jupiter.api.BeforeEach;
import unit.ApplicationBaseTest;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class BaseSharingTest extends ApplicationBaseTest {

    protected final String otherUserEmail = "doesNotExist@gmail.com";
    protected final String otherUserPassword = "somePassword";
    protected SafaUser otherUser = null;

    @BeforeEach
    public void clearData() {
        this.otherUser = null;
    }

    protected Project createAndShareProject(String projectName) throws Exception {
        // Step - Create other user to share project with.
        SafaUser otherUser = new SafaUser();
        otherUser.setEmail(this.otherUserEmail);
        otherUser.setPassword(this.otherUserPassword);
        this.otherUser = otherUser;
        this.safaUserRepository.save(otherUser);

        // Step - Create project to share
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);

        // Step - Share project
        shareProject(project, otherUser.getEmail(), ProjectRole.VIEWER, status().is2xxSuccessful());

        return project;
    }
}
