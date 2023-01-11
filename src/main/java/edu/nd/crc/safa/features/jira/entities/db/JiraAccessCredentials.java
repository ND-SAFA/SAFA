package edu.nd.crc.safa.features.jira.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.persistence.Version;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;


/**
 * Data required to access the JIRA api for a user on an JIRA application identified by its cloud id
 */
@Entity
@Table(name = "jira_access_credentials")
@Data
public class JiraAccessCredentials {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "artifact_id")
    private UUID id;

    @Version
    private Short version;

    @Lob
    @Column(name = "bearer_access_token", columnDefinition = "BLOB", length = 2048)
    private byte[] bearerAccessToken;

    @Column(name = "client_secret", length = 64)
    private String clientSecret;

    @Column(name = "client_id", length = 32)
    private String clientId;

    @Lob
    @Column(name = "refresh_token", columnDefinition = "mediumtext")
    private String refreshToken;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = SafaUser.ID_COLUMN, nullable = false)
    private SafaUser user;

}
