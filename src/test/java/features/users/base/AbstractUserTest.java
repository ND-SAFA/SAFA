package features.users.base;

import requests.SafaRequest;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.BeforeEach;

public class AbstractUserTest extends ApplicationBaseTest {
    protected String testEmail = "abc123@gmail.com";
    protected String testPassword = "r{QjR3<Ec2eZV@?";

    @BeforeEach
    public void clearUsers() {
        // Base controller (AuthenticatedBaseTest) clears all accounts before each test.
        SafaRequest.clearAuthorizationToken();
    }
}
