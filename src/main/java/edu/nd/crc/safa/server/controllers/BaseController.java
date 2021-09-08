package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;
import javax.servlet.http.HttpServletRequest;

import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.repositories.ProjectRepository;
import edu.nd.crc.safa.db.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.responses.ResponseCodes;
import edu.nd.crc.safa.server.responses.ServerError;
import edu.nd.crc.safa.server.responses.ServerResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public abstract class BaseController {

    protected ProjectVersionRepository projectVersionRepository;
    protected ProjectRepository projectRepository;

    @Autowired
    public BaseController(ProjectRepository projectRepository,
                          ProjectVersionRepository projectVersionRepository) {
        this.projectVersionRepository = projectVersionRepository;
        this.projectRepository = projectRepository;
    }

    @ExceptionHandler(ServerError.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleServerError(HttpServletRequest req,
                                            ServerError exception) {
        exception.printError();
        return new ServerResponse(exception, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleGenericError(HttpServletRequest req,
                                             Exception ex) {
        ex.printStackTrace();
        ServerError wrapper = new ServerError("unknown activity", ex);
        return new ServerResponse(wrapper, ResponseCodes.FAILURE);
    }

    protected Project getProject(String projectId) throws ServerError {
        Optional<Project> queriedProject = this.projectRepository.findById(UUID.fromString(projectId));
        if (!queriedProject.isPresent()) {
            throw new ServerError("Could not find project with id:" + projectId);
        }
        return queriedProject.get();
    }
}
