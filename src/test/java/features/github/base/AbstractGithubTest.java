package features.github.base;

import java.io.File;
import java.util.Optional;

import com.fasterxml.jackson.databind.ObjectMapper;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryBranchDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFiletreeResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mockito;
import org.springframework.core.io.ClassPathResource;

/**
 * Responsible for mocking the web service pulling GitHub data.
 */
public abstract class AbstractGithubTest extends ApplicationBaseTest {

    private static final String REPOSITORY_RESPONSE_FILE = "mock/github/repository_response.json";
    private static final String MASTER_BRANCH_RESPONSE_FILE = "mock/github/master_branch_response.json";
    private static final String FILETREE_RESPONSE_FILE = "mock/github/filetree_response.json";

    protected String githubLogin = "safaGithub";
    protected GithubAccessCredentials credentials = new GithubAccessCredentials();

    protected GithubConnectionService serviceMock;
    protected GithubAccessCredentialsRepository repositoryMock;

    @BeforeEach
    public void setup() {
        mockGithubService();
        mockRepository();

        serviceProvider.setGithubConnectionService(serviceMock);
        serviceProvider.setGithubAccessCredentialsRepository(repositoryMock);
    }

    private void mockGithubService() {
        serviceMock = Mockito.mock(GithubConnectionService.class);

        Mockito.when(serviceMock.getSelf(Mockito.any(GithubAccessCredentials.class)))
            .thenReturn(new GithubSelfResponseDTO(githubLogin));

        Mockito.when(serviceMock.getUserRepository(
            Mockito.any(GithubAccessCredentials.class),
            Mockito.any(String.class)
        )).thenReturn(
            this.readResourceFile(REPOSITORY_RESPONSE_FILE, GithubRepositoryDTO.class)
        );

        Mockito.when(serviceMock.getRepositoryBranch(
            Mockito.any(GithubAccessCredentials.class),
            Mockito.any(String.class),
            Mockito.any(String.class)
        )).thenReturn(
            this.readResourceFile(MASTER_BRANCH_RESPONSE_FILE, GithubRepositoryBranchDTO.class)
        );

        Mockito.when(serviceMock.getRepositoryFiles(
            Mockito.any(GithubAccessCredentials.class),
            Mockito.any(String.class),
            Mockito.any(String.class)
        )).thenReturn(
            this.readResourceFile(FILETREE_RESPONSE_FILE, GithubRepositoryFiletreeResponseDTO.class)
        );
    }

    private void mockRepository() {
        repositoryMock = Mockito.mock(GithubAccessCredentialsRepository.class);

        Mockito.when(repositoryMock.findByUser(Mockito.any(SafaUser.class)))
            .thenReturn(Optional.of(this.credentials));
    }

    private <T> T readResourceFile(String filepath, Class<T> clazz) {

        try {
            File file = new ClassPathResource(filepath).getFile();

            return new ObjectMapper().readValue(file, clazz);
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }
}
