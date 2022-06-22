package edu.nd.crc.safa.server.entities.db;

import java.util.Date;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.hibernate.annotations.UpdateTimestamp;


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
    @Type(type = "uuid-char")
    @Column(name = "mapping_id")
    UUID id;
    /**
     * ID of associated safa project
     */
    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "safa_project_id", nullable = false, unique = true)
    Project project;
    /**
     * ID of associated jira project
     */
    @Column(name = "jira_project_id", nullable = false, unique = true)
    Long jiraProjectId;

    /**
     * Timestamp of the last update
     */
    @Column(name = "last_update", nullable = false)
    private Date lastUpdate = new Date();

    public JiraProject(Project project, Long jiraProjectId) {
        this.project = project;
        this.jiraProjectId = jiraProjectId;
    }
}
