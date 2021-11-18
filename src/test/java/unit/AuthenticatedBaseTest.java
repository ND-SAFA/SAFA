package unit;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

public class AuthenticatedBaseTest extends EntityBaseTest {

    public static final String email = "abc123@gmail.com";
    public static final String password = "r{QjR3<Ec2eZV@?";
    protected String token;

    @Autowired
    SafaUserRepository safaUserRepository;

    @BeforeEach
    public void createData() throws Exception {
        token = null;
        this.safaUserRepository.deleteAll();
        this.defaultLogin();
    }

    public void defaultLogin() throws Exception {
        createUser(email, password);
        loginUser(email, password);
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

    public void assertTokenExists() throws ServerError {
        if (this.token == null || this.token.equals("")) {
            throw new ServerError("Authorization token not set.");
        }
    }

    public JSONObject createUser(String email, String password) throws Exception {
        JSONObject payload = new JSONObject();
        payload.put("email", email);
        payload.put("password", password);
        return sendPost("/sign-up", payload, status().is2xxSuccessful(), false);
    }

    public void loginUser(String email, String password) throws Exception {
        loginUser(email, password, status().is2xxSuccessful());
    }

    public void loginUser(String email, String password, ResultMatcher test) throws Exception {
        JSONObject user = new JSONObject();
        user.put("email", email);
        user.put("password", password);
        JSONObject response = sendRequest(addJsonBody(post("/login"), user), test, new String[]{"token"});
        this.token = response.getString("token");
    }
}
