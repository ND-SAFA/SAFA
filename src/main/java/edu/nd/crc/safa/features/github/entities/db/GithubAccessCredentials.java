package edu.nd.crc.safa.features.github.entities.db;

import java.time.LocalDateTime;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.PrePersist;
import javax.persistence.PreUpdate;
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

    @Column(name = "refresh_token", length = 128)
    private String refreshToken;

    @Transient
    private String clientSecret;

    @Transient
    private String clientId;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = SafaUser.ID_COLUMN, nullable = false)
    private SafaUser user;

    /**
     * In how many seconds the access token will expire
     */
    @Transient
    private Integer accessTokenExpiration;


    /**
     * In how many seconds the refresh token will expire
     * i.e. in how many minutes the credentials are useless
     *      and should be deleted
     */
    @Transient
    private Integer refreshTokenExpiration;

    /**
     * Computed after loading the entity.
     */
    @Column(name = "access_token_expiration_date")
    private LocalDateTime accessTokenExpirationDate;

    /**
     * Computed after loading the entity. Not persisted
     */
    @Column(name = "refresh_token_expiration_date")
    private LocalDateTime refreshTokenExpirationDate;

    /**
     * GitHub account username associated with the credentials.
     * Required by some GitHub API endpoints
     */
    private String githubHandler;

    public boolean isTokenExpired() {
        return this.accessTokenExpirationDate.isBefore(LocalDateTime.now());
    }

    public boolean areCredentialsExpired() {
        return this.refreshTokenExpirationDate.isBefore(LocalDateTime.now());
    }

    @PrePersist
    @PreUpdate
    public void updateExpirationDates() {
        if (this.refreshTokenExpiration != null) {
            this.refreshTokenExpirationDate = LocalDateTime.now().plusSeconds(this.refreshTokenExpiration);
        }

        if (this.accessTokenExpiration != null) {
            this.accessTokenExpirationDate = LocalDateTime.now().plusSeconds(this.accessTokenExpiration);
        }
    }

}
