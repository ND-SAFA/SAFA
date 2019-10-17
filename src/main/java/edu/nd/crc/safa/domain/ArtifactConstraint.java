package edu.nd.crc.safa.domain;
  
import org.neo4j.ogm.annotation.*;

@RelationshipEntity(type = "CONSTRAINT_OF")
public class ArtifactConstraint {

  @Id
  @GeneratedValue
  private Long id;

  private String type;
  
	@StartNode
	private Artifact constraint;

	@EndNode
	private Artifact artifact;

	public ArtifactConstraint() {
	}

	public ArtifactConstraint(Artifact artifact, Artifact constraint) {
		this.artifact = artifact;
		this.constraint = constraint;
	}

	public Long getId() {
	    return id;
	}

	public String getType() {
	    return type;
	}

	public Artifact getConstraint() {
	    return constraint;
	}

	public Artifact getArtifact() {
	    return artifact;
	}

  public void setType(String type) {
      this.type = type;
  }
}