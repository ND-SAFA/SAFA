package features.github.credentials;

import java.time.LocalDateTime;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.github.entities.app.GithubResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import features.github.base.AbstractGithubTest;
import lombok.extern.log4j.Log4j2;
import org.json.JSONObject;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import requests.SafaRequest;

@Log4j2
public class TestGithubCredentials extends AbstractGithubTest {
    @Override
    protected void mockRepositoryFindByUser() {
    }

    @Test
    void checkingIfValidButMissingCredentials() throws Exception {
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Credentials.VALID)
            .getWithoutBody(MockMvcResultMatchers.status().is2xxSuccessful());

        Assertions.assertEquals(GithubResponseDTO.GithubResponseMessage.MISSING.name(),
            response.get("message"));
    }

    @Test
    void checkingInvalidCredentialsDeletesThem() throws Exception {
        GithubAccessCredentials credentials = new GithubAccessCredentials();

        credentials.setRefreshTokenExpirationDate(LocalDateTime.MIN);
        super.mockRepositoryFindByUser(credentials);
        super.mockRepositoryDelete();

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Credentials.VALID)
            .getWithoutBody(MockMvcResultMatchers.status().is2xxSuccessful());

        Assertions.assertEquals(GithubResponseDTO.GithubResponseMessage.EXPIRED.name(),
            response.get("message"));

        Mockito.verify(repositoryMock, Mockito.times(1))
            .delete(Mockito.any(GithubAccessCredentials.class));
    }
}
