package edu.nd.crc.safa.features.github.services;

import javax.annotation.PostConstruct;

import java.util.Collections;

import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;

import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class GitHubTests {

    private static final Logger log = LoggerFactory.getLogger(GitHubTests.class);

    private GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private GithubConnectionService githubConnectionService;
    private SafaUserRepository safaUserRepository;
    private GithubProjectRepository githubProjectRepository;

    @PostConstruct
    public void init() {
        log.info("Init GitHub tests");
//        this.do_stuff();
    }

    private void do_stuff() {
        GithubAccessCredentials githubAccessCredentials = create();
//        GithubRefreshTokenDTO dto = githubConnectionService.refreshAccessToken(githubAccessCredentials);

//        log.info(dto.toString());
//        GithubRefreshTokenDTO refreshTokenDTO = githubConnectionService.refreshAccessToken(githubAccessCredentials);
//
//        if (refreshTokenDTO.getError() != null) {
//            log.error(refreshTokenDTO.getError());
//            return;
//        }
//
//        log.info("Refreshing existing credentials...");
//        log.info(refreshTokenDTO.toString());
//
//        githubAccessCredentials.setAccessToken(refreshTokenDTO.getAccessToken());
//        githubAccessCredentials.setRefreshToken(refreshTokenDTO.getRefreshToken());
//        githubAccessCredentials.setAccessTokenExpiration(refreshTokenDTO.getAccessTokenExpiration());
//        githubAccessCredentials.setRefreshTokenExpiration(refreshTokenDTO.getRefreshTokenExpiration());
//        githubAccessCredentials = githubAccessCredentialsRepository.save(githubAccessCredentials);

        log.info("Checking credentials because why not...");
        log.info(String.valueOf(githubConnectionService.getSelf(githubAccessCredentials)));

//        log.info("Getting user repositories...");
//        githubConnectionService.getUserRepositories(githubAccessCredentials).forEach(p -> {
//            log.info(p.toString());
//        });
//
//        log.info("_________________________________________________________________________");
//        log.info(githubConnectionService
//                .getUserRepository(githubAccessCredentials, "home_assistant_ro").toString());
//        log.info("_________________________________________________________________________");
//
//        log.info("Getting repository branches...");
//        githubConnectionService.getRepositoryBranches(
//                githubAccessCredentials,
//                "home_assistant_ro"
//        ).forEach(p -> {
//            log.info(p.toString());
//        });
//
//        log.info("Getting repository filetree...");
//        githubConnectionService.getRepositoryFiles(
//                githubAccessCredentials,
//                "home_assistant_ro",
//                "6f2aa95d8fdf1b4205d56b4fd41cc5474821f45d"
//        ).getTree().forEach(p -> {
//            log.info(p.toString());
//            log.info(githubConnectionService.getBlobInformation(create(), p.getBlobApiUrl()).toString());
//        });

//        log.info("Getting diff...");
//        githubConnectionService.getDiffBetweenOldCommitAndHead(
//                githubAccessCredentials,
//                "home_assistant_ro",
//                "3df1b2c2f6e20e36d02e52b07af76da040c207b4"
//        ).getFiles().forEach(p -> {
//            log.info(p.toString());
//        });

        GithubProject githubProject = githubProjectRepository.findByRepositoryName("Term-Rewriting-System")
            .orElseThrow(() -> new RuntimeException("TSR project missing"));

        githubConnectionService.getDiffBetweenOldCommitAndHead(
            githubAccessCredentials,
            githubProject.getRepositoryName(),
            githubProject.getLastCommitSha()
        ).getFiles().forEach(file -> {
            log.info(file.toString());
        });

        log.info(String.join("", Collections.nCopies(52, "_")));
    }

    protected GithubAccessCredentials create() {
        if (githubAccessCredentialsRepository.findAll().size() > 0) {
            return githubAccessCredentialsRepository.findAll().get(0);
        }

        throw new SafaError("No credentials");

//        String email = "marcuspopb@gmail.com";
//        SafaUser user = safaUserRepository.findByEmail(email).orElseThrow(() ->
//                new UnsupportedOperationException("no user"));
//        GithubAccessCredentials credentials = new GithubAccessCredentials();
//
//        credentials.setAccessToken("ghu_XcfyGXWLrrAaYLIqAdEbkdteqYlS1R2kmeJN");
//        credentials.setRefreshToken("ghr_Mw5NRf3MsDT5EjrMcKGalS8gL6J0vHbMNVvtGBpQYo00RP8WxeRBL6gtspLMnqbi7mNVa63vYVxZ");
//        credentials.setAccessTokenExpiration(28800);
//        credentials.setRefreshTokenExpiration(15897600);
//        credentials.setClientId("Iv1.f60cdb6afacc204e");
//        credentials.setClientSecret("d4c536e2ca759eea67990cfb1360f05b619c4409");
//        credentials.setGithubHandler("MarcusGitAccount");
//        credentials.setUser(user);
//
//        return githubAccessCredentialsRepository.save(credentials);
    }
}
