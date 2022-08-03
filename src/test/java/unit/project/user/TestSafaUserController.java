package unit.project.user;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;

import org.json.JSONArray;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that user is able to:
 * 1. Create an account.
 * 2. Log into an existing account
 * 3. User is not allowed without credentials.
 */
class TestSafaUserController extends ApplicationBaseTest {
    String testEmail = "abc123@gmail.com";
    String testPassword = "r{QjR3<Ec2eZV@?";

    @Autowired
    SafaUserRepository safaUserRepository;

    @BeforeEach
    public void clearUsers() {
        // Base controller (AuthenticatedBaseTest) clears all accounts before each test.
        SafaRequest.clearAuthorizationToken();
    }

    @Test
    void testCanCreateAccount() throws Exception {
        createUser(testEmail, testPassword);
        Optional<SafaUser> userQuery = safaUserRepository.findByEmail(testEmail);
        assertThat(userQuery).isPresent();

        SafaUser user = userQuery.get();
        assertThat(user.getEmail()).isEqualTo(testEmail);
    }

    @Test
    void testTokenIsSet() throws Exception {
        createUser(testEmail, testPassword);
        loginUser(testEmail, testPassword, status().isOk());
        assertThat(SafaRequest.getAuthorizationToken()).isNotNull();
    }

    @Test
    void testThatUserWasCreated() throws Exception {
        createUser(testEmail, testPassword);
        loginUser(testEmail, testPassword, status().isOk());

        // VP - Verify that user is able to be authenticated and no projects are assigned to it.
        JSONArray response = new SafaRequest(AppRoutes.Projects.GET_PROJECTS).getWithJsonArray();
        assertThat(response.length()).isZero();
    }

    @Test
    void testInvalidRequestMissingCredentials() throws Exception {
        SafaRequest.clearAuthorizationToken();
        SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonObject(status().isForbidden());
    }

    @Test
    void testForbiddenIsUserNotAuthorized() throws Exception {
        loginUser(testEmail, testPassword, status().is4xxClientError(), false);
    }
}
