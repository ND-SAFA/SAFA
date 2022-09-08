package features.github.base;

import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mockito;

/**
 * Responsible for mocking the web service pulling GitHub data.
 */
public abstract class AbstractGithubTest extends ApplicationBaseTest {

    protected String githubLogin = "safaGithub";
    protected GithubConnectionService serviceMock;
    protected GithubAccessCredentialsRepository repositoryMock;

    @BeforeEach
    public void setup() {
        mockGithubService();

        serviceProvider.setGithubConnectionService(serviceMock);
    }

    private void mockGithubService() {
        serviceMock = Mockito.mock(GithubConnectionService.class);

        Mockito.when(serviceMock.getSelf(Mockito.any(GithubAccessCredentials.class)))
            .thenReturn(new GithubSelfResponseDTO(githubLogin));
    }

    private void mockRepository() {
    }
}
