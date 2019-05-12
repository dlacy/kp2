<?xml version="1.0" encoding="UTF-8"?>
<!--
  The Syncro Soft SRL License
  
  
  Copyright (c) 1998-2011 Syncro Soft SRL, Romania.  All rights
  reserved.
  
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:
  
  1. Redistribution of source or in binary form is allowed only with
  the prior written permission of Syncro Soft SRL.
  
  2. Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
  
  2. Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the
  distribution.
  
  3. The end-user documentation included with the redistribution,
  if any, must include the following acknowledgment:
  "This product includes software developed by the
  Syncro Soft SRL (http://www.sync.ro/)."
  Alternately, this acknowledgment may appear in the software itself,
  if and wherever such third-party acknowledgments normally appear.
  
  4. The names "Oxygen" and "Syncro Soft SRL" must
  not be used to endorse or promote products derived from this
  software without prior written permission. For written
  permission, please contact support@oxygenxml.com.
  
  5. Products derived from this software may not be called "Oxygen",
  nor may "Oxygen" appear in their name, without prior written
  permission of the Syncro Soft SRL.
  
  THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED.  IN NO EVENT SHALL THE SYNCRO SOFT SRL OR
  ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
  USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
  SUCH DAMAGE.
  
  Check accessibility rules.
-->
<schema xmlns="http://purl.oclc.org/dsdl/schematron" 
    queryBinding="xslt2" xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <title>Accessibility rules for DITA 1.2</title>
    
    <ns uri="http://dita.oasis-open.org/architecture/2005/" prefix="ditaarch"/>
    
    <pattern id="no_alt_desc">
        <!-- EXM-28035 Avoid reporting warnings when the image has a @conref or @conkeyref, the attribute might be on the target. -->
        <rule context="*[contains(@class, ' topic/image ')][not(@conref)][not(@conkeyref)]">
            <assert test="@alt | alt" 
                flag="non-WAI" role="warning" sqf:fix="addAltElem" see="https://www.oxygenxml.com/dita/1.3/specs/langRef/base/image.html">                
                Images must have text alternatives that describe the information or function represented by them.</assert>
            
            <sqf:fix id="addAltElem">
                <sqf:description>
                    <sqf:title>Add alt element</sqf:title>   
                </sqf:description>
                <sqf:add node-type="element" target="alt"><xsl:processing-instruction name="oxy-placeholder">content="Insert alternate text here"</xsl:processing-instruction></sqf:add>                
            </sqf:fix>
        </rule>
    </pattern>    
</schema>