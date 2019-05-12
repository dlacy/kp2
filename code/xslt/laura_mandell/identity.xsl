<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs tei" xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:output method="xml" encoding="utf-8" omit-xml-declaration="no"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
    
    <!-- this identity template copies the whole xml document exactly as it is -->
    
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- to make changes to the xml, match the node/tag in the original document that you wish to change
        and then inside that template, add the tag and its attributes that you wish to use instead, as here: -->
    
   <xsl:template match="hi">
       <hi rend="italic" xmlns="http://www.tei-c.org/ns/1.0"><xsl:apply-templates/></hi>
   </xsl:template>
    
    <!-- for another way to make changes, see newWilson.xsl -->
        
</xsl:stylesheet>