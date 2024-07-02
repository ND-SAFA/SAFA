package edu.nd.crc.safa.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "fend")
@Data
public class FendPathConfig {

    private final String base;
    private final String resetEmailPath;
    private final String verifyEmailPath;
    private final String acceptInviteUrl;

    public String getResetPasswordUrl() {
        return base + resetEmailPath;
    }

    public String getVerifyEmailUrl() {
        return base + verifyEmailPath;
    }

}
