package edu.nd.crc.safa.server.entities.db;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

import javax.persistence.*;
import java.util.UUID;

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
    @JoinColumn(name = "safa_project_id", nullable = false, unique = true)
    private Project project;

    /**
     * ID of associated jira project
     *
     * {@link NonNull} annotated properties are included in the constructor
     * by {@link RequiredArgsConstructor}
     */
    @NonNull
    @Column(name = "github_project_id", nullable = false, unique = true)
    private Long githubProjectId;

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
    @Column(name = "last_commit_sha", nullable = false, length = 64)
    private String lastCommitSha;
}
