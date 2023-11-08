package edu.nd.crc.safa.features.users.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the application side view of an account.
 */
@NoArgsConstructor
@Data
public class UserAppEntity implements IUser {
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

    @Override
    public boolean equals(Object object) {
        if (object instanceof UserAppEntity otherUser) {
            return otherUser.getUserId().equals(this.userId);
        }
        return false;
    }

    @Override
    public int hashCode() {
        return this.userId.hashCode();
    }
}
