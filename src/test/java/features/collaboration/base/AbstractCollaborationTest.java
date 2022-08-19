package features.collaboration.base;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.junit.jupiter.api.BeforeEach;
import features.base.ApplicationBaseTest;

/**
 * Tests that projects defined in database are to be retrieved by user.
 */
public abstract class AbstractCollaborationTest extends ApplicationBaseTest {

    protected final String otherUserEmail = "otherUser@gmail.com";
    protected final String otherUserPassword = "otherUserPassword";
    protected SafaUser otherUser = null;

    @BeforeEach
    public void clearData() {
        this.otherUser = null;
    }

    protected Project createAndShareProject(String projectName) throws Exception {
        return createAndShareProject(projectName, ProjectRole.VIEWER, true);
    }

    protected Project createAndShareProject(String projectName,
                                            ProjectRole projectRole,
                                            boolean currentUserAsOwner) throws Exception {
        // Step - Create other user to share project with.
        SafaUser otherUser = new SafaUser();
        otherUser.setEmail(this.otherUserEmail);
        otherUser.setPassword(this.otherUserPassword);
        this.otherUser = otherUser;
        this.safaUserRepository.save(otherUser);

        // Step - Create project to share
        SafaUser owner = currentUserAsOwner ? currentUser : otherUser;
        Project project = dbEntityBuilder
            .newProject(projectName, owner)
            .getProject(projectName);

        // Step - Share project
        creationTestService.shareProject(project, otherUser.getEmail(), ProjectRole.VIEWER, status().is2xxSuccessful());

        return project;
    }
}
