package edu.nd.crc.safa.features.github.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.persistence.Transient;
import javax.persistence.Version;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;


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
    @Type(type = "uuid-char")
    @Column(name = "artifact_id")
    private UUID id;

    @Version
    private Short version;

    @Column(name = "access_token", length = 64)
    private String  accessToken;

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
