package edu.nd.crc.safa.config;

import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.generation.GenerationApi;
import edu.nd.crc.safa.features.traces.ITraceGenerationController;
import edu.nd.crc.safa.features.traces.vsm.VSMController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.core.env.Environment;

/**
 * Enables VSM to be used for unit tests while TGEN for production.
 */
@Configuration
public class TraceLinkGenerationConfig {
    private static Environment environment;

    @Autowired
    public TraceLinkGenerationConfig(Environment environment) {
        TraceLinkGenerationConfig.environment = environment;
    }

    public static boolean isTestEnvironment() {
        return environment.acceptsProfiles("test");
    }

    @Bean
    @Profile("test")
    public ITraceGenerationController getVSM() {
        return new VSMController();
    }

    @Bean
    @Profile("!test")
    public ITraceGenerationController getTGen(@Autowired SafaRequestBuilder safaRequestBuilder) {
        return new GenerationApi(safaRequestBuilder);
    }

    @Autowired
    public void setEnvironment(Environment environment) {
        TraceLinkGenerationConfig.environment = environment;
    }
}
