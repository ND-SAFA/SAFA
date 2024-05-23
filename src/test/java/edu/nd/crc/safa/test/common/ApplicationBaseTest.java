package edu.nd.crc.safa.test.common;

import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.AuthorizationTestService;
import edu.nd.crc.safa.test.services.CommitTestService;
import edu.nd.crc.safa.test.services.CreationTestService;
import edu.nd.crc.safa.test.services.LayoutTestService;
import edu.nd.crc.safa.test.services.MessageVerificationTestService;
import edu.nd.crc.safa.test.services.RetrievalTestService;
import edu.nd.crc.safa.test.services.assertions.VerificationTestService;
import edu.nd.crc.safa.test.services.builders.BuilderState;
import edu.nd.crc.safa.test.services.builders.DbEntityBuilder;
import edu.nd.crc.safa.test.services.builders.JsonBuilder;
import edu.nd.crc.safa.test.services.builders.RootBuilder;

import jakarta.annotation.PostConstruct;
import lombok.Getter;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
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
    private static final String TOKEN = "TOKEN";
    /**
     * Constants
     */
    private final Logger log = LoggerFactory.getLogger(ApplicationBaseTest.class);
    private final Map<UUID, String> usertokenMap = new HashMap<>();
    /**
     * Services
     */
    @Getter
    @LocalServerPort
    protected Integer port;
    protected String projectName = this.getClass().getSimpleName();
    protected CommitTestService commitService = new CommitTestService();
    protected CreationTestService creationService;
    protected VerificationTestService assertionService;
    protected RetrievalTestService retrievalService;
    protected AuthorizationTestService authorizationService;
    protected MessageVerificationTestService messageVerificationService = new MessageVerificationTestService();
    protected LayoutTestService layoutTestService = new LayoutTestService();
    protected RootBuilder rootBuilder;
    /**
     * Builders
     */
    protected DbEntityBuilder dbEntityBuilder;
    protected JsonBuilder jsonBuilder;
    @Getter
    private SafaUser currentUser;

    public static String getTokenName(String userName) {
        return String.format("%s-%s", userName, TOKEN);
    }


    /**
     * Initializes test environment.
     */
    @PostConstruct
    public void initTestEnvironment() throws Exception {
        initJobLauncher();
        setLegacyModeInH2Database();
    }

    /**
     * Initializes the resources needed for each individual test.
     */
    @BeforeEach
    public void initTestResources() throws Exception {
        initServices();
        initDefaultAccount();
        ReflectionTestUtils.setField(ServiceProvider.class, "instance", this.serviceProvider);
    }

    /**
     * Clears data in database.
     *
     * @throws IOException If error occurs while deleting data.
     */
    @AfterEach
    protected void clearData() throws IOException {
        this.serviceProvider.getJobRepository().deleteAll();
        this.safaUserRepository.deleteAll();
        this.dbEntityBuilder.initializeData();
        this.jsonBuilder.initializeData();
        this.rootBuilder.clear();
    }

    /**
     * Creates default account and sets the current authorization to it.
     */
    private void initDefaultAccount() throws Exception {
        this.currentUser = this.rootBuilder
            .authorize(a -> a
                .createUser(currentUserName, defaultUserPassword)
                .and()
                .getAccount(currentUserName))
            .get();
        this.currentUser.setPassword(defaultUserPassword);
        setAuthorization(this.currentUser);

        // TODO endpoint to set payment tier
        Organization defaultOrg = serviceProvider.getOrganizationService().getOrganizationById(currentUser.getDefaultOrgId());
        defaultOrg.setPaymentTier(PaymentTier.UNLIMITED);
        serviceProvider.getOrganizationService().updateOrganization(defaultOrg);
    }

    /**
     * Creates database and json builders with current service provider.
     */
    private void initServices() {
        if (this.serviceProvider == null) {
            throw new SafaError("Unable to start test, service provider is null");
        }
        this.rootBuilder = new RootBuilder(this.serviceProvider, this.getPort());
        BuilderState state = rootBuilder.store(s -> s).get();
        this.dbEntityBuilder = new DbEntityBuilder(serviceProvider, customAttributeRepository,
            attributeSystemServiceProvider);
        this.jsonBuilder = new JsonBuilder();
        this.creationService = new CreationTestService(this.getServiceProvider(), this.dbEntityBuilder);
        this.assertionService = new VerificationTestService(state);
        this.retrievalService = new RetrievalTestService(getServiceProvider(), this.dbEntityBuilder);
        this.authorizationService = new AuthorizationTestService(this.getServiceProvider(), state);
        SafaRequest.setMockMvc(mockMvc);
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
     * Creates new user and logs in, setting global test token.
     *
     * @throws Exception If error occurs while logging in.
     */
    private void setAuthorization(SafaUser user) throws Exception {
        SafaRequest.clearAuthorizationToken();
        clearToken(user);
        String token =
            this.rootBuilder.authorize(a -> a.loginUser(user.getEmail(), user.getPassword(), this).get()).get();
        this.setToken(user, token);
        this.dbEntityBuilder.setCurrentUser(user);
        ReflectionTestUtils.setField(SafaUserService.class, "CHECK_USER_THREAD", false);
    }

    public String getToken(IUser user) {
        if (!this.usertokenMap.containsKey(user.getUserId())) {
            throw new SafaError(String.format("User %s does not contain token.", user.getEmail()));
        }
        return this.usertokenMap.get(user.getUserId());
    }

    private void setToken(IUser user, String token) {
        if (this.usertokenMap.containsKey(user.getUserId())) {
            log.info("Overriding user token:" + user.getEmail());
        }
        this.usertokenMap.put(user.getUserId(), token);
    }

    private void clearToken(IUser user) {
        this.usertokenMap.remove(user.getUserId());
    }

    public void setCurrentUser(SafaUser user, String token) {
        setToken(user, token);
        this.currentUser = user;
    }

    public void setCurrentUser(SafaUser user) {
        setToken(user, getToken(user));
        this.currentUser = user;
    }
}
