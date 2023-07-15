package edu.nd.crc.safa.config;

import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.models.ITraceGenerationController;
import edu.nd.crc.safa.features.models.vsm.VSMController;
import edu.nd.crc.safa.features.generation.tgen.TGen;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

/**
 * Enables VSM to be used for unit tests while TGEN for production.
 */
@Configuration
public class TraceLinkGenerationConfig {

    @Bean
    @Profile("test")
    public ITraceGenerationController getVSM() {
        return new VSMController();
    }

    @Bean
    @Profile("!test")
    public ITraceGenerationController getTGen(@Autowired SafaRequestBuilder safaRequestBuilder) {
        return new TGen(safaRequestBuilder);
    }
}
