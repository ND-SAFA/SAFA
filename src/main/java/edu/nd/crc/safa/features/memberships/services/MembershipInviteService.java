package edu.nd.crc.safa.features.memberships.services;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.entities.db.MembershipInviteToken;
import edu.nd.crc.safa.features.memberships.entities.db.TokenUses;
import edu.nd.crc.safa.features.memberships.repositories.MembershipInviteTokenRepository;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.exception.InvalidTokenException;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class MembershipInviteService {

    private final MembershipInviteTokenRepository tokenRepo;
    private final MembershipService membershipService;

    /**
     * Generate a new invite token
     *
     * @param entity The entity to invite to
     * @param role The role for the new user
     * @param uses The number of uses for the token
     * @param asUser The user doing the sharing
     * @return The generated token
     */
    public MembershipInviteToken generateSharingToken(IEntityWithMembership entity, IRole role, TokenUses uses,
                                                      SafaUser asUser) {
        membershipService.requireEditMembersPermission(entity, asUser);
        return generateSharingTokenNoPermissionCheck(entity, role, uses);
    }

    /**
     * Generate a new invite token
     *
     * @param entityId The id of the entity to invite to
     * @param roleName The role for the new user
     * @param uses The number of uses for the token
     * @param asUser The user doing the sharing
     * @return The generated token
     */
    public MembershipInviteToken generateSharingToken(UUID entityId, String roleName, TokenUses uses, SafaUser asUser) {
        IEntityWithMembership entity = membershipService.getEntity(entityId);
        IRole role = membershipService.getRoleForEntity(entity, roleName);
        return generateSharingToken(entity, role, uses, asUser);
    }

    /**
     * Generate a new invite token without doing a permission check
     *
     * @param entity The entity to invite to
     * @param role The role for the new user
     * @param uses The number of uses for the token
     * @return The generated token
     */
    public MembershipInviteToken generateSharingTokenNoPermissionCheck(IEntityWithMembership entity, IRole role,
                                                                       TokenUses uses) {
        MembershipInviteToken token = new MembershipInviteToken(entity, role, uses);
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
            tokenRepo.delete(token);
            throw new InvalidTokenException();
        }

        IEntityWithMembership entity = membershipService.getEntity(token.getEntityId());
        IRole role = membershipService.getRoleForEntity(entity, token.getRole());
        IEntityMembership membership = membershipService.createMembership(user, entity, role);

        if (token.getUses() == TokenUses.SINGLE) {
            tokenRepo.delete(token);
        }

        return membership;
    }

    /**
     * Use a generated invite token to create a new membership
     *
     * @param tokenId The token
     * @param user The user
     * @return The newly created membership
     */
    public IEntityMembership useToken(UUID tokenId, SafaUser user) {
        MembershipInviteToken token = tokenRepo.findById(tokenId).orElseThrow(InvalidTokenException::new);
        return useToken(token, user);
    }

    /**
     * Delete a token by its ID
     *
     * @param tokenId The ID of the token
     */
    public void deleteToken(UUID tokenId) {
        MembershipInviteToken token = tokenRepo.findById(tokenId).orElseThrow(InvalidTokenException::new);
        tokenRepo.delete(token);
    }
}