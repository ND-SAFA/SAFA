package edu.nd.crc.safa.test.features.github.credentials;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.test.features.github.base.AbstractGithubTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import lombok.extern.log4j.Log4j2;
import org.json.JSONObject;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@Log4j2
@Disabled("Needs to be updated when GithubControllerUtils is updated")
public class TestGithubCredentials extends AbstractGithubTest {
    @Override
    protected void mockRepositoryFindByUser() {
    }

    @Test
    void checkingIfValidButMissingCredentials() throws Exception {
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Credentials.VALID)
            .getWithoutBody(MockMvcResultMatchers.status().is2xxSuccessful());

        //Assertions.assertEquals(GithubResponseDTO.GithubResponseMessage.MISSING.name(),
        //    response.get("message"));
    }
    
}
