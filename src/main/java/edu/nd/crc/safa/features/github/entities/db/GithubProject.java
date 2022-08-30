package edu.nd.crc.safa.features.github.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "github_project")
@Data
@NoArgsConstructor
@RequiredArgsConstructor
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
    @NonNull
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "safa_project_id", nullable = false)
    private Project project;

    /**
     * Repository name
     *
     * {@link NonNull} annotated properties are included in the constructor
     * by {@link RequiredArgsConstructor}
     */
    @NonNull
    @Column(name = "repository_name", nullable = false)
    private String repositoryName;

    /**
     * GitHub branch used to pull the artifacts
     */
    @NonNull
    @Column(name = "branch", nullable = false, length = 32)
    private String branch;

    /**
     * Latest commit sha used to pull artifacts
     */
    @NonNull
    @Column(name = "last_commit_sha", length = 64)
    private String lastCommitSha;

    /**
     * User that created the project
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = SafaUser.ID_COLUMN, nullable = false)
    private SafaUser user;
}
