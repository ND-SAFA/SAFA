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
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Represent a token for user email verification
 */
@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "email_verification_token")
public class EmailVerificationToken {

    /**
     * Uniquely identifies the user token.
     */
    @JdbcTypeCode(SqlTypes.BINARY)
    @Id
    @GeneratedValue
    @Column
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

    public EmailVerificationToken(@NonNull SafaUser user,
                                  @NonNull String token,
                                  @NonNull Date expirationDate) {
        this.user = user;
        this.token = token;
        this.expirationDate = expirationDate;
    }

}
