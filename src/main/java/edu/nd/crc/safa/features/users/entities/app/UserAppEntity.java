package edu.nd.crc.safa.features.users.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;

/**
 * Represents the application side view of an account.
 */
@Data
public class UserAppEntity {

    UUID userId;
    String email;
    
    public UserAppEntity(SafaUser safaUser) {
        this.userId = safaUser.getUserId();
        this.email = safaUser.getEmail();
    }
}
