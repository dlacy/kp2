<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0" version="2.0">

    <!-- This stylesheet is part of the EB project. It transforms a single EB TEI-entry into a simple HTML view for checking OCR and markup.-->

    <xsl:output method="xml"/>
    <xsl:template match="/">
        <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"></xsl:text>
        <html>
            <head>
                <title>test-output entry <xsl:value-of select="tokenize(base-uri(), '/')[last()]"
                    /></title>
                <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
                <style type="text/css">
                    body{
                        font-family: Georgia, serif;
                        margin-left: 2em;
                    }
                    p{
                        font-size: 1.1em;
                        line-height: 1.6em;
                        width: 750px;
                    }</style>
            </head>

            <body>
                <xsl:apply-templates/>
            </body>
        </html>

    </xsl:template>

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
