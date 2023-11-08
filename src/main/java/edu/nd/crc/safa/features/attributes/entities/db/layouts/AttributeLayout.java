package edu.nd.crc.safa.features.attributes.entities.db.layouts;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "attribute_layout")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
@AllArgsConstructor
public class AttributeLayout {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private UUID id;

    @Column
    private String name;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;
}
