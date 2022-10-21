package edu.nd.crc.safa.features.github.services;

import java.util.List;

import edu.nd.crc.safa.features.github.entities.app.GithubAccessCredentialsDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubCommitDiffResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubFileBlobDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRefreshTokenDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryBranchDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFiletreeResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;

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

    /**
     * @param credentials User credentials
     * @param url         Blob location. Format should be:
     *                    https://api.github.com/repos/{username}/{repo}/git/blobs/{file_sha}
     *                    URL can be constructed manually, or it can be provided in the filetree
     *                    response for each file.
     * @return Information blob information for the url provided.
     */
    GithubFileBlobDTO getBlobInformation(GithubAccessCredentials credentials, String url);

    /**
     * @param accessCode Code retrieved from FEND after user has authorized our application
     * @return Set of GitHub credentials that will be saved for later use.
     */
    GithubAccessCredentialsDTO useAccessCode(String accessCode);
}
