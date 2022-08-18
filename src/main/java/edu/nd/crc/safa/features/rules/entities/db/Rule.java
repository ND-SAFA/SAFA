package edu.nd.crc.safa.features.rules.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.rules.entities.app.RuleAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
    @Type(type = "uuid-char")
    @Column(name = "id")
    UUID id;
    /**
     * The project this rule is applied to.
     */
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id", nullable = false)
    Project project;
    /**
     * The name of the rule.
     */
    @Column
    String name;
    /**
     * Description of what the rule does.
     */
    String description;
    /**
     * The rule in String format.
     */
    @Column
    String rule;

    public Rule(Project project,
                RuleAppEntity rule) {
        this.project = project;
        this.name = rule.getName();
        this.description = rule.getDescription();
        this.rule = rule.toString();
    }
}
