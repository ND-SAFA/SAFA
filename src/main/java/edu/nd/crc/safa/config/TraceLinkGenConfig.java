package edu.nd.crc.safa.config;

import edu.nd.crc.safa.features.traces.ITraceGenerationController;
import edu.nd.crc.safa.features.traces.vsm.VSMController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;
import org.springframework.core.env.Environment;

/**
 * Enables VSM to be used for unit tests while TGEN for production.
 */
@Configuration
public class TraceLinkGenConfig {
    private static Environment environment;

    @Autowired
    public TraceLinkGenConfig(Environment environment) {
        TraceLinkGenConfig.environment = environment;
    }

    public static boolean isTestEnvironment() {
        return environment.acceptsProfiles("test");
    }

    @Bean
    @Primary
    @Profile("test")
    public ITraceGenerationController getVSM() {
        return new VSMController();
    }

//    @Bean
//    @Profile("!test")
//    public ITraceGenerationController getTGen(@Autowired GenerationApi generationApi) {
//        return generationApi;
//    }

    @Autowired
    public void setEnvironment(Environment environment) {
        TraceLinkGenConfig.environment = environment;
    }
}
