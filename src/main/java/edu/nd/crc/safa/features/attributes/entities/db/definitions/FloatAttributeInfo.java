package edu.nd.crc.safa.features.attributes.entities.db.definitions;

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
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "float_attribute")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class FloatAttributeInfo {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
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
