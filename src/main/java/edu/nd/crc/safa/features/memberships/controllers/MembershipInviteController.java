package edu.nd.crc.safa.features.memberships.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.app.InviteTokenAppEntity;
import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.entities.db.MembershipInviteToken;
import edu.nd.crc.safa.features.memberships.services.MembershipInviteService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MembershipInviteController extends BaseController {

    private final MembershipInviteService inviteService;

    @Value("${fend.accept-invite-path}")
    private String acceptInvitePath;

    public MembershipInviteController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                      MembershipInviteService inviteService) {
        super(resourceBuilder, serviceProvider);
        this.inviteService = inviteService;
    }

    /**
     * Create a project invite token. If an email is provided, the link to accept the invite will
     * be sent to the email.
     *
     * @param entityId ID of the entity the new membership will be a part of
     * @param inviteRequest Details about the request
     * @return A generated invite token
     */
    @PostMapping(AppRoutes.Memberships.Invites.BY_ENTITY_ID)
    public InviteTokenAppEntity createInvite(@PathVariable UUID entityId, @RequestBody InviteRequest inviteRequest) {
        SafaUser user = getCurrentUser();

        MembershipInviteToken token = inviteService.generateSharingToken(entityId, inviteRequest.getRole(), user);
        InviteTokenAppEntity tokenResponse = new InviteTokenAppEntity(token, acceptInvitePath);

        // TODO send email

        return tokenResponse;
    }

    /**
     * Accept an invite
     *
     * @param token The token associated with the invite
     * @return The new membership that was created
     */
    @PutMapping(AppRoutes.Memberships.Invites.ACCEPT_INVITE)
    public IEntityMembership acceptInvite(@RequestParam UUID token) {
        SafaUser user = getCurrentUser();
        return inviteService.useToken(token, user);
    }

    /**
     * Decline an invite
     *
     * @param token The token associated with the invite
     */
    @PutMapping(AppRoutes.Memberships.Invites.DECLINE_INVITE)
    public void declineInvite(@RequestParam UUID token) {
        inviteService.deleteToken(token);
    }

    @Data
    public static class InviteRequest {
        @NotNull
        @NotEmpty
        private String role;
        private String email;
    }
}
