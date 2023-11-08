package edu.nd.crc.safa.features.attributes.entities.db.definitions;

import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "float_attribute")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class FloatAttributeInfo {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private UUID id;

    @Column(nullable = false)
    private double min;

    @Column(nullable = false)
    private double max;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "attribute_id", nullable = false)
    private CustomAttribute attribute;

    public FloatAttributeInfo(CustomAttribute attribute, double min, double max) {
        this.attribute = attribute;
        this.min = min;
        this.max = max;
    }

}
