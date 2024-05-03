package edu.nd.crc.safa.test.features.github.base;

import java.io.File;
import java.util.Optional;
import java.util.stream.IntStream;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoryResponse;
import edu.nd.crc.safa.features.github.entities.app.GithubCommitDiffResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubFileBlobDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFiletreeResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.core.io.ClassPathResource;

/**
 * Responsible for mocking the web service pulling GitHub data.
 */
public abstract class AbstractGithubTest extends ApplicationBaseTest {

    private static final String REPOSITORY_RESPONSE_FILE = "mock/github/repository_response.json";
    private static final String FILETREE_RESPONSE_FILE = "mock/github/filetree_response.json";
    private static final String DIFF_RESPONSE_FILE = "mock/github/diff_response.json";

    protected String repositoryName = "home_assistant_ro";
    protected String githubLogin = "safaGithub";
    protected GithubAccessCredentials credentials = new GithubAccessCredentials();

    @MockBean
    protected GithubConnectionService serviceMock;

    @MockBean
    protected GithubGraphQlService gqlServiceMock;

    @MockBean
    protected GithubAccessCredentialsRepository repositoryMock;

    protected AutoCloseable closeable;

    @BeforeEach
    public void setup() {
        this.mockGithubService();
        this.mockRepositoryFindByUser();

        closeable = MockitoAnnotations.openMocks(this);
    }

    @AfterEach
    public void destroy() throws Exception {
        if (closeable != null) {
            closeable.close();
        }
    }

    private void mockGithubService() {
        Mockito.when(serviceMock.getSelf(Mockito.any(GithubAccessCredentials.class)))
            .thenReturn(new GithubSelfResponseDTO(githubLogin));

        Mockito.when(gqlServiceMock.getGithubRepository(
            Mockito.any(SafaUser.class),
            Mockito.any(String.class),
            Mockito.any(String.class)
        )).thenReturn(
            this.readResourceFile(REPOSITORY_RESPONSE_FILE, GithubGraphQlRepositoryResponse.class)
        );

        Mockito.when(serviceMock.getRepositoryFiles(
            Mockito.any(GithubAccessCredentials.class),
            Mockito.any(String.class),
            Mockito.any(String.class)
        )).thenReturn(
            this.readResourceFile(FILETREE_RESPONSE_FILE, GithubRepositoryFiletreeResponseDTO.class)
        );

        Mockito.when(serviceMock.getDiffBetweenOldCommitAndHead(
            Mockito.any(GithubAccessCredentials.class),
            Mockito.any(String.class),
            Mockito.any(String.class),
            Mockito.any(String.class),
            Mockito.any(String.class)
        )).thenReturn(
            this.readResourceFile(DIFF_RESPONSE_FILE, GithubCommitDiffResponseDTO.class)
        );

        GithubFileBlobDTO file = new GithubFileBlobDTO();
        Mockito.when(serviceMock.getBlobInformation(Mockito.any(), Mockito.any()))
            .thenReturn(file);
    }

    protected void mockRepositoryFindByUser() {
        this.mockRepositoryFindByUser(this.credentials);
    }

    protected void mockRepositoryFindByUser(GithubAccessCredentials credentials) {
        Mockito.when(repositoryMock.findByUser(Mockito.any(SafaUser.class)))
            .thenReturn(Optional.of(credentials));
        Mockito.when(serviceMock.getGithubCredentials(Mockito.any(SafaUser.class)))
            .thenReturn(Optional.of(credentials));
    }

    protected void mockRepositoryDelete() {
        Mockito.doNothing()
            .when(repositoryMock).delete(Mockito.any(GithubAccessCredentials.class));
    }

    protected <T> T readResourceFile(String filepath, Class<T> clazz) {
        try {
            File file = new ClassPathResource(filepath).getFile();

            return ObjectMapperConfig.create().readValue(file, clazz);
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }

    protected void createBaseSafaProject(String projectName, int initialArtifactCount) {
        String artifactTypeName = "requirement";

        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactTypeName);

        IntStream.range(0, initialArtifactCount).mapToObj(String::valueOf).forEach(name ->
            dbEntityBuilder.newArtifactAndBody(projectName, artifactTypeName, name, "", ""));
    }
}
