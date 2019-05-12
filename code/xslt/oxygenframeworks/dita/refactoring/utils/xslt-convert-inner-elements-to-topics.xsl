<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:f="http://www.oxygenxml.com/xsl/functions"
    exclude-result-prefixes="xs xd f"
    version="2.0">
    
    <xsl:import href="dita-formats.xsl"/>
    <xsl:param name="matchElement" as="xs:string*"/>
    
    <xd:doc>
        <xd:desc>Verifies if the current node is a topic(or specialization).</xd:desc>
        <xd:param name="node">Current node to check.</xd:param>
    </xd:doc>
    <xsl:function name="f:match4extraction" as="xs:boolean">
        <xsl:param name="node" as="node()"/>
        <xsl:value-of select="local-name($node) = $matchElement"/>
    </xsl:function>
    
    <xsl:variable name="extension" select="concat('.', tokenize(base-uri(), '[.]')[last()])"/>
    <xsl:variable name="timeStamp" select="( current-dateTime() - xs:dateTime('1970-01-01T00:00:00')) div xs:dayTimeDuration('PT1S') * 1000"/>
    
    <xd:doc>
        <xd:desc>DEFAULT COPY TEMPLATE</xd:desc>
    </xd:doc>
    <xsl:template match="node()[not(f:match4extraction(.))] | @*">
        <xsl:copy>
            <xsl:apply-templates select="node()[not(f:match4extraction(.))] | @*"/>
        </xsl:copy>
    </xsl:template>    
    
    <xd:doc>
        <xd:desc>Attributes copy template of generated documents. Cleanup: Skip oXygen attributes.</xd:desc>
    </xd:doc>
    <xsl:template match="@*" mode="write-sect">
        <xsl:if
            test="not(namespace-uri() = 'http://www.oxygenxml.com/ns/xmlRefactoring/additional_attributes')">
            <xsl:copy/>
        </xsl:if>
    </xsl:template>
    
    <xd:doc>
        <xd:desc>Node copy template of generated documents. </xd:desc>
    </xd:doc>
    <xsl:template match="node()[not(f:match4extraction(.))]" mode="write-sect">
        <xsl:copy>
            <xsl:apply-templates select="node()[not(f:match4extraction(.))] | @*[not(namespace-uri() = 'http://www.oxygenxml.com/ns/xmlRefactoring/additional_attributes')]" mode="write-sect"/>
        </xsl:copy>
    </xsl:template>
    
    <xd:doc>
        <xd:desc>Generate names for newly created files. Try to use topic's title, if any. If this fails 
            topic's ID is used. If this also fails generate a random name.</xd:desc>
        <xd:param name="node">Current node</xd:param>
        <xd:param name="baseURI">System ID of the current file.</xd:param>
        <xd:return>A name for refactored file.</xd:return>
    </xd:doc>
    <xsl:function name="f:generateOutputFileName" as="xs:string">
        <xsl:param name="node" as="node()"></xsl:param>
        <xsl:param name="baseURI" as="xs:string"/>
        <xsl:variable name="currentFileNameToUseAsPrefix" select="f:extractPrefixFromRefactoredFile($baseURI)"/>
        
        <xsl:variable name="uniqueFileName" select="f:generateUniqueFileName($node)"/>
        
        <xsl:variable name="fileNameCandidate"  select="concat($currentFileNameToUseAsPrefix, '_', $uniqueFileName)"/>
        
        <!-- check if file exists on file system -->
        <xsl:variable name="generatedFileSystemID" select="resolve-uri($fileNameCandidate, $baseURI)"/>
        
        <xsl:choose>
            <xsl:when test="doc-available($generatedFileSystemID)">
                <!-- NEW FILE -->
                <xsl:value-of select="concat(substring-before($fileNameCandidate, $extension), '_', $timeStamp, $extension)"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- save that file -->
                <xsl:value-of select="$fileNameCandidate"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:function>
    
    <xd:doc>
        <xd:desc>Generate a file name for each element. Does not guarantees the propsals are unique.</xd:desc>
        <xd:param name="node">Current node</xd:param>
    </xd:doc>
    <xsl:function name="f:generateFileName">
        <xsl:param name="node" as="node()"/>
        
        <!-- NODE TITLE -->
        <xsl:variable name="titleVal" select="$node/title"/>
        <!-- NODE ID -->
        <xsl:variable name="nodeID" select="$node/@id"/> 
        
        <xsl:variable name="fileName">
        <xsl:choose>
            <!-- First should try the title.-->
            <xsl:when test="$titleVal and $titleVal != ''">
                <xsl:value-of select="replace(lower-case(normalize-space(xs:string($titleVal))), ' ', '_')"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- No title; use sectionID. -->
                <xsl:choose>
                    <xsl:when test="$nodeID">
                        <xsl:value-of select="$nodeID"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="generate-id($node)"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>
        </xsl:variable>        
        <xsl:value-of select="translate($fileName, '\/:*&lt;&gt;&quot;|;&amp;!@#$%^?[]{}()', '')"/>
    </xsl:function>
    
    <xd:doc>
        <xd:desc>Generates an unique name for each topic.</xd:desc>
        <xd:param name="node">Current node</xd:param>
    </xd:doc>
    <xsl:function name="f:generateUniqueFileName">
        <xsl:param name="node" as="node()"/>
        <xsl:variable name="proposedFileName" select="f:generateFileName($node)"/>
        <xsl:variable name="uniqueNumber">            
            <xsl:value-of select="count($node/(preceding::* | ancestor:: *)[f:match4extraction($node)][f:generateFileName(.) = $proposedFileName])"/>
        </xsl:variable>
        <xsl:variable name="uniqueNumberSufix">
            <xsl:if test="$uniqueNumber > 0"><xsl:value-of select="$uniqueNumber"/></xsl:if>
        </xsl:variable>
        <xsl:value-of select="concat($proposedFileName, $uniqueNumberSufix, $extension)"/>        
    </xsl:function>
    
    <xd:doc>
        <xd:desc>Returns the name of the refactored files. Each new generated file will use this filename as prefix.</xd:desc>
        <xd:param name="baseURI">System ID of refactored file.</xd:param>
        <xd:return>Current file name without extension.</xd:return>
    </xd:doc>
    <xsl:function name="f:extractPrefixFromRefactoredFile">
        <xsl:param name="baseURI" as="xs:string"/>
        <xsl:variable name="fileName" select="(tokenize($baseURI,'/'))[last()]"/>
        <xsl:variable name="currentExtension" select="(tokenize($fileName, '\.'))[last()]"/>
        
        <xsl:value-of select="substring-before($fileName, concat('.', $currentExtension))"/>
    </xsl:function>
    
</xsl:stylesheet>