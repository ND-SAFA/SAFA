package edu.nd.crc.safa.features.memberships.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Joins each user to the project they are members in.
 */
@Entity
@Table(name = "project_membership",
    uniqueConstraints = {
        @UniqueConstraint(
            columnNames = {
                "project_id",
                "user_id"
            }, name = AppConstraints.SINGLE_ROLE_PER_PROJECT)
    })
@Data
@NoArgsConstructor
public class ProjectMembership implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "membership_id")
    UUID membershipId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false)
    Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "user_id",
        nullable = false)
    SafaUser member;

    @Column(name = "project_role")
    @Enumerated(EnumType.STRING)
    ProjectRole role;

    public ProjectMembership(Project project, SafaUser member, ProjectRole role) {
        this.project = project;
        this.member = member;
        this.role = role;
    }
}
