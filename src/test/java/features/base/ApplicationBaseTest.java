package features.base;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import common.AssertionTestService;
import common.AuthorizationTestService;
import common.CommitTestService;
import common.CreationTestService;
import common.NotificationTestService;
import common.RetrievalTestService;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.batch.core.launch.support.SimpleJobLauncher;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.core.task.SyncTaskExecutor;

/**
 * Testing layer for encapsulating application logic.
 */
public abstract class ApplicationBaseTest extends EntityBaseTest {
    /**
     * Authentication
     */
    public static final String defaultUser = "root-test-user@gmail.com";
    public static final String defaultUserPassword = "r{QjR3<Ec2eZV@?";
    public static SafaUser currentUser;
    public String token;
    /**
     * Services
     */
    @LocalServerPort
    protected Integer port;
    protected String projectName = this.getClass().getName();
    protected CommitTestService commitTestService = new CommitTestService();
    protected NotificationTestService notificationTestService;
    protected CreationTestService setupTestService;
    protected AssertionTestService assertionTestService = new AssertionTestService();
    protected RetrievalTestService retrievalTestService;
    protected AuthorizationTestService authorizationTestService;

    @PostConstruct
    public void init() throws Exception {
        initTestServices();
        initJobLauncher();
        setLegacyModeInH2Database();
    }

    @BeforeEach
    public void createAuthenticationData() throws Exception {
        token = null;
        this.safaUserRepository.deleteAll();
        SafaRequest.setMockMvc(mockMvc);
        this.authorizationTestService.defaultLogin();
        this.dbEntityBuilder.setCurrentUser(currentUser);
    }

    @AfterEach
    public void clearAuthentication() {
        SafaRequest.clearAuthorizationToken();
    }

    /**
     * Initializes test services with service provider and database entity builder.
     */
    public void initTestServices() {
        notificationTestService = new NotificationTestService(port);
        setupTestService = new CreationTestService(this.serviceProvider, this.dbEntityBuilder);
        retrievalTestService = new RetrievalTestService(this.serviceProvider, this.dbEntityBuilder);
        authorizationTestService = new AuthorizationTestService(this.serviceProvider, this.dbEntityBuilder);
    }

    /**
     * Sets the current job launcher to run job synchronously so that
     *
     * @throws Exception If error encountered during afterPropertiesSet.
     */
    public void initJobLauncher() throws Exception {
        SimpleJobLauncher jobLauncher = new SimpleJobLauncher();
        jobLauncher.setJobRepository(jobRepository);
        jobLauncher.setTaskExecutor(new SyncTaskExecutor());
        jobLauncher.afterPropertiesSet();

        serviceProvider.setJobLauncher(jobLauncher);
    }

    /**
     * Sets the testing database's mode, H2, to legacy in order for spring
     * batch to be able to initialize its own tables.
     *
     * @throws SQLException Throws exception if unable to set legacy mode.
     */
    public void setLegacyModeInH2Database() throws SQLException {
        String query = "SET MODE LEGACY;\n";
        Connection connection = this.dataSource.getConnection();
        try (Statement statement = connection.createStatement()) {
            statement.execute(query);
        }
        connection.close();
    }
}
