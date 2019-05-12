<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xra="http://www.oxygenxml.com/ns/xmlRefactoring/additional_attributes"
    xmlns:f="http://www.oxygenxml.com/xsl/functions"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    version="2.0" 
    exclude-result-prefixes="xra xs f xd">
    
    <xsl:param name="matchElement" 
        select="('topic', 'task', 'glossentry', 'concept', 'glossgroup', 'reference', 'troubleshooting')"></xsl:param>
    <xsl:import href="utils/xslt-convert-inner-elements-to-topics.xsl"/>
    
    <xd:doc>
        <xd:desc>Entry point. Match topic and generate new files for them.</xd:desc>
    </xd:doc>
    <xsl:template match="/*">
        <!-- Write to new files all descendents that match the extraction creteria. -->
        <xsl:apply-templates mode="emit" select=".//*[f:match4extraction(.)]"/>
        
        <!-- Copy the other ones. -->
        <xsl:copy>
            <xsl:apply-templates select="(node() except node()[f:match4extraction(.)]) | @*"/>
        </xsl:copy>
    </xsl:template>
    
    <xd:doc>
        <xd:desc>Match topics and call the template that creates new files.</xd:desc>
    </xd:doc>
    <xsl:template match="*[f:match4extraction(.)]" mode="emit">
        <xsl:variable name="proposalName" select="f:generateOutputFileName(., base-uri())"/>
        <xsl:variable name="name" select="resolve-uri($proposalName, base-uri())"/>
        <xsl:call-template name="write-topic" >
            <xsl:with-param name="newDocumentName" select="$name"/>
        </xsl:call-template>
    </xsl:template>
    
    <xd:doc>
        <xd:desc>The template that generates new documents from topics.</xd:desc>
        <xd:param name="newDocumentName">New file name.</xd:param>
    </xd:doc>
    <xsl:template name="write-topic">
        <xsl:param name="newDocumentName" as="xs:string"/>
        
        <xsl:variable name="outputFormat">
            <xsl:choose>
                <xsl:when test="local-name(.) = 'section'">
                    <xsl:value-of select="'topic'"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="local-name(.)"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <!-- Creating  -->
        <xsl:result-document href="{$newDocumentName}" format="{$outputFormat}" indent="yes">
            
            <xsl:choose>
                <xsl:when test="local-name(.) = 'section'">
                    <topic>
                        <xsl:call-template name="copyAttributes"/>
                        <xsl:apply-templates select="title" mode="write-sect"/>
                        <body>
                            <xsl:apply-templates select="node() except title" mode="write-sect"/>
                        </body>
                    </topic>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy>
                        <xsl:call-template name="copyAttributes"/>
                        <xsl:apply-templates select="node() except (*[f:match4extraction(.)])" mode="write-sect"/>
                    </xsl:copy>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:result-document>
    </xsl:template>
    
    <xd:doc>
        <xd:desc>Copies all atributes. If an @id doesn't exist, it generates one.</xd:desc>
    </xd:doc>
    <xsl:template name="copyAttributes">
        <xsl:apply-templates select="@*" mode="write-sect"/>

        <xsl:if test="not(@id)">
            <xsl:attribute name="id" select="replace(f:generateOutputFileName(., base-uri()), $extension, '')"/>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>
