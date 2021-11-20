package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;

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
        createUser(email, password);
        SafaUser user = safaUserRepository.findByEmail(email);
        assertThat(user.getEmail()).isEqualTo(email);
    }

    @Test
    public void correctLoginAttempt() throws Exception {
        createUser(email, password);
        loginUser(email, password, status().isOk());
        assertThat(this.token).isNotNull();
    }

    @Test
    public void validResourceRequest() throws Exception {
        String email = "abc123@gmail.com";
        String password = "r{QjR3<Ec2eZV@?";
        createUser(email, password);
        loginUser(email, password, status().isOk());
        sendGet(Routes.projects, status().is2xxSuccessful());
    }

    @Test
    public void invalidResourceRequest() throws Exception {
        sendRequest(get(Routes.projects), status().is4xxClientError());
    }

    @Test
    public void wrongLoginAttempt() {
        assertThrows(JSONException.class, () -> {
            loginUser(email, password, status().is4xxClientError());
        });
    }
}
