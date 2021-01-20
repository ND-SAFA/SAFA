package edu.nd.crc.safa.importer;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.xml.transform.Source;

import java.util.Base64;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import com.jsoniter.JsonIterator;
import org.springframework.stereotype.Component;

@Component
public class UploadFlatfile {

  public class ParsedFiles {
    private List<String> requiredFiles;
    private List<GeneratedFiles> generatedFiles;
    private List<String> generatedFileNames;

    public ParsedFiles(List<String> requiredFiles, List<GeneratedFiles> generatedFiles, List<String> generatedFileNames){
      this.requiredFiles = requiredFiles;
      this.generatedFiles = generatedFiles;
      this.generatedFileNames = generatedFileNames;
    }

    public List<String> getRequired(){
      return requiredFiles;
    }

    public List<GeneratedFiles> getGenerated() {
      return generatedFiles;
    }

    public List<String> getGeneratedNames() {
      return generatedFileNames;
    }
  }

  public class GeneratedFiles {
    private final String filename;
    private final String source;
    private final String target;

    public GeneratedFiles(String filename, String source, String target) {
      this.filename = filename;
      this.source = source;
      this.target = target;
    }

    public String getName(){
      return filename;
    }

    public String getSource(){
      return source;
    }

    public String getTarget(){
      return target;
    }
  }

  public void uploadFile(String projId, String jsonfiles) throws Exception {
    String flatfileDir = "/flatfilesDir";
    String generatedDir = "/generatedFilesDir";
    createDirectory(flatfileDir);
    createDirectory(generatedDir);
    
    JsonIterator iterator = JsonIterator.parse(jsonfiles);
    for (String filename = iterator.readObject(); filename != null; filename = iterator.readObject()){
      String encodedData = iterator.readString();
      byte[] bytes = Base64.getDecoder().decode(encodedData);
      String fullPath = flatfileDir + "/" + filename; 
      Files.write(Paths.get(fullPath), bytes);
    }
  }

  public String getMissingFiles(String projId) throws Exception {
    String flatfileDir = "/flatfilesDir";
    String generatedDir = "/generatedFilesDir";

    File flatDir = createDirectory(flatfileDir);
    File genDir = createDirectory(generatedDir);

    ParsedFiles parsedfiles = parseTim(flatfileDir);
    List<String> uploadedFiles = Arrays.asList(flatDir.list());
    List<String> generatedFiles = Arrays.asList(genDir.list());
    
    String requiredJSONPath = flatfileDir + "/requiredData.json";
    String generatedJSONPath = generatedDir + "/generatedData.json";
    
    
    String data = storeFilesAsJSON(uploadedFiles, parsedfiles, generatedFiles, requiredJSONPath, generatedJSONPath);
    
    System.out.println(data);
    return String.format("{ \"success\": true, \"message\": \"Checking missing files successful.\", \"data\": %s }", data);
  }

  public String deleteDirectory(String dir, String name) throws Exception {
    File myDir = createDirectory(dir);
    File[] fileList = myDir.listFiles();
    
    if (fileList.length > 0) {
      if (deleteDirectoryHelper(myDir)){
        createDirectory(dir);
        return String.format("{ \"success\": true, \"message\": \"%s have successfully been cleared.\"}", name);
      } 
      else {
        return String.format("{ \"success\": false, \"message\": \"%s could not be cleared.\"}", name);
      }
    }

    return String.format("{ \"success\": true, \"message\": \"%s have already been cleared.\"}", name);
  }

  public boolean deleteDirectoryHelper(File dir) throws Exception {
    File[] files = dir.listFiles();
    if (files != null) {
      for (File file : files) {
        deleteDirectoryHelper(file);
      }
    }
    return dir.delete();
  }
  
  // Modified file from Flatfile.java
  public ParsedFiles parseTim(String dirName) throws Exception {
    String fileName = dirName + '/' + "tim.json";
    File tim = new File(fileName);
    if (!tim.exists()){
      throw new Exception("Please upload a tim.json file");
    }

    String data = new String(Files.readAllBytes(Paths.get(fileName)));
    JsonIterator iterator = JsonIterator.parse(data);

    List<String> requiredFiles = new ArrayList<String>();
    List<String> generatedFileNames = new ArrayList<String>();
    List<GeneratedFiles> generatedFiles = new ArrayList<GeneratedFiles>();

    requiredFiles.add("tim.json");
    for (String field = iterator.readObject(); field != null; field = iterator.readObject()){
      if (field.toLowerCase().equals("datafiles")) {
        for (String artifact = iterator.readObject(); artifact != null; artifact = iterator.readObject()){
          Boolean fileCheck = false;

          for (String file = iterator.readObject(); file != null; file = iterator.readObject()){
            if (!file.toLowerCase().equals("file")){
              throw new Exception(String.format("Artifact: %s. Expected File attribute. The File attribute should appear as 'File': 'FileName'", artifact));
            }
            fileCheck = true;
            requiredFiles.add(iterator.readString());
          }

          if (!fileCheck) {
            throw new Exception(String.format("Did not provide a File attribute for Artifact: %s. The File attribute should appear as 'File': 'FileName'", artifact));
          }
        }
      }
      else {
        addLinkFile(field, iterator, requiredFiles, generatedFiles, generatedFileNames);
      }
    }
    return new ParsedFiles(requiredFiles, generatedFiles, generatedFileNames);
  }

  public void addLinkFile(String field, JsonIterator iterator, List<String> requiredFiles, List<GeneratedFiles> generatedFiles, List<String> generatedFileNames) throws Exception {
    String filename = "";
    String source = "";
    String target = "";
    Boolean generated = false;

    for (String attr = iterator.readObject(); attr != null; attr = iterator.readObject()) {
      if (!attr.toLowerCase().matches("file|source|target|generatelinks")) {
        throw new Exception(String.format("LinkFile: %s Attribute: %s does not match expected: 'File', 'Source', 'Target', or 'generateLinks'", field, attr));
      }

      if (attr.toLowerCase().equals("file")){
        filename = iterator.readString();
      }

      if (attr.toLowerCase().equals("source")){
        source = iterator.readString();
      }

      if (attr.toLowerCase().equals("target")){
        target = iterator.readString();
      }

      if (attr.toLowerCase().equals("generatelinks")){
        generated = iterator.readString().toLowerCase().equals("true") ? true : false;
      }
    }

    if (source.isEmpty()) {
      throw new Exception(String.format("Missing attribute for: '%s'. Missing: 'Source' Required attributes are 'File', 'Source', 'Target'", field));
    }

    if (target.isEmpty()) {
      throw new Exception(String.format("Missing attribute for: '%s'. Missing: 'Target' Required attributes are 'File', 'Source', 'Target'", field));
    }

    if (filename.isEmpty()) {
      throw new Exception(String.format("Missing attribute for: '%s'. Missing: 'File' Required attributes are 'File', 'Source', 'Target'", field));
    }

    if (generated){
      generatedFileNames.add(filename);
      generatedFiles.add(new GeneratedFiles(filename,source,target));
    }
    else {
      requiredFiles.add(filename);
    }
  }
  
  public static String createJsonArray(List<String> files) {
    String jsonArr = "";

    if (files.size() == 0){
      return "[]";
    }

    else if (files.size() == 1){
      return String.format("[\"%s\"]", files.get(0));
    }
    
    else {
      for (int i = 0; i < files.size(); i++){
        if (i == 0){
          jsonArr += "[\"" + files.get(i) + "\"";
        } 
        else if (i == files.size() - 1){
          jsonArr += ",\"" + files.get(i) + "\"]";
        }
        else {
          jsonArr += ",\"" + files.get(i) + "\"";
        }
      }
    }

    return jsonArr;
  }

  public String createGeneratedFileObj(List<GeneratedFiles> generatedFiles) {
    String data = "";

    if (generatedFiles.size() == 0){
      return "[]";
    }

    else if (generatedFiles.size() == 1){
      return "[{\"filename\":" + "\"" + generatedFiles.get(0).getName() + "\"" + ",\"source\":" + "\"" + generatedFiles.get(0).getSource() + "\"" + ",\"target\":" + "\"" + generatedFiles.get(0).getTarget() + "\"" + "}]";
    }
    
    else {
      for (int i = 0; i < generatedFiles.size(); i++){
        if (i == 0){
          data += "[{\"filename\":" + "\"" + generatedFiles.get(i).getName() + "\"" + ",\"source\":" + "\"" + generatedFiles.get(i).getSource() + "\"" + ",\"target\":" + "\"" + generatedFiles.get(i).getTarget() + "\"" + "}";
        } 
        else if (i == generatedFiles.size() - 1){
          data += ",{\"filename\":" + "\"" + generatedFiles.get(i).getName() + "\"" + ",\"source\":" + "\"" + generatedFiles.get(i).getSource() + "\"" + ",\"target\":" + "\"" + generatedFiles.get(i).getTarget() + "\"" + "}]";
        }
        else {
          data += ",{\"filename\":" + "\"" + generatedFiles.get(i).getName() + "\"" + ",\"source\":" + "\"" + generatedFiles.get(i).getSource() + "\"" + ",\"target\":" + "\"" + generatedFiles.get(i).getTarget() + "\"" + "}";
        }
      }
    }

    return data;
  }
    
  
  public String storeFilesAsJSON(List<String> uploadedFiles, ParsedFiles timFiles, List<String> generatedFiles, String requiredJSONPath, String generatedJSONPath) throws Exception {
    String requiredData = "{\"uploadedFiles\":" + createJsonArray(uploadedFiles) + ",\"expectedFiles\":" + createJsonArray(timFiles.getRequired()) + ",\"generatedFiles\":" + createJsonArray(generatedFiles) + ",\"expectedGeneratedFiles\":" + createJsonArray(timFiles.getGeneratedNames()) + "}";
    Files.write(Paths.get(requiredJSONPath), requiredData.getBytes());
    
    String generatedData = createGeneratedFileObj(timFiles.getGenerated());
    Files.write(Paths.get(generatedJSONPath), generatedData.getBytes());

    return requiredData;
  }
  
  public static File createDirectory(String dir) throws Exception {
    File myDir = new File(dir);

    if (!myDir.exists()) {
      if (!myDir.mkdirs()){
        throw new Exception(String.format("Error creating Flatfile folder: Path: %s", dir));
      }
    }

    if (!myDir.isDirectory()) {
      if (!myDir.delete()){
        throw new Exception(String.format("Error deleting Flatfile file: Path: %s", dir));
      }
      if (!myDir.mkdirs()){
        throw new Exception(String.format("Error creating Flatfile folder: Path: %s", dir));
      }
    }

    return myDir;
  }
}
