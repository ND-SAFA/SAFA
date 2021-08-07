package edu.nd.crc.safa.entities;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "saved_layouts")
public class Layout {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "layout_id")
    UUID layoutId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @Column
    String treeId;

    @Column
    private String data;

    public Layout(Project project, String treeId, String data) {
        this.project = project;
        this.treeId = treeId;
        this.data = data;
    }

    public String getData() {
        return this.data;
    }
}
