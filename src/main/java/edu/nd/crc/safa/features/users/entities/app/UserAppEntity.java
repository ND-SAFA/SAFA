package edu.nd.crc.safa.features.users.entities.app;

import java.util.UUID;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the application side view of an account.
 */
@NoArgsConstructor
@Data
public class UserAppEntity {
    /**
     * Unique identifier for user.
     */
    @NotNull
    private UUID userId;

    /**
     * User's email.
     */
    @NotNull
    @NotEmpty
    private String email;

    public UserAppEntity(SafaUser safaUser) {
        this.userId = safaUser.getUserId();
        this.email = safaUser.getEmail();
    }
}
