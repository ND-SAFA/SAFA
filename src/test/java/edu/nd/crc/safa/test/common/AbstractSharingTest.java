package edu.nd.crc.safa.test.common;

import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.Getter;
import org.junit.jupiter.api.BeforeEach;

/**
 * Creates a project under the default user and shares with an external account, Sharee.
 */
public abstract class AbstractSharingTest extends ApplicationBaseTest implements IShareTest {

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
    /**
     * The user used to share resources with.
     */
    @Getter
    protected IUser sharee;

    @BeforeEach
    public void setupProject() throws Exception {
        setupTestResources();
    }

    protected void setupTestResources() throws Exception {
        // Step - Create project and initial version
        this.projectVersion = creationService.createProjectWithNewVersion(projectName);
        this.project = this.projectVersion.getProject();

        // Step - Create other user to share project with.
        this.sharee = this.authorizationService.createUser(Sharee.email, Sharee.password);
        String shareeToken = this.authorizationService.loginUser(Sharee.email, Sharee.password);

        this.authorizationService.logicDefaultUser();

        // Step - Share project with sharee
        creationService.shareProject(
            this.projectVersion.getProject(),
            Sharee.email,
            this.otherUserProjectRole);

        // Step - Subscribe Sharee to project  notifications
        notificationService.initializeUser(sharee, shareeToken);
        notificationService.subscribeToProject(sharee, project);
        notificationService.subscribeToVersion(sharee, projectVersion);
    }

    /**
     * @return {@link ProjectRole} of user to share project with.
     */
    protected ProjectRole getShareePermission() {
        return ProjectRole.VIEWER;
    }

    @Override
    public String getShareeEmail() {
        return Sharee.email;
    }

    @Override
    public String getShareePassword() {
        return Sharee.password;
    }

    /**
     * The account for which the project is shared with.
     */
    public static class Sharee {
        public static final String email = "otherUser@gmail.com";
        public static final String password = "otherUserPassword";
    }
}
