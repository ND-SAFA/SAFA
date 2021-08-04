package edu.nd.crc.safa.entities;

import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "saved_layouts")
public class Layout {

    @Id
    @Column(name = "layout_id")
    @GeneratedValue
    UUID layoutId;


    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @Column
    String hash;

    @Column
    private String data;

    public Layout(Project project, String hash, String data) {
        this.project = project;
        this.hash = hash;
        this.data = data;
    }

    public String getData() {
        return this.data;
    }
}
