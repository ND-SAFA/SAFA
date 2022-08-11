package edu.nd.crc.safa.server.services.github;

import edu.nd.crc.safa.server.entities.api.github.*;
import edu.nd.crc.safa.server.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.server.entities.db.Project;

import java.util.List;

public interface GithubConnectionService {

    /**
     * @param credentials User credentials
     * @return GitHub handler from the credentials
     */
    GithubSelfResponseDTO getSelf(GithubAccessCredentials credentials);

    /**
     * Get new credentials based on old ones
     *
     * @param credentials The credentials to refresh.
     * @return Refreshed credentials.
     */
    GithubRefreshTokenDTO refreshAccessToken(GithubAccessCredentials credentials);

    /**
     * @param credentials User credentials
     * @return A list of available user repositories
     */
    List<GithubRepositoryDTO> getUserRepositories(GithubAccessCredentials credentials);

    /**
     * @param credentials User credentials
     * @param name        Repository name
     * @return Requested user repository
     */
    GithubRepositoryDTO getUserRepository(GithubAccessCredentials credentials, String name);

    /**
     * @param credentials    User credentials
     * @param repositoryName Repository name
     * @return A list of available branches for the given repository
     */
    List<GithubRepositoryBranchDTO> getRepositoryBranches(GithubAccessCredentials credentials,
                                                          String repositoryName);

    /**
     * @param credentials      User credentials
     * @param repositoryName   Repository name
     * @param repositoryBranch Repository branch
     * @return The requested branch info for the given repository
     */
    GithubRepositoryBranchDTO getRepositoryBranch(GithubAccessCredentials credentials,
                                                  String repositoryName,
                                                  String repositoryBranch);

    /**
     * @param credentials    User credentials
     * @param repositoryName Repository name
     * @param commitSha      Commit checkpoint
     * @return The file tree for the given repository
     */
    GithubRepositoryFiletreeResponseDTO getRepositoryFiles(GithubAccessCredentials credentials,
                                                           String repositoryName,
                                                           String commitSha);

    /**
     * @param credentials    User credentials
     * @param repositoryName Repository name
     * @param baseCommitSha  Commit checkpoint
     * @return Diff between the base commit and the master HEAD
     */
    GithubCommitDiffResponseDTO getDiffBetweenOldCommitAndHead(GithubAccessCredentials credentials,
                                                               String repositoryName,
                                                               String baseCommitSha);
}
