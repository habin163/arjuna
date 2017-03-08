package com.autocognite.pvt.batteries.hocon;

import java.util.HashMap;
import java.util.Set;
import java.util.Map.Entry;

import com.autocognite.arjuna.interfaces.Value;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigValue;

public interface HoconReader {

	void setConfig(Config loadedConf);

	void process() throws Exception;

	Config getConfig();

	HashMap<String, Value> getProperties();
	
	 void loadConfig() throws Exception;
	 
	 Set<Entry<String, ConfigValue>> getSystemPropSet();
	 Set<String> getSystemKeys();

}