@echo off
REM Generated file, do not edit manually
echo "NOTE: The startcmd.bat has been deprecated, use the dita.bat command instead."
pause

REM Get the absolute path of DITAOT's home directory
set DITA_DIR=%~dp0

REM Set environment variables
set ANT_OPTS=-Xmx512m %ANT_OPTS%
set ANT_OPTS=%ANT_OPTS% -Djavax.xml.transform.TransformerFactory=net.sf.saxon.TransformerFactoryImpl
set ANT_HOME=%DITA_DIR%
set PATH=%DITA_DIR%\bin;%PATH%
set CLASSPATH=%DITA_DIR%lib;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\ant-apache-resolver-1.10.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\ant-launcher.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\ant.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\commons-codec-1.10.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\commons-io-2.5.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\dost-configuration.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\dost.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\guava-19.0.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\icu4j-57.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\jsearch.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\logback-classic-1.2.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\logback-core-1.2.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\saxon-9.1.0.8-dom.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\saxon-9.1.0.8.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\slf4j-api-1.7.23.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\xercesImpl-2.11.0.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\xml-apis-1.4.01.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%lib\xml-resolver-1.2.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\markdown-1.3.0.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\pegdown-1.6.0.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\asm-analysis-5.0.3.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\asm-tree-5.0.3.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\asm-util-5.0.3.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\asm-5.0.3.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\parboiled-core-1.1.7.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\parboiled-java-1.1.7.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.elovirta.dita.markdown\snakeyaml-1.18.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2\lib\fo.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.oxygenxml.common\lib\jaxb-api-2.3.0.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.oxygenxml.common\lib\jaxb-core-2.3.0.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.oxygenxml.common\lib\jaxb-impl-2.3.0.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.oxygenxml.common\lib\activation-1.1.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.oxygenxml.common\lib\ant-contrib-1.0b3.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.oxygenxml.dost.patches\lib\oxygen-dost-patches.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\com.oxygenxml.highlight\lib\xslthl-2.1.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.odt\lib\odt.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.axf\lib\axf.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\oxygen-patches-fop.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\oxygen-patches-batik.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\avalon-framework-api-4.3.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\avalon-framework-impl-4.3.1.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\batik-all-1.9.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\commons-logging-1.0.4.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\fontbox-2.0.4.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\fop-2.2.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\xmlgraphics-commons-2.2.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.fop\lib\xml-apis-ext-1.3.04.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.pdf2.xep\lib\xep.jar;%CLASSPATH%
set CLASSPATH=%DITA_DIR%plugins\org.dita.wordrtf\lib\wordrtf.jar;%CLASSPATH%
start "DITA-OT" cmd.exe
