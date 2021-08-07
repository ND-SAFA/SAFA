package edu.nd.crc.safa.services;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.repositories.ProjectRepository;
import edu.nd.crc.safa.responses.ServerError;
import edu.nd.crc.safa.utilities.OSHelper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@Service

public class ProjectService {
    /**
     * Responsible for all providing an API for performing the
     * business logic involved in ProjectsController.
     */
    ProjectRepository projectRepository;
    Puller mPuller;

    @Autowired
    public ProjectService(ProjectRepository projectRepository,
                          Puller puller) {
        this.projectRepository = projectRepository;
        this.mPuller = puller;
    }

    public void deleteProject(Project project) throws ServerError {
        this.projectRepository.delete(project);
        OSHelper.deletePath(ProjectPaths.getPathToStorage(project));
    }

    public SseEmitter projectPull(Project project, ProjectVersion projectVersion) {
        SseEmitter emitter = new SseEmitter(0L);
        ExecutorService sseMvcExecutor = Executors.newSingleThreadExecutor();
        sseMvcExecutor.execute(() -> {
            try {
                emitter.send(SseEmitter.event()
                    .data("{\"complete\": false}")
                    .id(String.valueOf(0))
                    .name("update"));

                String Mysql2NeoData = mPuller.mySQLNeo(project, projectVersion);
                emitter.send(SseEmitter.event()
                    .data(Mysql2NeoData)
                    .id(String.valueOf(3))
                    .name("update"));

                mPuller.execute();
                emitter.send(SseEmitter.event()
                    .data("{\"complete\": true}")
                    .id(String.valueOf(4))
                    .name("update"));

                emitter.complete();
            } catch (Exception ex) {
                emitter.completeWithError(ex);
            }
        });
        return emitter;
    }
}
