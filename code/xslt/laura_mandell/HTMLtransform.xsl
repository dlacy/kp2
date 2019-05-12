<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xhtml="http://www.w3.org/1999/xhtml" exclude-result-prefixes="xs tei xhtml" version="2.0">

    <!-- From Laura Mandell Digital Editing course. This is a copy of her basic master for beginning creating a TEI-to-HTML transform. -->

    <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" method="xhtml"
        omit-xml-declaration="yes" indent="yes" encoding="UTF-8"/>

    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <!-- Begins with template match for TEI root element. In that context, you can create the html elements surrounding the whole document: the html root and its two children, head and body. -->

    <xsl:template match="tei:TEI">
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <xsl:comment>This document is generated from a TEI Master--do not edit!</xsl:comment>
                <title>
                    <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                </title>
                <link rel="stylesheet" type="text/css" href="../css/myStyle.css"/>
                <style type="text/css">
                    @import url("../css/myStyle.css");</style>

            </head>
            <body>
                <xsl:apply-templates select="tei:text"/>
                <h3 xmlns="http://www.w3.org/1999/xhtml">Endnotes</h3>
                <xsl:apply-templates select="//tei:note" mode="tei:endnote"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="tei:head">
        <h3 xmlns="http://www.w3.org/1999/xhtml">
            <xsl:apply-templates/>
        </h3>
    </xsl:template>

    <xsl:template match="tei:byline">
        <h4 xmlns="http://www.w3.org/1999/xhtml">
            <xsl:apply-templates/>
        </h4>
    </xsl:template>

    <xsl:template match="tei:p | tei:lg">
        <p xmlns="http://www.w3.org/1999/xhtml">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <xsl:template match="tei:imprint/tei:date">
        <xsl:text>, published </xsl:text>
        <xsl:value-of select="substring-after(., '-')"/>
        <xsl:text>/</xsl:text>
        <xsl:value-of select="substring-before(., '-')"/>
        <xsl:text>, </xsl:text>
    </xsl:template>

    <xsl:template match="tei:date">
        <xsl:text> </xsl:text>
        <xsl:value-of select="."/>
        <xsl:text/>
    </xsl:template>

    <xsl:template match="tei:title">
        <em xmlns="http://www.w3.org/1999/xhtml">
            <xsl:apply-templates/>
        </em>
    </xsl:template>

    <xsl:template match="tei:biblScope">
        <xsl:choose>
            <xsl:when test="@unit = 'volume'">
                <xsl:text>, Vol. </xsl:text>
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:when test="@unit = 'page'">
                <xsl:text>pp. </xsl:text>
                <xsl:value-of select="."/>
                <xsl:text>.</xsl:text>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:note">
        <xsl:variable name="N">
            <xsl:number level="any"/>
        </xsl:variable>
        <a xmlns="http://www.w3.org/1999/xhtml" name="back{$N}"/>
        <a xmlns="http://www.w3.org/1999/xhtml" href="#note{$N}">
            <sup xmlns="http://www.w3.org/1999/xhtml">
                <xsl:value-of select="$N"/>
            </sup>
        </a>
    </xsl:template>

    <xsl:template match="tei:note" mode="tei:endnote">
        <xsl:variable name="N">
            <xsl:number level="any"/>
        </xsl:variable>
        <p xmlns="http://www.w3.org/1999/xhtml">
            <a name="note{$N}"/>
            <xsl:value-of select="$N"/>
            <xsl:text>. </xsl:text>
            <xsl:apply-templates/>
            <a xmlns="http://www.w3.org/1999/xhtml" href="#back{$N}">. Back.</a>
        </p>
    </xsl:template>

</xsl:stylesheet>
