package edu.nd.crc.safa.features.rules.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.entities.app.RuleAppEntity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Data
@Entity
@Table(name = "project_rule")
@NoArgsConstructor
public class Rule {
    /**
     * Unique id for each rule.
     */
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "id")
    private UUID id;
    /**
     * The project this rule is applied to.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;
    /**
     * The name of the rule.
     */
    @Column
    private String name;
    /**
     * Description of what the rule does.
     */
    private String description;
    /**
     * The rule in String format.
     */
    @Column
    private String rule;

    public Rule(Project project,
                RuleAppEntity rule) {
        this.project = project;
        this.name = rule.getName();
        this.description = rule.getDescription();
        this.rule = rule.toString();
    }
}
