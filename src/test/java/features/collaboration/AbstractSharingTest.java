package features.collaboration;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.BeforeEach;

/**
 * Creates a project under the default user and shares with an external account, Sharee.
 */
public abstract class AbstractSharingTest extends ApplicationBaseTest {

    /**
     * Project role of sharee.
     */
    protected final ProjectRole otherUserProjectRole = getShareePermission();
    /**
     * The project version shared with sharee.
     */
    protected ProjectVersion projectVersion;
    /**
     * Project shared with sharee.
     */
    protected Project project;

    @BeforeEach
    public void createShareeAccountAndShareProject() throws Exception {
        // Step - Create project and initial version
        this.projectVersion = creationTestService.createProjectWithNewVersion(projectName);
        this.project = this.projectVersion.getProject();

        // Step - Create other user to share project with.
        this.authorizationTestService.createUser(Sharee.email, Sharee.password);

        // Step - Share project with sharee
        creationTestService.shareProject(
            this.projectVersion.getProject(),
            Sharee.email,
            this.otherUserProjectRole);
    }

    /**
     * @return {@link ProjectRole} of user to share project with.
     */
    protected ProjectRole getShareePermission() {
        return ProjectRole.VIEWER;
    }

    /**
     * The account for which the project is shared with.
     */
    protected static class Sharee {
        public static final String email = "otherUser@gmail.com";
        public static final String password = "otherUserPassword";
    }
}
