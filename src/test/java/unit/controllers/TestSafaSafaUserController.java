package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.ResultMatcher;
import unit.EntityBaseTest;

/**
 * Tests that user is able to:
 * 1. Create an account.
 * 2. Log into an existing account
 * 3. User is not allowed without credentials.
 */
public class TestSafaSafaUserController extends EntityBaseTest {

    @Autowired
    SafaUserRepository safaUserRepository;

    @Test
    public void createAccount() throws Exception {
        String email = "vhsalbertorodriguez@gmail.com";
        String password = "r{QjR3<Ec2eZV@?";

        createUser(email, password);

        SafaUser user = safaUserRepository.findByEmail(email);
        assertThat(user.getEmail()).isEqualTo(email);
    }

    @Test
    public void correctLoginAttempt() throws Exception {
        String email = "abc123@gmail.com";
        String password = "r{QjR3<Ec2eZV@?";
        createUser(email, password);
        loginUser(email, password, status().isOk());
    }

    @Test
    public void wrongLoginAttempt() throws Exception {
        String email = "abc123@gmail.com";
        String password = "r{QjR3<Ec2eZV@?";
        loginUser(email, password, status().is4xxClientError());
    }

    private JSONObject createUser(String email, String password) throws Exception {
        JSONObject payload = new JSONObject();
        payload.put("email", email);
        payload.put("password", password);
        return sendPost("/sign-up", payload, status().is2xxSuccessful());
    }

    private JSONObject loginUser(String email, String password, ResultMatcher test) throws Exception {
        return sendRequest(post("/login")
                .contentType(MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                .param("email", email)
                .param("password", password),
            test);
    }
}
