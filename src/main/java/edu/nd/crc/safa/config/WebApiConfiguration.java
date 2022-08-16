package edu.nd.crc.safa.config;

import edu.nd.crc.safa.features.jira.repositories.JiraProjectRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jira.services.JiraConnectionServiceImpl;
import edu.nd.crc.safa.server.repositories.github.GithubProjectRepository;
import edu.nd.crc.safa.server.services.github.GithubConnectionService;
import edu.nd.crc.safa.server.services.github.GithubConnectionServiceImpl;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.codec.json.Jackson2JsonDecoder;
import org.springframework.http.codec.json.Jackson2JsonEncoder;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.netty.http.client.HttpClient;

/**
 * Responsible for configuring the services and components responsible for linking Safa to external APIs
 */
@Configuration
@AllArgsConstructor
public class WebApiConfiguration {

    public static final String JSON_CONTENT_TYPE_HEADER_VALUE = "application/json";

    private static final Integer WEBCLIENT_MAX_MEMORY = 16 * 1024 * 1024;
    private static final Logger log = LoggerFactory.getLogger(WebApiConfiguration.class);

    private JiraProjectRepository jiraProjectRepository;
    private GithubProjectRepository githubProjectRepository;

    @Bean
    public JiraConnectionService jiraConnectionService() {
        return new JiraConnectionServiceImpl(jiraProjectRepository, webClient());
    }

    @Bean
    public GithubConnectionService githubConnectionService() {
        return new GithubConnectionServiceImpl(githubProjectRepository, webClient());
    }

    private ExchangeFilterFunction logRequest() {
        return ExchangeFilterFunction.ofRequestProcessor(clientRequest -> {
            log.info("Request: {} {}", clientRequest.method(), clientRequest.url());

            clientRequest.headers().forEach((name, values) -> {
                values.forEach(value -> {
                    log.info("{}={}", name, value);
                });
            });

            return Mono.just(clientRequest);
        });
    }

    @Bean
    public WebClient webClient() {
        ObjectMapper mapper = new ObjectMapper();

        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

        return WebClient.builder()
            .codecs(configure -> {
                configure.defaultCodecs().maxInMemorySize(WEBCLIENT_MAX_MEMORY);
                configure.defaultCodecs().enableLoggingRequestDetails(true);
                configure.defaultCodecs().jackson2JsonEncoder(
                    new Jackson2JsonEncoder(mapper, MediaType.APPLICATION_JSON));
                configure.defaultCodecs().jackson2JsonDecoder(
                    new Jackson2JsonDecoder(mapper, MediaType.APPLICATION_JSON));
            })
            .clientConnector(new ReactorClientHttpConnector(HttpClient.create().wiretap(true)))
            .defaultHeader(HttpHeaders.CONTENT_TYPE, JSON_CONTENT_TYPE_HEADER_VALUE)
            .defaultHeader(HttpHeaders.ACCEPT, "*/*")
            .build();
    }

}
