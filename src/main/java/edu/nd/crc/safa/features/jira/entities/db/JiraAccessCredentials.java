package edu.nd.crc.safa.features.jira.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;
import jakarta.persistence.Version;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;


/**
 * Data required to access the JIRA api for a user on an JIRA application identified by its cloud id
 */
@Entity
@Table(name = "jira_access_credentials")
@Data
public class JiraAccessCredentials {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "artifact_id")
    private UUID id;

    @Version
    private Short version;

    @Lob
    @Column(name = "bearer_access_token", columnDefinition = "BLOB", length = 2048)
    private byte[] bearerAccessToken;

    @Transient
    private String clientSecret;

    @Transient
    private String clientId;

    @Lob
    @Column(name = "refresh_token", columnDefinition = "mediumtext")
    private String refreshToken;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = SafaUser.ID_COLUMN, nullable = false)
    private SafaUser user;

}
