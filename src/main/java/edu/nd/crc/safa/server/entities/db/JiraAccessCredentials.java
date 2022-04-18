package edu.nd.crc.safa.server.entities.db;


import java.util.UUID;

import javax.persistence.*;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.json.JSONObject;


@Entity
@Table(name = "jira_access_credentials")
public class JiraAccessCredentials {

	@Id
	@GeneratedValue
	@Type(type = "uuid-char")
	@Column(name = "artifact_id")
	UUID id;

	@Column(name = "cloud_id", length = 64)
	String cloudId;

	@Column(name = "project_id", length = 64)
	String projectId;

	@Column(name = "bearer_access_token", length = 32)
	String bearerAccessToken;

	@Column(name = "client_secret", length = 32)
	String clientSecret;

	@OneToOne
	@OnDelete(action = OnDeleteAction.CASCADE)
	@JoinColumn(name = "user_id", nullable = false)
	SafaUser user;

	public UUID getId() {
		return id;
	}

	public JiraAccessCredentials setId(UUID id) {
		this.id = id;
		return this;
	}

	public String getCloudId() {
		return cloudId;
	}

	public JiraAccessCredentials setCloudId(String cloudId) {
		this.cloudId = cloudId;
		return this;
	}

	public String getProjectId() {
		return projectId;
	}

	public JiraAccessCredentials setProjectId(String projectId) {
		this.projectId = projectId;
		return this;
	}

	public String getBearerAccessToken() {
		return bearerAccessToken;
	}

	public JiraAccessCredentials setBearerAccessToken(String bearerAccessToken) {
		this.bearerAccessToken = bearerAccessToken;
		return this;
	}

	public String getClientSecret() {
		return clientSecret;
	}

	public JiraAccessCredentials setClientSecret(String clientSecret) {
		this.clientSecret = clientSecret;
		return this;
	}

	public SafaUser getUser() {
		return user;
	}

	public JiraAccessCredentials setUser(SafaUser user) {
		this.user = user;
		return this;
	}

	public String toString() {
		JSONObject json = new JSONObject();

		json.put("cloudId", this.cloudId);
		json.put("projectId", this.projectId);
		json.put("user", this.user.toString());
		return json.toString();
	}
}
