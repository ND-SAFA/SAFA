package edu.nd.crc.safa.features.memberships.entities.app;

import java.time.LocalDateTime;

import edu.nd.crc.safa.features.memberships.entities.db.MembershipInviteToken;

import lombok.Data;

@Data
public class InviteTokenAppEntity {
    private String token;
    private LocalDateTime expiration;
    private String url;

    public InviteTokenAppEntity(MembershipInviteToken token, String urlPathFormat) {
        this.token = token.getId().toString();
        this.expiration = token.getExpiration();
        this.url = String.format(urlPathFormat, this.token);
    }
}
