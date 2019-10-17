package edu.nd.crc.safa.domain;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import org.neo4j.ogm.annotation.GeneratedValue;
import org.neo4j.ogm.annotation.Id;
import org.neo4j.ogm.annotation.NodeEntity;
import org.neo4j.ogm.annotation.Relationship;

@NodeEntity
public class Artifact {

  @Id
  @GeneratedValue
  private Long id;

  private String name;
	private String root;
	private String DATA;
	private String tag;

	@JsonIgnoreProperties("artifact")
	@Relationship(type = "CONSTRAINT_OF", direction = Relationship.INCOMING)
	private List<ArtifactConstraint> constraints;

	public Artifact() {
	}

	public Artifact(String name, String root, String DATA, String tag) {
    this.name = name;
		this.root = root;
		this.DATA = DATA;
		this.tag = tag;
	}

	public Long getId() {
		return id;
	}

  public String getName() {
		return name;
  }
  
	public String getRoot() {
		return root;
	}

	public String getData() {
		return DATA;
	}

	public String getTag() {
		return tag;
	}

	public List<ArtifactConstraint> getConstraints() {
		return constraints;
	}

	public void addConstraint(ArtifactConstraint constraint) {
		if (this.constraints == null) {
			this.constraints = new ArrayList<ArtifactConstraint>();
    }
    this.constraints.add(constraint);
	}
}