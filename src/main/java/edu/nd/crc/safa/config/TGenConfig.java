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

    /**
     * Returns TGEN endpoint path.
     *
     * @param endpointName The name of the endpoint.
     * @return Endpoint path according to current environment.
     */
    public static String getEndpoint(String endpointName) {
        TGenConfig config = get();
        return buildTGenEndpoint(config.baseEndpoint, endpointName);
    }

    private static String buildTGenEndpoint(String... components) {
        return FileUtilities.buildUrl(components) + FileUtilities.URL_SEP;
    }

    @PostConstruct
    public void init() {
        TGenConfig.staticConfig = this;
    }
}
