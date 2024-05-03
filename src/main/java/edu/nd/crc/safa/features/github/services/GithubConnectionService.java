package edu.nd.crc.safa.features.github.services;

import java.util.Optional;

import edu.nd.crc.safa.features.github.entities.app.GithubAccessCredentialsDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubCommitDiffResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubFileBlobDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFiletreeResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

public interface GithubConnectionService {

    /**
     * Gets access credentials for the given user.
     *
     * @param user The safa user to look up credentials for
     * @return The user's github credentials, if they exist
     */
    Optional<GithubAccessCredentials> getGithubCredentials(SafaUser user);

    /**
     * Deletes stored credentials for a given user
     *
     * @param user The user
     */
    void deleteGithubCredentials(SafaUser user);

    /**
     * @param credentials User credentials
     * @return GitHub handler from the credentials
     */
    GithubSelfResponseDTO getSelf(GithubAccessCredentials credentials);

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
     * @param credentials     User credentials
     * @param repositoryOwner Repository owner
     * @param repositoryName  Repository name
     * @param baseCommitSha   Commit checkpoint
     * @param branchName      Branch name
     * @return Diff between the base commit and named branch.
     */
    GithubCommitDiffResponseDTO getDiffBetweenOldCommitAndHead(GithubAccessCredentials credentials,
                                                               String repositoryOwner,
                                                               String repositoryName,
                                                               String baseCommitSha,
                                                               String branchName);

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
