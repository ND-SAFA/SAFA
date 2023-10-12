package edu.nd.crc.safa.features.memberships.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Joins each user to the project they are members in.
 */
@Entity
@Table(name = "user_project_membership",
    uniqueConstraints = {
        @UniqueConstraint(
            columnNames = {
                "project_id",
                "user_id"
            }, name = AppConstraints.SINGLE_ROLE_PER_PROJECT)
    })
@Data
@NoArgsConstructor
public class UserProjectMembership implements Serializable {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "membership_id")
    private UUID membershipId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false)
    private Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "user_id",
        nullable = false)
    private SafaUser member;

    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Enumerated(EnumType.STRING)
    @Column(name = "project_role")
    private ProjectRole role;

    public UserProjectMembership(Project project, SafaUser member, ProjectRole role) {
        this.project = project;
        this.member = member;
        this.role = role;
    }
}
