package edu.nd.crc.safa.services;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import edu.nd.crc.safa.entities.database.Project;
import edu.nd.crc.safa.entities.database.ProjectVersion;
import edu.nd.crc.safa.importer.Puller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@Service
public class PullingService {

    Puller puller;

    @Autowired
    public PullingService(Puller puller) {
        this.puller = puller;
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

                String Mysql2NeoData = puller.mySQLNeo(project, projectVersion);
                emitter.send(SseEmitter.event()
                    .data(Mysql2NeoData)
                    .id(String.valueOf(3))
                    .name("update"));

                puller.execute();
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
