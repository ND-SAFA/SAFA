package edu.nd.crc.safa.server.controllers.utils;

import edu.nd.crc.safa.features.github.entities.app.GithubResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;

import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class GithubControllerUtils {

    private static final Logger log = LoggerFactory.getLogger(GithubControllerUtils.class);

    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;

    public GithubResponseDTO<Boolean> checkCredentials(GithubAccessCredentials credentials) {
        // TODO this doesn't actually check the credentials
        return new GithubResponseDTO<>(true, GithubResponseDTO.GithubResponseMessage.OK);
    }
}
