package edu.nd.crc.safa.test.common;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.builders.DbEntityBuilder;
import edu.nd.crc.safa.test.builders.JsonBuilder;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.AssertionTestService;
import edu.nd.crc.safa.test.services.AuthorizationTestService;
import edu.nd.crc.safa.test.services.CommitTestService;
import edu.nd.crc.safa.test.services.CreationTestService;
import edu.nd.crc.safa.test.services.LayoutTestService;
import edu.nd.crc.safa.test.services.MessageVerificationTestService;
import edu.nd.crc.safa.test.services.NotificationTestService;
import edu.nd.crc.safa.test.services.RetrievalTestService;

import org.junit.jupiter.api.BeforeEach;
import org.springframework.batch.core.launch.support.SimpleJobLauncher;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.core.task.SyncTaskExecutor;
import org.springframework.test.util.ReflectionTestUtils;

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
    protected CommitTestService commitService = new CommitTestService();
    protected NotificationTestService notificationService;
    protected CreationTestService creationService;
    protected AssertionTestService assertionService = new AssertionTestService();
    protected RetrievalTestService retrievalService;
    protected AuthorizationTestService authorizationService;
    protected MessageVerificationTestService changeMessageVerifies = new MessageVerificationTestService();
    protected LayoutTestService layoutTestService = new LayoutTestService();
    /**
     * Builders
     */
    protected DbEntityBuilder dbEntityBuilder;
    protected JsonBuilder jsonBuilder;

    @PostConstruct
    public void init() throws Exception {
        initBuilders();
        initTestServices();
        initJobLauncher();
        setLegacyModeInH2Database();
    }

    @BeforeEach
    public void testSetup() throws Exception {
        clearData();
        setAuthorization();
        ReflectionTestUtils.setField(ServiceProvider.class, "instance", this.serviceProvider);
    }

    /**
     * Creates database and json builders with current service provider.
     */
    private void initBuilders() {
        assert this.serviceProvider != null;
        this.dbEntityBuilder = new DbEntityBuilder(serviceProvider, customAttributeRepository,
            attributeSystemServiceProvider);
        this.jsonBuilder = new JsonBuilder();
    }

    /**
     * Initializes test services with service provider and database entity builder.
     */
    private void initTestServices() {
        assert this.dbEntityBuilder != null;
        notificationService = new NotificationTestService(port);
        creationService = new CreationTestService(this.serviceProvider, this.dbEntityBuilder);
        retrievalService = new RetrievalTestService(this.serviceProvider, this.dbEntityBuilder);
        authorizationService = new AuthorizationTestService(this.serviceProvider, this.dbEntityBuilder);
    }

    /**
     * Sets the current job launcher to run job synchronously so that
     *
     * @throws Exception If error encountered during afterPropertiesSet.
     */
    private void initJobLauncher() throws Exception {
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
    private void setLegacyModeInH2Database() throws SQLException {
        String query = "SET MODE LEGACY;\n";
        Connection connection = this.dataSource.getConnection();
        try (Statement statement = connection.createStatement()) {
            statement.execute(query);
        }
        connection.close();
    }

    /**
     * Clears data in database.
     *
     * @throws IOException If error occurs while deleting data.
     */
    private void clearData() throws IOException {
        this.serviceProvider.getJobRepository().deleteAll();
        this.safaUserRepository.deleteAll();
        this.dbEntityBuilder.createEmptyData();
        this.jsonBuilder.createEmptyData();
    }

    /**
     * Creates new user and logs in, setting global test token.
     *
     * @throws Exception If error occurs while logging in.
     */
    private void setAuthorization() throws Exception {
        SafaRequest.setMockMvc(mockMvc);
        SafaRequest.clearAuthorizationToken();
        token = null;
        this.authorizationService.defaultLogin();
        this.dbEntityBuilder.setCurrentUser(currentUser);
        ReflectionTestUtils.setField(SafaUserService.class, "CHECK_USER_THREAD", false);
    }
}
