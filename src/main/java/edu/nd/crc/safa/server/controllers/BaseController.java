package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.ResponseCodes;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
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
    public ServerResponse handleServerError(ServerError exception) {
        exception.printError();
        return new ServerResponse(exception, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleValidationError(MethodArgumentNotValidException exception) {
        BindingResult bindingResult = exception.getBindingResult();
        StringBuilder errorMessage = new StringBuilder();
        for (ObjectError error : bindingResult.getAllErrors()) {
            errorMessage.append(createValidationMessage(error)).append("\n");
        }
        ServerError error = new ServerError(errorMessage.toString());
        error.setDetails(exception.getMessage());
        return new ServerResponse(error, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleDataIntegrityViolationException(DataIntegrityViolationException exception) {
        exception.printStackTrace();
        String causeName = exception.getMostSpecificCause().toString();
        String errorMessage = String.format("Data integrity violation: %s", causeName);
        ServerError error = new ServerError(errorMessage, exception);
        error.setDetails(exception.getMessage());
        return new ServerResponse(error, ResponseCodes.FAILURE);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ServerResponse handleGenericError(Exception ex) {
        ex.printStackTrace();
        ServerError wrapper = new ServerError("An unexpected server error occurred.", ex);
        return new ServerResponse(wrapper, ResponseCodes.FAILURE);
    }

    protected Project getProject(String projectId) throws ServerError {
        Optional<Project> queriedProject = this.projectRepository.findById(UUID.fromString(projectId));
        if (queriedProject.isEmpty()) {
            throw new ServerError("Could not find project with id:" + projectId);
        }
        return queriedProject.get();
    }

    private String createValidationMessage(ObjectError error) {
        String objectName = error.getObjectName();
        String message = error.getDefaultMessage();
        if (error instanceof FieldError) {
            String fieldName = ((FieldError) error).getField();
            return fieldName + " in " + objectName + " " + message;
        } else {
            return objectName + message;
        }
    }

    protected Project createProjectIdentifier(String name, String description) {
        Project project = new Project(name, description); // TODO: extract name from TIM file
        this.projectRepository.save(project);
        return project;
    }

    protected ProjectVersion createProjectVersion(Project project) {
        ProjectVersion projectVersion = new ProjectVersion(project, 1, 1, 1);
        this.projectVersionRepository.save(projectVersion);
        return projectVersion;
    }
}
