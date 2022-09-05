package edu.nd.crc.safa.features.users.entities.db;

import java.util.Date;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import lombok.NonNull;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Represents list of tokens used to reset user password
 */
@Entity
@Table(name = "password_reset_token")
public class PasswordResetToken {

    private static final int EXPIRATION = 60 * 60 * 24;

    /**
     * Uniquely identifies the user token.
     */
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "id", columnDefinition = "VARCHAR(36)")
    private UUID id;

    /**
     * The user associated with the reset token.
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @Type(type = "uuid-char")
    @JoinColumn(name = "user_id", nullable = false, unique = true, columnDefinition = "VARCHAR(36)")
    @NonNull
    private final SafaUser user;

    /**
     * The token used to verify the identity of the user.
     */
    @Column(nullable = false)
    @NonNull
    private final String token;

    @Column(name = "expiration_date", nullable = false)
    @NonNull
    private final Date expirationDate;

    public PasswordResetToken(SafaUser user,
                              String token,
                              Date expirationDate) {
        this.user = user;
        this.token = token;
        this.expirationDate = expirationDate;
    }

}
