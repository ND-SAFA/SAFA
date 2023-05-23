package edu.nd.crc.safa.config;

import javax.annotation.PostConstruct;

import edu.nd.crc.safa.utilities.FileUtilities;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

/**
 * Responsible for any parameters surrounding TBert.
 */
@Configuration
@Getter
public class TGenConfig {
    private static TGenConfig staticConfig;
    @Value("${tgen.endpoint}")
    private String baseEndpoint;

    public static TGenConfig get() {
        return TGenConfig.staticConfig;
    }
    
    @PostConstruct
    public void init() {
        TGenConfig.staticConfig = this;
    }

    public String getTGenEndpoint(String endpointName) {
        return buildTGenEndpoint(baseEndpoint, endpointName);
    }

    public String buildTGenEndpoint(String... components) {
        return FileUtilities.buildUrl(components) + FileUtilities.URL_SEP;
    }
}
