package edu.nd.crc.safa.features.users.entities.db;

import java.util.Date;
import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Represents list of tokens used to reset user password
 */
@Data
@NoArgsConstructor
@Entity
@Table(name = "password_reset_token")
public class PasswordResetToken {

    /**
     * Uniquely identifies the user token.
     */
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "id", columnDefinition = "VARCHAR(36)")
    private UUID id;

    /**
     * The user associated with the reset token.
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @JoinColumn(name = "user_id", nullable = false, columnDefinition = "VARCHAR(36)")
    @NonNull
    private SafaUser user;

    /**
     * The token used to verify the identity of the user.
     */
    @Column(nullable = false)
    @NonNull
    private String token;

    @Column(name = "expiration_date", nullable = false)
    @NonNull
    private Date expirationDate;

    public PasswordResetToken(@NonNull SafaUser user,
                              @NonNull String token,
                              @NonNull Date expirationDate) {
        this.user = user;
        this.token = token;
        this.expirationDate = expirationDate;
    }

}
