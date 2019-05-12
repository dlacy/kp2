<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <!-- DITA output format -->
    <xsl:output name="topic" exclude-result-prefixes="#all" indent="yes" doctype-public="-//OASIS//DTD DITA Topic//EN" doctype-system="topic.dtd"/>
    
    <!-- DITA task -->
    <xsl:output name="task" exclude-result-prefixes="#all" indent="yes" doctype-public="-//OASIS//DTD DITA Task//EN" doctype-system="task.dtd"/>
    
    <!-- DITA glossentry -->
    <xsl:output name="glossentry" exclude-result-prefixes="#all" indent="yes" doctype-public="-//OASIS//DTD DITA Glossary//EN" doctype-system="glossary.dtd"/>
    
    <!-- DITA  Concept-->
    <xsl:output name="concept" exclude-result-prefixes="#all" indent="yes" doctype-public="-//OASIS//DTD DITA Concept//EN" doctype-system="concept.dtd"/>
    
    <!-- DITA  Glossgroup-->
    <xsl:output name="glossgroup" exclude-result-prefixes="#all" indent="yes" doctype-public="-//OASIS//DTD DITA Glossary Group//EN" doctype-system="glossgroup.dtd"/>
    
    <!-- DITA  Reference-->
    <xsl:output name="reference" exclude-result-prefixes="#all" indent="yes" doctype-public="-//OASIS//DTD DITA Reference//EN" doctype-system="reference.dtd"/>
    
    <!-- DITA  Troubleshooting-->
    <xsl:output name="troubleshooting" exclude-result-prefixes="#all" indent="yes" doctype-public="-//OASIS//DTD DITA Troubleshooting//EN" doctype-system="troubleshooting.dtd"/>
    
</xsl:stylesheet>