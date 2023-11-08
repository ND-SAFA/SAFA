package edu.nd.crc.safa.features.github.entities.db;

import java.util.Date;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.OneToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "github_project")
@Data
@NoArgsConstructor
public class GithubProject {

    /**
     * Uniquely identifies the mapping
     */
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "mapping_id")
    private UUID id;

    /**
     * ID of associated safa project
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "safa_project_id", nullable = false)
    private Project project;

    /**
     * Repository name
     */
    @Column(name = "owner", nullable = false)
    private String owner;

    /**
     * Repository name
     */
    @Column(name = "repository_name", nullable = false)
    private String repositoryName;

    /**
     * GitHub branch used to pull the artifacts
     */
    @Column(name = "branch", nullable = false, length = 32)
    private String branch;

    /**
     * Latest commit sha used to pull artifacts
     */
    @Column(name = "last_commit_sha", length = 64)
    private String lastCommitSha;

    /**
     * Timestamp of the last update
     */
    @Column(name = "last_update", nullable = false)
    private Date lastUpdate = new Date();

    @Column(name = "include", nullable = false, columnDefinition = "mediumtext")
    @Lob
    private String include = "**";

    @Column(name = "exclude", nullable = false, columnDefinition = "mediumtext")
    @Lob
    private String exclude = "";

    @OneToOne
    @OnDelete(action = OnDeleteAction.NO_ACTION)
    @JoinColumn(name = "artifact_type_id", nullable = false)
    private ArtifactType artifactType;

    @PreUpdate
    @PrePersist
    public void updateTimeStamps() {
        this.lastUpdate = new Date();
    }
}
