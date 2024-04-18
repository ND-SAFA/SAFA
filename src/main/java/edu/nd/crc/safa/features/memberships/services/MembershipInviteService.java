package edu.nd.crc.safa.features.memberships.services;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.entities.db.MembershipInviteToken;
import edu.nd.crc.safa.features.memberships.repositories.MembershipInviteTokenRepository;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.exception.ExpiredTokenException;

import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.NotImplementedException;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class MembershipInviteService {

    private final MembershipInviteTokenRepository tokenRepo;

    /**
     * Generate a new invite token
     *
     * @param entity The entity to invite to
     * @param role The role for the new user
     * @return The generated token
     */
    public MembershipInviteToken generateSharingToken(IEntityWithMembership entity, IRole role) {
        MembershipInviteToken token = new MembershipInviteToken(entity, role);
        return tokenRepo.save(token);
    }

    /**
     * Use a generated invite token to create a new membership
     *
     * @param token The token
     * @param user The user
     * @return The newly created membership
     */
    public IEntityMembership useToken(MembershipInviteToken token, SafaUser user) {
        if (token.getExpiration().isBefore(LocalDateTime.now())) {
            throw new ExpiredTokenException(token.getExpiration());
        }

        // TODO add membership
        throw new NotImplementedException();
    }

    /**
     * Use a generated invite token to create a new membership
     *
     * @param tokenId The token
     * @param user The user
     * @return The newly created membership
     */
    public IEntityMembership useToken(UUID tokenId, SafaUser user) {
        MembershipInviteToken token = tokenRepo.findById(tokenId)
                .orElseThrow(() -> new SafaItemNotFoundError("No token with the given ID found"));
        return useToken(token, user);
    }
}