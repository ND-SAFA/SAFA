package edu.nd.crc.safa.features.artifacts.entities.db.schema;

import java.util.Objects;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.Hibernate;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "float_field")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class FloatFieldInfo {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Column(nullable = false)
    private float min;

    @Column(nullable = false)
    private float max;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "schema_field_id", nullable = false)
    private CustomAttribute schemaField;

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) {
            return false;
        }
        FloatFieldInfo that = (FloatFieldInfo) o;
        return id != null && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
