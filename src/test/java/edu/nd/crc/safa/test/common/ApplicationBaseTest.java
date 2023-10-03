package edu.nd.crc.safa.test.common;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.AuthorizationTestService;
import edu.nd.crc.safa.test.services.CommitTestService;
import edu.nd.crc.safa.test.services.CreationTestService;
import edu.nd.crc.safa.test.services.LayoutTestService;
import edu.nd.crc.safa.test.services.MessageVerificationTestService;
import edu.nd.crc.safa.test.services.RetrievalTestService;
import edu.nd.crc.safa.test.services.assertions.VerificationTestSerfice;
import edu.nd.crc.safa.test.services.builders.BuilderState;
import edu.nd.crc.safa.test.services.builders.DbEntityBuilder;
import edu.nd.crc.safa.test.services.builders.JsonBuilder;
import edu.nd.crc.safa.test.services.builders.RootBuilder;
import edu.nd.crc.safa.test.services.notifications.NotificationTestService;

import jakarta.annotation.PostConstruct;
import lombok.Getter;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.batch.core.launch.support.TaskExecutorJobLauncher;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.core.task.SyncTaskExecutor;
import org.springframework.test.util.ReflectionTestUtils;

/**
 * Testing layer for encapsulating application logic.
 */
public abstract class ApplicationBaseTest extends EntityBaseTest {
    /**
     * Authentication
     */
    public static final String currentUserName = "root-test-user@gmail.com";
    public static final String defaultUserPassword = "r{QjR3<Ec2eZV@?";
    /**
     * Constants
     */
    private static final String TOKEN = "TOKEN";
    public static SafaUser currentUser;
    public String token;
    /**
     * Services
     */
    @Getter
    @LocalServerPort
    protected Integer port;
    protected String projectName = this.getClass().getName();
    protected CommitTestService commitService = new CommitTestService();
    protected NotificationTestService notificationService;
    protected CreationTestService creationService;
    protected VerificationTestSerfice assertionService;
    protected RetrievalTestService retrievalService;
    protected AuthorizationTestService authorizationService;
    protected MessageVerificationTestService changeMessageVerifies = new MessageVerificationTestService();
    protected LayoutTestService layoutTestService = new LayoutTestService();
    protected RootBuilder rootBuilder;
    /**
     * Builders
     */
    protected DbEntityBuilder dbEntityBuilder;
    protected JsonBuilder jsonBuilder;

    public static String getTokenName(String userName) {
        return String.format("%s-%s", userName, TOKEN);
    }

    @PostConstruct
    public void init() throws Exception {
        initJobLauncher();
        setLegacyModeInH2Database();
    }

    @BeforeEach
    public void testSetup() throws Exception {
        initBuilders();
        setAuthorization();
        ReflectionTestUtils.setField(ServiceProvider.class, "instance", this.serviceProvider);
    }

    /**
     * Creates database and json builders with current service provider.
     */
    private void initBuilders() {
        if (this.serviceProvider == null) {
            throw new SafaError("Unable to start test, service provider is null");
        }
        this.rootBuilder = new RootBuilder(this.serviceProvider, this.getPort());
        BuilderState state = rootBuilder.store(s -> s).get();
        this.dbEntityBuilder = new DbEntityBuilder(serviceProvider, customAttributeRepository,
            attributeSystemServiceProvider, artifactVersionRepositoryImpl);
        this.jsonBuilder = new JsonBuilder();
        this.creationService = new CreationTestService(this.getServiceProvider(), this.dbEntityBuilder);
        this.assertionService = new VerificationTestSerfice(state);
        this.retrievalService = new RetrievalTestService(getServiceProvider(), this.dbEntityBuilder);
        this.notificationService = new NotificationTestService(state, this.getPort());
        this.authorizationService = new AuthorizationTestService(this.getServiceProvider(), state);
    }


    /**
     * Sets the current job launcher to run job synchronously so that
     *
     * @throws Exception If error encountered during afterPropertiesSet.
     */
    private void initJobLauncher() throws Exception {
        TaskExecutorJobLauncher jobLauncher = new TaskExecutorJobLauncher();
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
    @AfterEach
    private void clearData() throws IOException {
        this.serviceProvider.getJobRepository().deleteAll();
        this.safaUserRepository.deleteAll();
        this.dbEntityBuilder.initializeData();
        this.jsonBuilder.initializeData();
        this.rootBuilder.clear();
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
        token = this.rootBuilder.authorize(AuthorizationTestService::createDefaultAccount).get();
        this.dbEntityBuilder.setCurrentUser(currentUser);
        ReflectionTestUtils.setField(SafaUserService.class, "CHECK_USER_THREAD", false);
    }
}
