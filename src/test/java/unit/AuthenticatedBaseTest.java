package unit;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

public class AuthenticatedBaseTest extends EntityBaseTest {

    public static final String email = "abc123@gmail.com";
    public static final String password = "r{QjR3<Ec2eZV@?";
    protected String token;
    @Autowired
    SafaUserRepository safaUserRepository;

    @BeforeEach
    public void createData() {
        token = null;
        this.safaUserRepository.deleteAll();
    }

    public void authenticatedPost(String routeName,
                                  JSONObject body,
                                  ResultMatcher test) throws Exception {
        assertTokenExists();
        MockHttpServletRequestBuilder request = post(routeName)
            .content(body.toString())
            .contentType(MediaType.APPLICATION_JSON);
        sendRequest(request, test, this.token);
    }

    public void authenticatedGet(String routeName,
                                 ResultMatcher test) throws Exception {
        assertTokenExists();
        sendRequest(get(routeName), test, this.token);
    }

    private void assertTokenExists() throws ServerError {
        if (this.token == null || this.token.equals("")) {
            throw new ServerError("Authorization token not set.");
        }
    }

    public JSONObject createUser(String email, String password) throws Exception {
        JSONObject payload = new JSONObject();
        payload.put("email", email);
        payload.put("password", password);
        return sendPost("/sign-up", payload, status().is2xxSuccessful());
    }

    public void loginUser(String email, String password, ResultMatcher test) throws Exception {
        JSONObject user = new JSONObject();
        user.put("email", email);
        user.put("password", password);
        JSONObject response = sendPost("/login", user, test, new String[]{"token"});
        this.token = response.getString("token");
    }
}
