package edu.nd.crc.safa.server.accounts;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import lombok.Data;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Represents list of tokens used to reset user password
 */
@Entity
@Table(name = "password_reset_token")
@Data
public class PasswordResetToken {

    private static final int EXPIRATION = 60 * 24;

    /**
     * Uniquely identifies the user token.
     */
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "id")
    private UUID id;

    /**
     * The user associated with the reset token.
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private SafaUser user;

    /**
     * The token used to verify the identity of the user.
     */
    @Column
    private String token;

    public PasswordResetToken(SafaUser user, String token) {
        this.user = user;
        this.token = token;
    }
}
