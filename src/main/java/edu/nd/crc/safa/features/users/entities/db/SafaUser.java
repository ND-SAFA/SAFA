package edu.nd.crc.safa.features.users.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.Type;

/**
 * The model for our users.
 */
@Entity
@Table(name = "safa_user")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SafaUser implements Serializable {

    public static final String ID_COLUMN = "user_id";

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = ID_COLUMN)
    private UUID userId;

    @Column(name = "email", nullable = false, unique = true)
    private String email;

    @Column(name = "password", nullable = false)
    private String password;

    @Column
    private UUID personalOrgId;

    @Column
    private boolean superuser;

    public SafaUser(String email, String password) {
        this.email = email;
        this.password = password;
        this.superuser = false;
    }
}
