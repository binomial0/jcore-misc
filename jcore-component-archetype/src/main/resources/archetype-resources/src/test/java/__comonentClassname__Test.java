#set($symbol_pound='#')#set($symbol_dollar='$')#set($symbol_escape='\')

package ${package};

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.fit.factory.AnalysisEngineFactory;
import org.apache.uima.fit.factory.JCasFactory;
import org.apache.uima.fit.util.JCasUtil;
import org.apache.uima.jcas.JCas;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import cc.mallet.pipe.Pipe;
import cc.mallet.types.Instance;
import cc.mallet.types.InstanceList;import ${package}.Tokenizer;import ${package}.Unit;import ${package}.main.TokenAnnotator;import ${groupId}.jcore.types.Token;

/**
 * Unit tests for ${artifactId}.
 * @author 
 *
 */
public class ${componentClassname}Test{
// TODO
}
