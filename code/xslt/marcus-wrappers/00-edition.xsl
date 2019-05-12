<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0" version="2.0">

    <!-- This stylesheet is part of the EB project. It transforms all entries from one single EB edition into a simple HTML view for checking OCR and markup. It is to be used on the wrapper files for each edition.-->

    <xsl:output method="xml"/>
    <xsl:template match="/">
        <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"></xsl:text>
        <html>
            <head>
                <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
                <title>test <xsl:value-of
                        select="tokenize(/TEI/teiHeader[1]/fileDesc[1]/titleStmt[1]/title[1], ' ')[3]"
                    /> Ed.</title>
                <style type="text/css">
                    body{
                        font-family: Georgia, serif;
                        margin-left: 2em;
                    }
                    p{
                        font-size: 1em;
                        line-height: 1.5em;
                        width: 750px;
                    }
                </style>
            </head>
            <body>
                <xsl:value-of select="/TEI/teiHeader[1]/fileDesc[1]/publicationStmt[1]/p[1]"/>
                <xsl:value-of select="/TEI/teiHeader[1]/encodingDesc[1]/p[1]"/>
                <xsl:apply-templates/>
            </body>
        </html>

    </xsl:template>

    <xsl:template match="teiHeader"/>

    <xsl:template match="label">
        <strong>
            <xsl:value-of select="."/>
        </strong>       
    </xsl:template>

    <xsl:template match="p">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

</xsl:stylesheet>
