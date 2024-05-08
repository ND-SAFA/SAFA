package edu.nd.crc.safa.features.memberships.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.FendPathConfig;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.email.services.EmailService;
import edu.nd.crc.safa.features.memberships.entities.app.InviteTokenDTO;
import edu.nd.crc.safa.features.memberships.entities.db.MembershipInviteToken;
import edu.nd.crc.safa.features.memberships.services.MembershipInviteService;
import edu.nd.crc.safa.features.memberships.services.MembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MembershipInviteController extends BaseController {

    private final MembershipInviteService inviteService;
    private final FendPathConfig fendPathConfig;
    private final EmailService emailService;
    private final MembershipService membershipService;

    public MembershipInviteController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                      MembershipInviteService inviteService, FendPathConfig fendPathConfig,
                                      EmailService emailService, MembershipService membershipService) {
        super(resourceBuilder, serviceProvider);
        this.inviteService = inviteService;
        this.fendPathConfig = fendPathConfig;
        this.emailService = emailService;
        this.membershipService = membershipService;
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
    public InviteTokenDTO createInvite(@PathVariable UUID entityId, @RequestBody InviteRequestDTO inviteRequest) {
        SafaUser user = getCurrentUser();

        MembershipInviteToken token = inviteService.generateSharingToken(entityId, inviteRequest.getRole(), user);
        InviteTokenDTO tokenResponse = new InviteTokenDTO(token, fendPathConfig.getAcceptInviteUrl());

        String email = inviteRequest.getEmail();
        if (email != null && !email.isBlank()) {
            IEntityWithMembership entity = membershipService.getEntity(entityId);
            emailService.sendMembershipInvite(email, entity, token);
        }

        return tokenResponse;
    }

    /**
     * Accept an invite
     *
     * @param token The token associated with the invite
     * @return The new membership that was created
     */
    @PutMapping(AppRoutes.Memberships.Invites.ACCEPT_INVITE)
    public MembershipAppEntity acceptInvite(@RequestParam UUID token) {
        SafaUser user = getCurrentUser();
        return new MembershipAppEntity(inviteService.useToken(token, user));
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
    public static class InviteRequestDTO {
        @NotNull
        @NotEmpty
        private String role;
        private String email;
    }
}
