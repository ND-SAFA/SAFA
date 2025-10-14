package edu.nd.crc.safa.config;

import edu.nd.crc.safa.utilities.ExecutorDelegate;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;


/**
 * Configures the threads used to serve the requests
 * to the server.
 */
@Configuration
public class ThreadConfiguration {

    @Value("${task-executor.controller.core-pool-size}")
    private int controllerCorePoolSize;
    @Value("${task-executor.controller.max-pool-size}")
    private int controllerMaxPoolSize;

    @Bean
    @Primary
    public ThreadPoolTaskExecutor controllerExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();

        executor.setCorePoolSize(controllerCorePoolSize);
        executor.setMaxPoolSize(controllerMaxPoolSize);
        executor.initialize();

        return executor;
    }

    @Bean
    public ExecutorDelegate executorDelegate() {
        return new ExecutorDelegate(controllerExecutor());
    }

    /**
     * I am leaving this method so that there is documentation about why this behavior was removed
     * in case anyone tries to add it back. MODE_INHERITABLETHREADLOCAL should NOT be used in a pooled
     * environment (see <a href="https://github.com/spring-projects/spring-security/issues/6856">this github issue</a>).
     * <br /><br />
     * To summarize: thread pools reuse threads (that's the whole point), but the security context is only copied
     * to the thread when it is first spawned. This means that subsequent jobs using that thread will use the old
     * context, which is likely to have been created for a different user. This creates instances where one user may
     * have access to parts of another user's account, if the request made for that object happened to be handled
     * from within the thread pool.
     * <br /><br />
     * Instead, the user's information needs to be retrieved in the thread that was originally handling the request
     * and then passed to the thread doing the background task.
     */
    @PostConstruct
    public void setSecurityContextMode() {
        // Only call this method once, otherwise the strategy will reset to default

        // DO NOT UNCOMMENT THIS LINE - SEE ABOVE COMMENT FOR EXPLANATION
        //SecurityContextHolder.setStrategyName(SecurityContextHolder.MODE_INHERITABLETHREADLOCAL);
    }
}
