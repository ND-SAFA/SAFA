package features.users.crud;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Objects;
import java.util.Optional;

import common.ApplicationBaseTest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.email.EmailService;
import edu.nd.crc.safa.features.users.entities.app.ResetPasswordRequestDTO;
import edu.nd.crc.safa.features.users.entities.app.UserIdentifierDTO;
import edu.nd.crc.safa.features.users.entities.db.PasswordResetToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.PasswordResetTokenRepository;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.security.crypto.password.PasswordEncoder;
import requests.SafaRequest;

public class TestPasswordReset extends ApplicationBaseTest {
    private final String testEmail = "abc@test.com";
    private final String testPassword = "password123";

    @MockBean
    private EmailService emailService;

    @Autowired
    private PasswordResetTokenRepository tokenRepository;

    @Autowired
    private SafaUserRepository safaUserRepository;

    @Autowired
    private PasswordEncoder encoder;

    private AutoCloseable closeable;

    @BeforeEach
    @Override
    public void testSetup() throws Exception {
        Mockito.doNothing().when(emailService).send(
            Mockito.anyString(),
            Mockito.anyString(),
            Mockito.anyString());

        tokenRepository.deleteAll();
        closeable = MockitoAnnotations.openMocks(this);
        super.testSetup();
    }

    @AfterEach
    public void destroy() throws Exception {
        if (closeable != null) {
            closeable.close();
        }
    }

    @Test
    public void testResetTokenIsIssued() throws Exception {
        authorizationService.createUser(testEmail, testPassword);

        SafaUser storedUser = issueForgetPasswordCall();

        Assertions.assertEquals(1, tokenRepository.count());

        Optional<SafaUser> safaUser = tokenRepository.findAll()
            .stream()
            .findFirst()
            .map(PasswordResetToken::getUser)
            .filter(t -> t.getEmail().equals(storedUser.getEmail()));

        Assertions.assertTrue(safaUser.isPresent());
    }

    @Test
    public void testPasswordIsChanged() throws Exception {
        authorizationService.createUser(testEmail, testPassword);

        String newPassword = "newPassword";
        SafaUser storedUser = issueForgetPasswordCall();
        String token = tokenRepository.findAll()
            .stream()
            .findFirst()
            .map(PasswordResetToken::getToken)
            .orElse(null);

        SafaRequest
            .withRoute(AppRoutes.Accounts.RESET_PASSWORD)
            .putWithJsonObject(new ResetPasswordRequestDTO(token, newPassword),
                status().is2xxSuccessful());

        Optional<SafaUser> safaUser = safaUserRepository.findByEmail(testEmail);

        Assertions.assertTrue(safaUser.isPresent());
        Assertions.assertTrue(encoder.matches(newPassword, safaUser.get().getPassword()));
        Assertions.assertEquals(0, tokenRepository.count());
    }

    private SafaUser issueForgetPasswordCall() throws Exception {
        SafaUser storedUser = Objects.requireNonNull(
            serviceProvider.getSafaUserRepository().findByEmail(testEmail).orElse(null));
        UserIdentifierDTO userIdentifierDTO = new UserIdentifierDTO(storedUser);
        SafaRequest
            .withRoute(AppRoutes.Accounts.FORGOT_PASSWORD)
            .putWithJsonObject(userIdentifierDTO, status().is2xxSuccessful());

        return storedUser;
    }

}
