package edu.nd.crc.safa.features.jira.entities.db;

import java.util.Date;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;


/**
 * Maps a Safa project to a Jira project
 */
@Entity
@Table(name = "jira_project")
@Data
@NoArgsConstructor
public class JiraProject {
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
     * ID of associated jira project
     */
    @Column(name = "jira_project_id", nullable = false)
    private Long jiraProjectId;

    @JdbcTypeCode(SqlTypes.BINARY)
    @Column(nullable = false)
    private UUID orgId;

    /**
     * Timestamp of the last update
     */
    @Column(name = "last_update", nullable = false)
    private Date lastUpdate = new Date();

    public JiraProject(Project project, UUID orgId, Long jiraProjectId) {
        this.project = project;
        this.orgId = orgId;
        this.jiraProjectId = jiraProjectId;
    }
}
