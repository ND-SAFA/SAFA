package edu.nd.crc.safa.server.services.jira;


import java.util.Optional;

import javax.annotation.PostConstruct;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientException;
import reactor.core.publisher.Mono;


/**
 * @author mpop
 */
@Service
public class JiraConnectionService {

	private final Logger log = LoggerFactory.getLogger(JiraConnectionService.class);

	private static final int API_VERSION = 3;

	private static final String CONTENT_TYPE_HEADER_VALUE = "application/json; charset=UTF-8;";

	private WebClient webClient;

	private String authorization;

	private String buildBaseURI(String cloudId) {
		return String.format("/jira/%s/rest/api/%d", cloudId, API_VERSION);
	}

	private String buildAuthorizationHeaderValue(String token) {
		return String.format("Bearer %s", token);
	}

	@PostConstruct
	private void init() {
		this.webClient = WebClient.builder()
			.baseUrl("https://api.atlassian.com/ex")
			.defaultHeader(HttpHeaders.CONTENT_TYPE, CONTENT_TYPE_HEADER_VALUE)
			.build();

		log.info("Web client initialised");
	}

	public JiraProjectResponse retrieveJIRAProject(JiraAccessCredentials credentials, Long id) throws SafaError {
		String baseURI = this.buildBaseURI(credentials.getCloudId());

		return blockOptional(
			this.webClient
				.method(ApiRoutes.PROJECT.getMethod())
				.uri(baseURI + ApiRoutes.PROJECT.getPath(), id)
				.header(HttpHeaders.AUTHORIZATION, this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
				.retrieve()
				.bodyToMono(JiraProjectResponse.class)
		).orElseThrow(() -> new SafaError("Error while trying to retrieve JIRA project"));
	}

	public boolean checkCredentials(JiraAccessCredentials credentials) {
		String baseURI = this.buildBaseURI(credentials.getCloudId());

		HttpStatus code = this.webClient
			.method(ApiRoutes.MYSELF.getMethod())
			.uri(baseURI + ApiRoutes.MYSELF.getPath())
			.header(HttpHeaders.AUTHORIZATION, this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
			.retrieve()
			.toBodilessEntity()
			.map(ResponseEntity::getStatusCode)
			.block();

		return !HttpStatus.UNAUTHORIZED.equals(code);
	}

	private <T> Optional<T> blockOptional(Mono<T> mono) throws SafaError {
		try {
			return mono.blockOptional();
		} catch (WebClientException ex) {
			log.error("Exception thrown while executing blocking call", ex);
			throw new SafaError("Exception thrown while executing blocking call", ex);
		}
	}

	private enum ApiRoutes {
		PROJECT("/project/{id}", HttpMethod.GET),
		MYSELF("/myself", HttpMethod.GET);

		private final String path;

		private final HttpMethod method;

		ApiRoutes(String path, HttpMethod method) {
			this.path = path;
			this.method = method;
		}

		public String getPath() {
			return path;
		}

		public HttpMethod getMethod() {
			return method;
		}
	}
}

