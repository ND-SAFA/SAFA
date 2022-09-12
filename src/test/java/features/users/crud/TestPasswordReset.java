package features.users.crud;

import edu.nd.crc.safa.features.email.EmailService;
import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestPasswordReset extends ApplicationBaseTest {
    private final String testEmail = "abc@test.com";
    private final String testPassword = "password123";

    @MockBean
    private EmailService emailService;

    @BeforeEach
    public void init() throws Exception {
        Mockito.doNothing().when(emailService).send(
            Mockito.any(String.class),
            Mockito.any(String.class),
            Mockito.any(String.class));
    }

    @Test
    public void testResetTokenIsIssued() {

    }

}
