package edu.nd.crc.safa.features.github.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;
import jakarta.persistence.Version;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;


/**
 * Data required to access the GitHub api on behalf of an existing user
 */
@Entity
@Table(name = "github_access_credentials")
@Data
@NoArgsConstructor
public class GithubAccessCredentials {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "artifact_id")
    private UUID id;

    @Version
    private Short version;

    @Column(name = "access_token", length = 64)
    private String accessToken;

    @Transient
    private String clientSecret;

    @Transient
    private String clientId;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = SafaUser.ID_COLUMN, nullable = false)
    private SafaUser user;

    /**
     * GitHub account username associated with the credentials.
     * Required by some GitHub API endpoints
     */
    private String githubHandler;

}
