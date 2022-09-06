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
public class TBertConfig {
    private static TBertConfig staticConfig;
    @Value("${tbert.endpoint}")
    private String baseEndpoint;

    public static TBertConfig get() {
        return TBertConfig.staticConfig;
    }

    public String getPredictEndpoint() {
        return FileUtilities.buildPath(baseEndpoint, "predict") + "/";
    }

    @PostConstruct
    public void init() {
        TBertConfig.staticConfig = this;
    }
}
