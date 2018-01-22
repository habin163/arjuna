package pvt.unitee.reporter.lib.generator;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.log4j.Logger;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import arjunasdk.console.Console;
import pvt.batteries.config.Batteries;
import pvt.batteries.filehandler.FileReader;
import pvt.unitee.arjuna.ArjunaInternal;
import unitee.interfaces.Reporter;

public abstract class JsonResultsReader{
	private Logger logger = Logger.getLogger(Batteries.getCentralLogName());
	private String reportDir = null;
	private File[] files = null;
	private List<Reporter> generators = new ArrayList<Reporter>();
	
	public JsonResultsReader(String reportDir, List<Reporter> observers) throws Exception{
		this.reportDir = reportDir;
		files = (new File(reportDir)).listFiles();
		Arrays.sort(files);
		this.getGenerators().addAll(observers);
	}
	
	public void addGenerator(Reporter observer){
		this.getGenerators().add(observer);
	}
	
	private JsonElement getJson(File f) throws IOException{
		FileReader reader = new FileReader(reportDir + "/" + f.getName());
		return (new JsonParser()).parse(reader.read());
	}
	
	abstract protected void update(JsonElement jElement) throws Exception;
	
	public void generate() {
		if (ArjunaInternal.displayReportGenerationInfo){
			logger.debug(String.format("%s: #Generators: %d.", this.getClass().getSimpleName(), this.generators.size()));
			logger.debug(String.format("%s: #Records: %d.", this.getClass().getSimpleName(), this.files.length));
		}
		for (File f: files){
			try {
				if (ArjunaInternal.displayReportGenerationInfo){
					logger.debug(String.format("%s: Convert file to Json: %s.", this.getClass().getSimpleName(), f.getName()));
				}
				JsonElement jElement = getJson(f);
				if (ArjunaInternal.displayReportGenerationInfo){
					logger.debug(String.format("%s: Convert JSON to Reportable.", this.getClass().getSimpleName(), f.getName()));
					logger.debug(String.format("JSON: %s.", jElement.toString()));
					logger.debug(String.format("%s: Update generators.", this.getClass().getSimpleName(), f.getName()));
				}
				update(jElement);
				if (ArjunaInternal.displayReportGenerationInfo){
					
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				Console.displayExceptionBlock(e);
			}
		}			
	}

	protected List<Reporter> getGenerators() {
		return generators;
	}

	private void setGenerators(List<Reporter> generators) {
		this.generators = generators;
	}
}
