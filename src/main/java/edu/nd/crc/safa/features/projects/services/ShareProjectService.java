package edu.nd.crc.safa.features.projects.services;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ShareProjectToken;
import edu.nd.crc.safa.features.projects.repositories.ShareProjectTokenRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.exception.ExpiredTokenException;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ShareProjectService {

    private final ShareProjectTokenRepository tokenRepo;
    private final ProjectMembershipService projectMembershipService;

    /**
     * Generate a new project sharing token
     *
     * @param project The project to share
     * @param role The role for the new user
     * @return The generated token
     */
    public ShareProjectToken generateSharingToken(Project project, ProjectRole role) {
        ShareProjectToken token = new ShareProjectToken(project, role);
        return tokenRepo.save(token);
    }

    /**
     * Use a generated project sharing token to share a project with a user
     *
     * @param token The token
     * @param user The user
     */
    public void useToken(ShareProjectToken token, SafaUser user) {
        if (token.getExpiration().isBefore(LocalDateTime.now())) {
            throw new ExpiredTokenException(token.getExpiration());
        }
        projectMembershipService.addUserRole(user, token.getProject(), token.getRole());
    }

    /**
     * Use a generated project sharing token to share a project with a user
     *
     * @param tokenId The token
     * @param user The user
     */
    public void useToken(UUID tokenId, SafaUser user) {
        ShareProjectToken token = tokenRepo.findById(tokenId)
                .orElseThrow(() -> new SafaItemNotFoundError("No token with the given ID found"));
        useToken(token, user);
    }
}