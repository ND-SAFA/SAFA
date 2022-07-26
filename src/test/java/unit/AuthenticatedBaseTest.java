package unit;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.json.JSONObject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.test.web.servlet.ResultMatcher;

/**
 * Wraps each test with a test harness for creating a user account and logging in before each test.
 * If a certain test needs to exclude this harness one needs to create a test rule that excludes the
 * pre-test setup.
 */
public abstract class AuthenticatedBaseTest extends EntityBaseTest {

    public static final String defaultUser = "root-test-user@gmail.com";
    public static final String defaultUserPassword = "r{QjR3<Ec2eZV@?";
    public static SafaUser currentUser;
    protected String token;

    @BeforeEach
    public void createData() throws Exception {
        token = null;
        this.safaUserRepository.deleteAll();
        SafaRequest.setMockMvc(mockMvc);
        this.defaultLogin();
        this.dbEntityBuilder.setCurrentUser(currentUser);
    }

    @AfterEach
    public void clearAuthentication() {
        SafaRequest.clearAuthorizationToken();
    }

    public void defaultLogin() throws Exception {
        createUser(defaultUser, defaultUserPassword);
        loginUser(defaultUser, defaultUserPassword);
        currentUser = safaUserService.getUserFromUsername(defaultUser);
    }

    public void createUser(String email, String password) throws Exception {
        SafaUser user = new SafaUser(email, password);
        SafaRequest
            .withRoute(AppRoutes.Accounts.createNewUser)
            .postWithJsonObject(user);
    }

    public void loginUser(String email, String password) throws Exception {
        this.loginUser(email, password, true);
    }

    public void loginUser(String email, String password, boolean setToken) throws Exception {
        loginUser(email, password, status().is2xxSuccessful(), setToken);
    }

    public void loginUser(String email, String password, ResultMatcher test) throws Exception {
        this.loginUser(email, password, test, true);
    }

    public void loginUser(String email, String password, ResultMatcher test, boolean setToken) throws Exception {
        JSONObject user = new JSONObject();
        user.put("email", email);
        user.put("password", password);
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Accounts.loginLink)
            .postWithJsonObject(user, test);
        if (setToken) {
            this.token = response.getString("token");
            SafaRequest.setAuthorizationToken(this.token);
        }
    }

    public void removeMemberFromProject(Project project, String username) throws Exception {
        Optional<SafaUser> safaUserOptional = this.safaUserRepository.findByEmail(username);
        if (safaUserOptional.isEmpty()) {
            throw new SafaError("Could not find user with name: " + username);
        }
        Optional<ProjectMembership> projectMembershipOptional = this.projectMembershipRepository.findByProjectAndMember(
            project,
            safaUserOptional.get());
        if (projectMembershipOptional.isEmpty()) {
            String errorMessage = String.format("Could not find membership between {%s} and {%s}.",
                username,
                project.getName());
            throw new SafaError(errorMessage);

        }
        SafaRequest
            .withRoute(AppRoutes.Projects.Membership.deleteProjectMembership)
            .withProjectMembership(projectMembershipOptional.get())
            .deleteWithJsonObject();
    }
}
