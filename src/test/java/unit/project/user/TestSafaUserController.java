package unit.project.user;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.accounts.SafaUser;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;
import org.json.JSONException;
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
public class TestSafaUserController extends ApplicationBaseTest {

    @Autowired
    SafaUserRepository safaUserRepository;

    @BeforeEach
    public void clearUsers() {
        this.safaUserRepository.deleteAll();
    }

    @Test
    public void createAccount() throws Exception {
        createUser(currentUsername, localPassword);
        Optional<SafaUser> userQuery = safaUserRepository.findByEmail(currentUsername);
        assertThat(userQuery.isPresent()).isTrue();

        SafaUser user = userQuery.get();
        assertThat(user.getEmail()).isEqualTo(currentUsername);
    }

    @Test
    public void correctLoginAttempt() throws Exception {
        createUser(currentUsername, localPassword);
        loginUser(currentUsername, localPassword, status().isOk());
        assertThat(this.token).isNotNull();
    }

    @Test
    public void validResourceRequest() throws Exception {
        String email = "abc123@gmail.com";
        String password = "r{QjR3<Ec2eZV@?";
        createUser(email, password);
        loginUser(email, password, status().isOk());
        sendGetWithArrayResponse(AppRoutes.Projects.getProjects, status().is2xxSuccessful());
    }

    @Test
    public void invalidResourceRequest() throws Exception {
        sendRequest(get(AppRoutes.Projects.getProjects), status().is4xxClientError());
    }

    @Test
    public void wrongLoginAttempt() {
        assertThrows(JSONException.class, () -> {
            loginUser(currentUsername, localPassword, status().is4xxClientError());
        });
    }

    @Test
    public void invalidPasswordChangeAttempt() throws Exception {
        String invalidOldPassword = (String) localPassword.subSequence(0, localPassword.length() / 2);

        createUser(currentUsername, localPassword);
        loginUser(currentUsername, localPassword);
        changePassword(invalidOldPassword, localPassword, status().is4xxClientError());
    }

    @Test
    public void anotherInvalidPasswordChangeAttempt() throws Exception {
        createUser(currentUsername, localPassword);
        loginUser(currentUsername, localPassword);
        changePassword(localPassword, localPassword, status().is4xxClientError());
    }

    @Test
    public void validPasswordChangeAttempt() throws Exception {
        String validNewPassword = (String) localPassword.subSequence(0, localPassword.length() / 2);

        createUser(currentUsername, localPassword);
        loginUser(currentUsername, localPassword);
        changePassword(localPassword, validNewPassword, status().is2xxSuccessful());
    }
}
