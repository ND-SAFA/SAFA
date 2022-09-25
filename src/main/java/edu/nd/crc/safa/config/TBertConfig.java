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
    @Value("${tgen.endpoint}")
    private String baseEndpoint;

    public static TBertConfig get() {
        return TBertConfig.staticConfig;
    }

    public String getPredictEndpoint() {
        return FileUtilities.buildPath(baseEndpoint, "predict") + "/";
    }

    public String getTrainEndpoint() {
        return FileUtilities.buildPath(baseEndpoint, "fine-tune") + "/";
    }

    public String getCreateModelEndpoint() {
        return FileUtilities.buildPath(baseEndpoint, "models") + "/";
    }

    @PostConstruct
    public void init() {
        TBertConfig.staticConfig = this;
    }
}
