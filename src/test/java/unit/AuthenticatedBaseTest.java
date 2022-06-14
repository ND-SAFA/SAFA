package unit;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.StringCreator;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.json.JSONArray;
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

    public static final String currentUserEmail = "current-user@gmail.com";
    public static final String currentUserPassword = "r{QjR3<Ec2eZV@?";
    public static SafaUser currentUser;
    protected String token;

    @BeforeEach
    public void createData() throws Exception {
        token = null;
        this.safaUserRepository.deleteAll();
        currentUser = createUser(currentUserEmail, currentUserPassword);
        loginUser(currentUserEmail, currentUserPassword);
        this.dbEntityBuilder.setCurrentUser(currentUser);
    }

    public SafaUser createUser(String email, String password) throws Exception {
        SafaUser user = new SafaUser(email, password);
        sendPost(AppRoutes.Accounts.createNewUser, toJson(user), status().is2xxSuccessful(),
            false);
        return safaUserService.getUserFromUsername(email);
    }

    public void loginUser(String username, String password) throws Exception {
        this.loginUser(username, password, true);
    }

    public void loginUser(String email, String password, boolean setToken) throws Exception {
        loginUser(email, password, status().is2xxSuccessful(), setToken);
    }

    public void loginUser(String email, String password, ResultMatcher test) throws Exception {
        this.loginUser(email, password, test, true);
    }

    public void loginUser(String email, String password,
                          ResultMatcher test,
                          boolean setTokenIfSuccess) throws Exception {
        JSONObject user = new JSONObject();
        user.put("email", email);
        user.put("password", password);
        JSONObject response = sendRequest(addJsonBody(post(AppRoutes.Accounts.loginLink), user),
            test);
        if (setTokenIfSuccess) {
            this.token = response.getString("token");
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
        String url = RouteBuilder
            .withRoute(AppRoutes.Projects.Membership.deleteProjectMembership)
            .withProjectMembership(projectMembershipOptional.get())
            .get();
        sendDelete(url, status().isNoContent());
    }

    public void assertTokenExists() throws SafaError {
        if (this.token == null || this.token.equals("")) {
            throw new SafaError("Authorization token not set.");
        }
    }

    /**
     * HTTP Routes
     */

    public void sendDelete(String routeName) throws Exception {
        sendDelete(routeName, status().isNoContent());
    }

    public JSONObject sendGet(String routeName) throws Exception {
        return sendGet(routeName, status().isOk());
    }

    public JSONObject sendGet(String routeName,
                              ResultMatcher test) throws Exception {
        assertTokenExists();
        return sendRequest(get(routeName), test, this.token);
    }

    public JSONArray sendGetWithArrayResponse(String routeName,
                                              ResultMatcher test) throws Exception {
        assertTokenExists();
        return sendRequestWithCreator(get(routeName), test, this.token, EntityBaseTest::arrayCreator);
    }

    public JSONObject sendPost(String routeName, Object body) throws Exception {
        return sendPost(routeName, body, status().is2xxSuccessful());
    }

    public JSONObject sendPost(String routeName,
                               Object body,
                               ResultMatcher test) throws Exception {
        return sendPost(routeName, body, test, true, EntityBaseTest::jsonCreator);
    }

    public JSONArray sendPostWithArrayResponse(String routeName,
                                               Object body,
                                               ResultMatcher test) throws Exception {
        return sendPost(routeName, body, test, true, EntityBaseTest::arrayCreator);
    }

    public void sendPost(String routeName,
                         Object body,
                         ResultMatcher test,
                         boolean assertToken) throws Exception {
        sendPost(routeName, body, test, assertToken, JSONObject::new);
    }

    public <T> T sendPost(String routeName,
                          Object body,
                          ResultMatcher test,
                          boolean assertToken,
                          StringCreator<T> stringCreator) throws Exception {
        MockHttpServletRequestBuilder request;
        if (assertToken) {
            assertTokenExists();
            request = addJsonBody(post(routeName), body);
            return sendRequestWithCreator(request, test, this.token, stringCreator);
        } else {
            //TODO: Create better way to omit authentication token
            request = addJsonBody(post(routeName), body);
            return sendRequestWithCreator(request, test, "", stringCreator);
        }
    }

    public void sendDelete(String routeName,
                           ResultMatcher test) throws Exception {
        assertTokenExists();
        sendRequest(delete(routeName), test, this.token);
    }
}
