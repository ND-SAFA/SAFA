package edu.nd.crc.safa.features.users.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.IUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

/**
 * The model for our users.
 */
@Entity
@Table(name = "safa_user")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SafaUser implements Serializable, IUser {

    public static final String ID_COLUMN = "user_id";

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = ID_COLUMN)
    private UUID userId;

    @Column(name = "email", nullable = false, unique = true)
    private String email;

    @Column(name = "password", nullable = false)
    private String password;

    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID personalOrgId;

    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID defaultOrgId;

    @Column
    private boolean superuser;

    @Column
    private boolean verified;

    public SafaUser(String email, String password) {
        this.email = email;
        this.password = password;
        this.superuser = false;
        this.verified = false;
    }

    @Override
    public boolean equals(Object object) {
        if (object instanceof SafaUser user) {
            return user.getUserId().equals(this.userId);
        }
        return false;
    }

    @Override
    public int hashCode() {
        return this.userId.hashCode();
    }
}
