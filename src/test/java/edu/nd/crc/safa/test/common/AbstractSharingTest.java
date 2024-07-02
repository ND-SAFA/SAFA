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

        // Step
        this.rootBuilder
            .store(s -> s.save("project", this.project).save("user", getCurrentUser()))
            .and("Login root user.")
            .authorize((s, a) -> a.loginDefaultUser(this))
            .and("Root User: Subscribe to project")
            .notifications((s, n) -> n
                .initializeUser(getCurrentUser(), getToken(getCurrentUser()))
                .subscribeToProject(getCurrentUser(), s.getProject("project")));
        
        // TODO https://www.notion.so/nd-safa/BE-Tests-Occasionally-Fail-9500d5c1f1d84a76acf429ee3653bb86
        /*
            .and()
            .actions(a -> a.verifyActiveMembers(getCurrentUser(), List.of(currentUserName)));
         */

        this.sharee = this.rootBuilder
            .authorize((s, a) -> a
                .createUser(Sharee.email, Sharee.password)
                .save("sharee-user").get()).get();

        this.rootBuilder.authorize(a -> a
                .loginUser(Sharee.email, Sharee.password, this)
                .save("shareeToken"))
            .and()
            .authorize((s, a) -> a
                .loginDefaultUser(this))
            .and()
            .request((s, r) -> r.project().addUserToProject(s.getProject("project"), Sharee.email,
                this.otherUserProjectRole, getCurrentUser()));

        // TODO https://www.notion.so/nd-safa/BE-Tests-Occasionally-Fail-9500d5c1f1d84a76acf429ee3653bb86
        /*
            .and()
            .notifications((s, n) -> n
                .initializeUser(s.getIUser("sharee-user"), s.getString("shareeToken"))
                .subscribeToProject(s.getIUser("sharee-user"), s.getProject("project"))
                .subscribeToVersion(s.getIUser("sharee-user"), projectVersion)
                .getEntityMessage(s.getIUser("sharee-user")))
            .save("sharee-project-message")
            .and()
            .verify((s, v) -> v
                .notifications(n -> n
                    .verifyMemberNotification(s.getMessage("sharee-project-message"),
                        List.of(currentUserName, Sharee.email))));
         */
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
