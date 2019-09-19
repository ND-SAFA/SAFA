package edu.nd.crc.safa.models;

// import com.fasterxml.jackson.databind.util.JSONPObject;

import org.neo4j.ogm.annotation.GeneratedValue;
import org.neo4j.ogm.annotation.Id;
import org.neo4j.ogm.annotation.NodeEntity;

@NodeEntity
public class HazardTree {

	@Id @GeneratedValue private Long id;

	private String name;
	private String structure;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getStructure() {
		return structure;
	}

	public void setStructure(String structure) {
		this.structure = structure;
	}
}