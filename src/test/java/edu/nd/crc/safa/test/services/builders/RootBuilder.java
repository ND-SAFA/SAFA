package edu.nd.crc.safa.test.services.builders;

import java.util.function.BiFunction;
import java.util.function.Function;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.test.services.AuthorizationTestService;
import edu.nd.crc.safa.test.services.CommonRequestService;
import edu.nd.crc.safa.test.services.assertions.VerificationTestService;
import edu.nd.crc.safa.test.services.notifications.NotificationTestService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class RootBuilder {
    private static final Logger logger = LoggerFactory.getLogger(AndBuilder.class);
    private BuilderState state;
    private NotificationTestService notificationTestService;
    private DatabaseTestBuilder databaseTestBuilder;
    private AuthorizationTestService authorizationTestService;
    private VerificationTestService verificationTestService;
    private CommonRequestService commonRequestService;
    private ActionBuilder actionBuilder;

    public RootBuilder(ServiceProvider serviceProvider, int port) {
        this.state = new BuilderState();
        this.state.setServiceProvider(serviceProvider);
        this.state.setPort(port);
    }

    public void clear() {
        BuilderState newState = new BuilderState();
        newState.setServiceProvider(this.state.getServiceProvider());
        newState.setPort(this.state.getPort());
        this.state = newState;
        if (this.notificationTestService != null) {
            this.notificationTestService.clearServer();
        }
        this.notificationTestService = null;
        this.databaseTestBuilder = null;
        this.authorizationTestService = null;
        this.verificationTestService = null;
        this.commonRequestService = null;
        this.actionBuilder = null;
    }

    public RootBuilder log(String message) {
        logger.info(message);
        return this;
    }

    /**
     * Creates new database entity builder.
     *
     * @return DatabaseBuilder
     */
    public <T> AndBuilder<RootBuilder, T> authorize(BiFunction<BuilderState, AuthorizationTestService, T> consumer) {
        AuthorizationTestService authorizationTestService = this.getAuthorizationTestService();
        T result = consumer.apply(state, authorizationTestService);
        return new AndBuilder<>(this, result, this.state);
    }

    public <T> AndBuilder<RootBuilder, T> authorize(Function<AuthorizationTestService, T> consumer) {
        return authorize((s, a) -> consumer.apply(a));
    }

    public AuthorizationTestService getAuthorizationTestService() {
        if (this.authorizationTestService == null) {
            ServiceProvider serviceProvider = this.state.getServiceProvider();
            this.authorizationTestService = new AuthorizationTestService(serviceProvider, this.state);
        }
        return this.authorizationTestService;
    }

    /**
     * Creates new database entity builder.
     *
     * @return DatabaseBuilder
     */
    public <T> AndBuilder<RootBuilder, T> build(BiFunction<BuilderState, DatabaseTestBuilder, T> consumer) {
        DatabaseTestBuilder databaseTestBuilder = this.getDatabaseTestBuilder();
        T result = consumer.apply(this.state, databaseTestBuilder);
        return new AndBuilder<>(this, result, this.state);
    }

    public <T> AndBuilder<RootBuilder, T> build(Function<DatabaseTestBuilder, T> consumer) {
        return build((s, b) -> consumer.apply(b));
    }

    public DatabaseTestBuilder getDatabaseTestBuilder() {
        if (this.databaseTestBuilder == null) {
            ServiceProvider serviceProvider = state.getServiceProvider();
            this.databaseTestBuilder = new DatabaseTestBuilder(serviceProvider, this.state);
        }
        return this.databaseTestBuilder;
    }

    /**
     * Creates a new notification test service.
     *
     * @return New service instance.
     */
    public <T> AndBuilder<RootBuilder, T> notifications(BiFunction<BuilderState, NotificationTestService, T> consumer) {
        NotificationTestService notificationTestService = this.getNotificationTestService();
        T result = consumer.apply(this.state, notificationTestService);
        return new AndBuilder<>(this, result, this.state);
    }

    public <T> AndBuilder<RootBuilder, T> notifications(Function<NotificationTestService, T> consumer) {
        return notifications((s, n) -> consumer.apply(n));
    }

    public NotificationTestService getNotificationTestService() {
        if (this.notificationTestService == null) {
            int port = this.state.getPort();
            this.notificationTestService = new NotificationTestService(this.state, port);
        }
        return this.notificationTestService;
    }

    /**
     * Creates new verification test service.
     */
    public <T> AndBuilder<RootBuilder, T> verify(BiFunction<BuilderState, VerificationTestService, T> consumer) {
        VerificationTestService verificationTestService = this.getAssertionTestService();
        T result = consumer.apply(this.state, verificationTestService);
        return new AndBuilder<>(this, result, this.state);
    }

    public <T> AndBuilder<RootBuilder, T> verify(Function<VerificationTestService, T> consumer) {
        return verify((s, v) -> consumer.apply(v));
    }

    public VerificationTestService getAssertionTestService() {
        if (this.verificationTestService == null) {
            this.verificationTestService = new VerificationTestService(this.state);
        }
        return this.verificationTestService;
    }

    /**
     * Creates new instance of common requests test service.
     */
    public <T> AndBuilder<RootBuilder, T> request(BiFunction<BuilderState, CommonRequestService, T> consumer) {
        CommonRequestService commonRequestService = this.getCommonRequestService();
        T result = consumer.apply(this.state, commonRequestService);
        return new AndBuilder<>(this, result, this.state);
    }

    public <T> AndBuilder<RootBuilder, T> request(Function<CommonRequestService, T> consumer) {
        return request((s, r) -> consumer.apply(r));
    }

    public CommonRequestService getCommonRequestService() {
        if (this.commonRequestService == null) {
            this.commonRequestService = new CommonRequestService(this.state);
        }
        return this.commonRequestService;
    }

    /**
     * Creates new database entity builder.
     *
     * @return DatabaseBuilder
     */
    public <T> AndBuilder<RootBuilder, T> actions(BiFunction<BuilderState, ActionBuilder, T> consumer) {
        ActionBuilder actionBuilder = this.getActionBuilder();
        T result = consumer.apply(this.state, actionBuilder);
        return new AndBuilder<>(this, result, this.state);
    }

    public <T> AndBuilder<RootBuilder, T> actions(Function<ActionBuilder, T> consumer) {
        return actions((s, a) -> consumer.apply(a));
    }

    public ActionBuilder getActionBuilder() {
        if (this.actionBuilder == null) {
            this.actionBuilder = new ActionBuilder(this);
        }
        return this.actionBuilder;
    }

    /**
     * Provides access to builder state.
     */
    public <T> AndBuilder<RootBuilder, T> store(Function<BuilderState, T> consumer) {
        T result = consumer.apply(this.state);
        return new AndBuilder<>(this, result, this.state);
    }
}
