package edu.nd.crc.safa.server.entities.db;

import java.util.UUID;

import javax.persistence.*;

import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "jira_access_credentials")
@Getter
@Setter
public class JiraAccessCredentials {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "artifact_id")
    private UUID id;

    @Version
    private Short version;

    @Column(name = "cloud_id", length = 64)
    private String cloudId;

    @Lob
    @Column(name = "bearer_access_token", columnDefinition = "BLOB", length = 2048)
    private byte[] bearerAccessToken;

    @Column(name = "client_secret", length = 64)
    private String clientSecret;

    @Column(name = "client_id", length = 32)
    private String clientId;

    @Column(name = "refresh_token", length = 128)
    private String refreshToken;

    @OneToOne
    @JoinColumn(name = SafaUser.ID_COLUMN, nullable = false)
    private SafaUser user;

}
