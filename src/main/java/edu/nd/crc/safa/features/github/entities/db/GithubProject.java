package edu.nd.crc.safa.features.github.entities.db;

import java.util.Date;
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

import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
    @Type(type = "uuid-char")
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

    @PreUpdate
    @PrePersist
    public void updateTimeStamps() {
        this.lastUpdate = new Date();
    }
}
