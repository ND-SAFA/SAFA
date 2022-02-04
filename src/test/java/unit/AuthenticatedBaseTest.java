package unit;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

/**
 * Wraps each test with a test harness for creating a user account and logging in before each test.
 * If a certain test needs to exclude this harness one needs to create a test rule that excludes the
 * pre-test setup.
 */
public class AuthenticatedBaseTest extends EntityBaseTest {

    public static final String localUsername = "root-test-user@gmail.com";
    public static final String localPassword = "r{QjR3<Ec2eZV@?";
    public static SafaUser currentUser;
    protected String token;

    @BeforeEach
    public void createData() throws Exception {
        token = null;
        this.safaUserRepository.deleteAll();
        this.defaultLogin();
        this.dbEntityBuilder.setCurrentUser(currentUser);
    }

    public void defaultLogin() throws Exception {
        createUser(localUsername, localPassword);
        loginUser(localUsername, localPassword);
        currentUser = safaUserService.getUserFromUsername(localUsername);
    }

    public JSONObject sendGet(String routeName,
                              ResultMatcher test) throws Exception {
        assertTokenExists();
        return sendRequest(get(routeName), test, this.token);
    }

    public JSONObject sendPost(String routeName,
                               JSONObject body,
                               ResultMatcher test) throws Exception {
        return sendPost(routeName, body, test, true);
    }

    public JSONObject sendPost(String routeName,
                               JSONObject body,
                               ResultMatcher test,
                               boolean assertToken) throws Exception {
        MockHttpServletRequestBuilder request;
        if (assertToken) {
            assertTokenExists();
            request = addJsonBody(post(routeName), body);
            return sendRequest(request, test, this.token);
        } else {
            request = addJsonBody(post(routeName), body);
            return sendRequest(request, test);
        }
    }

    public JSONObject sendPut(String routeName,
                              JSONObject body,
                              ResultMatcher test) throws Exception {
        assertTokenExists();
        MockHttpServletRequestBuilder request = addJsonBody(put(routeName), body);
        return sendRequest(request, test, this.token);
    }

    public void sendDelete(String routeName,
                           ResultMatcher test) throws Exception {
        assertTokenExists();
        sendRequest(delete(routeName), test, this.token);
    }

    public void assertTokenExists() throws SafaError {
        if (this.token == null || this.token.equals("")) {
            throw new SafaError("Authorization token not set.");
        }
    }

    /**
     * Sends a Http request to the create account endpoint with given username and password.
     *
     * @param email    The id for the account.
     * @param password The password associated with account created.
     * @return The response object of the creation endpoint.
     * @throws Exception Throws exception if problems occurs with Http request.
     */
    public JSONObject createUser(String email, String password) throws Exception {
        SafaUser user = new SafaUser(email, password);
        return sendPost(AppRoutes.Accounts.createNewUser, toJson(user), status().is2xxSuccessful(), false);
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
        JSONObject response = sendRequest(addJsonBody(post(AppRoutes.Accounts.loginLink), user), test);
        if (setToken) {
            this.token = response.getString("token");
        }
    }

    public void removeMemberFromProject(Project project, String username) throws Exception {
        Optional<SafaUser> safaUser = this.safaUserRepository.findByEmail(username);
        Optional<ProjectMembership> query = this.projectMembershipRepository.findByProjectAndMember(project,
            safaUser.get());
        String url = RouteBuilder
            .withRoute(AppRoutes.Projects.deleteProjectMembership)
            .withProjectMembership(query.get())
            .get();
        sendDelete(url, status().isNoContent());
    }
}
