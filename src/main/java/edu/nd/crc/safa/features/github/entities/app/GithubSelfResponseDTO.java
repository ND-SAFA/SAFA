package edu.nd.crc.safa.features.github.entities.app;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Transfer object wrapping data we need from the /self endpoint
 */
@Data
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubSelfResponseDTO {

    /**
     * GitHub username
     */
    private String login;

}
