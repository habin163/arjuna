package com.autocognite.pvt.unitee.reporter.lib.fixture;

import com.autocognite.pvt.unitee.core.lib.testvars.InternalTestVariables;
import com.autocognite.pvt.unitee.reporter.lib.reportable.ResultDeserializer;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonObject;

public class FixtureResultDeserializer extends ResultDeserializer<FixtureResult> implements JsonDeserializer<FixtureResult> {
	
	public FixtureResult process(JsonObject root){
		FixtureResultBuilder builder = null;
		InternalTestVariables testVars = getTestVars(root);
		FixtureResult outResult = null;

		try{
			builder = new FixtureResultBuilder();

			//Deserialize autoProps
			JsonObject resultPropsObj = root.get("resultProps").getAsJsonObject();
			FixtureResultProperties resultProps = new FixtureResultProperties();
			processJsonObjectForEnumMap(resultPropsObj, resultProps);
	
			outResult = builder.resultProps(resultProps).testVariables(testVars).build();
		} catch (Exception e){
			e.printStackTrace();
		}

		return outResult;		
	}

}