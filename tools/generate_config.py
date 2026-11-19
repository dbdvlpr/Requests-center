# -*- coding: utf-8 -*-
"""Конфигурация 8.3.25: центр интеллектуальной обработки клиентских обращений."""
import os
import re
import uuid
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
TEMPLATE_CATALOG = os.path.abspath(os.path.join(ROOT, "..", "src", "Catalogs", "Поставщики.xml"))
TEMPLATE_CONFIG = os.path.abspath(os.path.join(ROOT, "..", "src", "Configuration.xml"))
TEMPLATE_LANG = os.path.abspath(os.path.join(ROOT, "..", "src", "Languages", "Русский.xml"))
NS = uuid.uuid5(uuid.NAMESPACE_DNS, "1c-marathon-appeals")
UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xen="http://v8.1c.ru/8.3/xcf/enums" xmlns:xpr="http://v8.1c.ru/8.3/xcf/predef" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.18">
'''

FORM_NS = '''<?xml version="1.0" encoding="UTF-8"?>
<Form xmlns="http://v8.1c.ru/8.3/xcf/logform" xmlns:app="http://v8.1c.ru/8.2/managed-application/core" xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" xmlns:dcscor="http://v8.1c.ru/8.1/data-composition-system/core" xmlns:dcssch="http://v8.1c.ru/8.1/data-composition-system/schema" xmlns:dcsset="http://v8.1c.ru/8.1/data-composition-system/settings" xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.18">
'''


def uid(name):
    return str(uuid.uuid5(NS, name))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text)


def read_text(path):
    with open(path, encoding="utf-8-sig") as handle:
        return handle.read()


def syn_item(text, indent):
    return (
        "%s<v8:item>\n"
        "%s\t<v8:lang>ru</v8:lang>\n"
        "%s\t<v8:content>%s</v8:content>\n"
        "%s</v8:item>" % (indent, indent, indent, escape(text), indent)
    )


def synonym(text, indent="\t\t\t"):
    return "%s<Synonym>\n%s\n%s</Synonym>" % (indent, syn_item(text, indent + "\t"), indent)


def generated(pairs, indent="\t\t"):
    lines = [indent + "<InternalInfo>"]
    inner = indent + "\t"
    for name, category in pairs:
        lines.append(inner + '<xr:GeneratedType name="%s" category="%s">' % (name, category))
        lines.append(inner + "\t<xr:TypeId>%s</xr:TypeId>" % uid(name + ":type"))
        lines.append(inner + "\t<xr:ValueId>%s</xr:ValueId>" % uid(name + ":value"))
        lines.append(inner + "</xr:GeneratedType>")
    lines.append(indent + "</InternalInfo>")
    return "\n".join(lines)


def type_xml(kind, ref=None, length=10, fraction=0, sign="Nonnegative", date="DateTime", indent="\t\t\t\t\t"):
    if kind == "string":
        return (
            "%s<Type>\n"
            "%s\t<v8:Type>xs:string</v8:Type>\n"
            "%s\t<v8:StringQualifiers>\n"
            "%s\t\t<v8:Length>%s</v8:Length>\n"
            "%s\t\t<v8:AllowedLength>Variable</v8:AllowedLength>\n"
            "%s\t</v8:StringQualifiers>\n"
            "%s</Type>" % (indent, indent, indent, indent, length, indent, indent, indent)
        )
    if kind == "number":
        return (
            "%s<Type>\n"
            "%s\t<v8:Type>xs:decimal</v8:Type>\n"
            "%s\t<v8:NumberQualifiers>\n"
            "%s\t\t<v8:Digits>%s</v8:Digits>\n"
            "%s\t\t<v8:FractionDigits>%s</v8:FractionDigits>\n"
            "%s\t\t<v8:AllowedSign>%s</v8:AllowedSign>\n"
            "%s\t</v8:NumberQualifiers>\n"
            "%s</Type>" % (indent, indent, indent, indent, length, indent, fraction, indent, sign, indent, indent)
        )
    if kind == "boolean":
        return "%s<Type>\n%s\t<v8:Type>xs:boolean</v8:Type>\n%s</Type>" % (indent, indent, indent)
    if kind == "date":
        return (
            "%s<Type>\n"
            "%s\t<v8:Type>xs:dateTime</v8:Type>\n"
            "%s\t<v8:DateQualifiers>\n"
            "%s\t\t<v8:DateFractions>%s</v8:DateFractions>\n"
            "%s\t</v8:DateQualifiers>\n"
            "%s</Type>" % (indent, indent, indent, indent, date, indent, indent)
        )
    return "%s<Type>\n%s\t<v8:Type>%s</v8:Type>\n%s</Type>" % (indent, indent, ref, indent)


def fill_value(kind, indent):
    if kind == "string":
        return '%s<FillValue xsi:type="xs:string"/>' % indent
    if kind == "number":
        return '%s<FillValue xsi:type="xs:decimal">0</FillValue>' % indent
    if kind == "boolean":
        return '%s<FillValue xsi:type="xs:boolean">false</FillValue>' % indent
    return '%s<FillValue xsi:nil="true"/>' % indent


def render_attribute(owner, spec, for_catalog=False, tabular=False):
    kind = spec["kind"]
    indent = "\t\t\t\t\t"
    lines = [
        '\t\t\t<Attribute uuid="%s">' % uid(owner + "." + spec["name"]),
        "\t\t\t\t<Properties>",
        "\t\t\t\t\t<Name>%s</Name>" % spec["name"],
        synonym(spec["title"], "\t\t\t\t\t"),
        "\t\t\t\t\t<Comment/>",
        type_xml(kind, spec.get("ref"), spec.get("length", 10), spec.get("fraction", 0),
                 spec.get("sign", "Nonnegative"), spec.get("date", "DateTime"), indent),
        "\t\t\t\t\t<PasswordMode>%s</PasswordMode>" % ("true" if spec.get("password") else "false"),
        "\t\t\t\t\t<Format/>",
        "\t\t\t\t\t<EditFormat/>",
        "\t\t\t\t\t<ToolTip/>",
        "\t\t\t\t\t<MarkNegatives>false</MarkNegatives>",
        "\t\t\t\t\t<Mask/>",
        "\t\t\t\t\t<MultiLine>%s</MultiLine>" % ("true" if spec.get("multiline") else "false"),
        "\t\t\t\t\t<ExtendedEdit>%s</ExtendedEdit>" % ("true" if spec.get("multiline") else "false"),
        '\t\t\t\t\t<MinValue xsi:nil="true"/>',
        '\t\t\t\t\t<MaxValue xsi:nil="true"/>',
    ]
    if not tabular:
        lines.append("\t\t\t\t\t<FillFromFillingValue>false</FillFromFillingValue>")
        lines.append(fill_value(kind, "\t\t\t\t\t"))
    lines += [
        "\t\t\t\t\t<FillChecking>%s</FillChecking>" % spec.get("fill", "DontCheck"),
        "\t\t\t\t\t<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>",
        "\t\t\t\t\t<ChoiceParameterLinks/>",
        "\t\t\t\t\t<ChoiceParameters/>",
        "\t\t\t\t\t<QuickChoice>Auto</QuickChoice>",
        "\t\t\t\t\t<CreateOnInput>Auto</CreateOnInput>",
        "\t\t\t\t\t<ChoiceForm/>",
        "\t\t\t\t\t<LinkByType/>",
        "\t\t\t\t\t<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>",
    ]
    if for_catalog and not tabular:
        lines.append("\t\t\t\t\t<Use>ForItem</Use>")
    lines += [
        "\t\t\t\t\t<Indexing>%s</Indexing>" % spec.get("index", "DontIndex"),
        "\t\t\t\t\t<FullTextSearch>%s</FullTextSearch>" % spec.get("fulltext", "Use"),
        "\t\t\t\t\t<DataHistory>Use</DataHistory>",
        "\t\t\t\t</Properties>",
        "\t\t\t</Attribute>",
    ]
    return "\n".join(lines)


def enum_xml(name, title, values):
    body = [HEADER, '\t<Enum uuid="%s">' % uid("Enum." + name)]
    body.append(generated([
        ("EnumRef." + name, "Ref"),
        ("EnumManager." + name, "Manager"),
        ("EnumList." + name, "List"),
    ]))
    body += [
        "\t\t<Properties>",
        "\t\t\t<Name>%s</Name>" % name,
        synonym(title, "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<UseStandardCommands>false</UseStandardCommands>",
        "\t\t\t<Characteristics/>",
        "\t\t\t<QuickChoice>true</QuickChoice>",
        "\t\t\t<ChoiceMode>BothWays</ChoiceMode>",
        "\t\t\t<DefaultListForm/>",
        "\t\t\t<DefaultChoiceForm/>",
        "\t\t\t<AuxiliaryListForm/>",
        "\t\t\t<AuxiliaryChoiceForm/>",
        "\t\t\t<ListPresentation/>",
        "\t\t\t<ExtendedListPresentation/>",
        "\t\t\t<Explanation/>",
        "\t\t\t<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>",
        "\t\t</Properties>",
        "\t\t<ChildObjects>",
    ]
    for value, value_title in values:
        body += [
            '\t\t\t<EnumValue uuid="%s">' % uid("Enum.%s.%s" % (name, value)),
            "\t\t\t\t<Properties>",
            "\t\t\t\t\t<Name>%s</Name>" % value,
            synonym(value_title, "\t\t\t\t\t"),
            "\t\t\t\t\t<Comment/>",
            "\t\t\t\t</Properties>",
            "\t\t\t</EnumValue>",
        ]
    body += ["\t\t</ChildObjects>", "\t</Enum>", "</MetaDataObject>\n"]
    write(os.path.join(SRC, "Enums", name + ".xml"), "\n".join(body))


def constant_xml(name, title, kind, ref=None, length=100, fraction=0, sign="Nonnegative", password=False):
    body = [HEADER, '\t<Constant uuid="%s">' % uid("Constant." + name)]
    body.append(generated([
        ("ConstantManager." + name, "Manager"),
        ("ConstantValueManager." + name, "ValueManager"),
        ("ConstantValueKey." + name, "ValueKey"),
    ]))
    body += [
        "\t\t<Properties>",
        "\t\t\t<Name>%s</Name>" % name,
        synonym(title, "\t\t\t"),
        "\t\t\t<Comment/>",
        type_xml(kind, ref, length, fraction, sign, "DateTime", "\t\t\t"),
        "\t\t\t<UseStandardCommands>true</UseStandardCommands>",
        "\t\t\t<DefaultForm/>",
        "\t\t\t<ExtendedPresentation/>",
        "\t\t\t<Explanation/>",
        "\t\t\t<PasswordMode>%s</PasswordMode>" % ("true" if password else "false"),
        "\t\t\t<Format/>",
        "\t\t\t<EditFormat/>",
        "\t\t\t<ToolTip/>",
        "\t\t\t<MarkNegatives>false</MarkNegatives>",
        "\t\t\t<Mask/>",
        "\t\t\t<MultiLine>false</MultiLine>",
        "\t\t\t<ExtendedEdit>false</ExtendedEdit>",
        '\t\t\t<MinValue xsi:nil="true"/>',
        '\t\t\t<MaxValue xsi:nil="true"/>',
        "\t\t\t<FillChecking>DontCheck</FillChecking>",
        "\t\t\t<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>",
        "\t\t\t<ChoiceParameterLinks/>",
        "\t\t\t<ChoiceParameters/>",
        "\t\t\t<QuickChoice>Auto</QuickChoice>",
        "\t\t\t<ChoiceForm/>",
        "\t\t\t<LinkByType/>",
        "\t\t\t<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>",
        "\t\t\t<DataLockControlMode>Managed</DataLockControlMode>",
        "\t\t\t<DataHistory>DontUse</DataHistory>",
        "\t\t</Properties>",
        "\t</Constant>",
        "</MetaDataObject>\n",
    ]
    write(os.path.join(SRC, "Constants", name + ".xml"), "\n".join(body))


def common_module(name, title):
    body = [
        HEADER,
        '\t<CommonModule uuid="%s">' % uid("CommonModule." + name),
        "\t\t<Properties>",
        "\t\t\t<Name>%s</Name>" % name,
        synonym(title, "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<Global>false</Global>",
        "\t\t\t<ClientManagedApplication>false</ClientManagedApplication>",
        "\t\t\t<Server>true</Server>",
        "\t\t\t<ExternalConnection>true</ExternalConnection>",
        "\t\t\t<ClientOrdinaryApplication>false</ClientOrdinaryApplication>",
        "\t\t\t<ServerCall>true</ServerCall>",
        "\t\t\t<Privileged>false</Privileged>",
        "\t\t\t<ReturnValuesReuse>DontUse</ReturnValuesReuse>",
        "\t\t</Properties>",
        "\t</CommonModule>",
        "</MetaDataObject>\n",
    ]
    write(os.path.join(SRC, "CommonModules", name + ".xml"), "\n".join(body))


def catalog_xml(name, title, attributes, sections=None):
    text = read_text(TEMPLATE_CATALOG)
    text = UUID_RE.sub(lambda match: uid("remap:" + name + ":" + match.group(0)), text)
    text = text.replace("Поставщики", name)
    text = text.replace("<v8:content>%s</v8:content>" % name, "<v8:content>%s</v8:content>" % escape(title), 1)
    blocks = [render_attribute(name, spec, for_catalog=True) for spec in attributes]
    for section_name, section_title, columns in sections or []:
        blocks.append("\t\t\t<TabularSection uuid=\"%s\">" % uid(name + "." + section_name))
        blocks.append(generated([
            ("CatalogTabularSection.%s.%s" % (name, section_name), "TabularSection"),
            ("CatalogTabularSectionRow.%s.%s" % (name, section_name), "TabularSectionRow"),
        ], "\t\t\t\t"))
        blocks += [
            "\t\t\t\t<Properties>",
            "\t\t\t\t\t<Name>%s</Name>" % section_name,
            synonym(section_title, "\t\t\t\t\t"),
            "\t\t\t\t\t<Comment/>",
            "\t\t\t\t\t<ToolTip/>",
            "\t\t\t\t\t<FillChecking>DontCheck</FillChecking>",
            "\t\t\t\t\t<Use>ForItem</Use>",
            "\t\t\t\t</Properties>",
            "\t\t\t\t<ChildObjects>",
        ]
        for column in columns:
            blocks.append(render_attribute(name + "." + section_name, column, tabular=True).replace("\t\t\t<", "\t\t\t\t\t<"))
        blocks += ["\t\t\t\t</ChildObjects>", "\t\t\t</TabularSection>"]
    start = text.index("\t\t<ChildObjects>")
    end = text.index("\t\t</ChildObjects>") + len("\t\t</ChildObjects>")
    text = text[:start] + "\t\t<ChildObjects>\n" + "\n".join(blocks) + "\n\t\t</ChildObjects>" + text[end:]
    write(os.path.join(SRC, "Catalogs", name + ".xml"), text)


def document_xml(name, title, attributes):
    body = [HEADER, '\t<Document uuid="%s">' % uid("Document." + name)]
    body.append(generated([
        ("DocumentObject." + name, "Object"),
        ("DocumentRef." + name, "Ref"),
        ("DocumentSelection." + name, "Selection"),
        ("DocumentList." + name, "List"),
        ("DocumentManager." + name, "Manager"),
    ]))
    body += [
        "\t\t<Properties>",
        "\t\t\t<Name>%s</Name>" % name,
        synonym(title, "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<UseStandardCommands>true</UseStandardCommands>",
        "\t\t\t<Numerator/>",
        "\t\t\t<NumberType>String</NumberType>",
        "\t\t\t<NumberLength>9</NumberLength>",
        "\t\t\t<NumberAllowedLength>Variable</NumberAllowedLength>",
        "\t\t\t<NumberPeriodicity>Year</NumberPeriodicity>",
        "\t\t\t<CheckUnique>true</CheckUnique>",
        "\t\t\t<Autonumbering>true</Autonumbering>",
        "\t\t\t<Characteristics/>",
        "\t\t\t<BasedOn/>",
        "\t\t\t<InputByString>",
        "\t\t\t\t<xr:Field>Document.%s.StandardAttribute.Number</xr:Field>" % name,
        "\t\t\t</InputByString>",
        "\t\t\t<SearchStringModeOnInputByString>Begin</SearchStringModeOnInputByString>",
        "\t\t\t<FullTextSearchOnInputByString>DontUse</FullTextSearchOnInputByString>",
        "\t\t\t<ChoiceDataGetModeOnInputByString>Directly</ChoiceDataGetModeOnInputByString>",
        "\t\t\t<DefaultObjectForm/>",
        "\t\t\t<DefaultListForm/>",
        "\t\t\t<DefaultChoiceForm/>",
        "\t\t\t<AuxiliaryObjectForm/>",
        "\t\t\t<AuxiliaryListForm/>",
        "\t\t\t<AuxiliaryChoiceForm/>",
        "\t\t\t<Posting>Deny</Posting>",
        "\t\t\t<RealTimePosting>Deny</RealTimePosting>",
        "\t\t\t<RegisterRecordsDeletion>AutoDeleteOnUnpost</RegisterRecordsDeletion>",
        "\t\t\t<RegisterRecordsWritingOnPost>WriteSelected</RegisterRecordsWritingOnPost>",
        "\t\t\t<SequenceFilling>AutoFillOff</SequenceFilling>",
        "\t\t\t<RegisterRecords/>",
        "\t\t\t<PostInPrivilegedMode>true</PostInPrivilegedMode>",
        "\t\t\t<UnpostInPrivilegedMode>true</UnpostInPrivilegedMode>",
        "\t\t\t<IncludeHelpInContents>false</IncludeHelpInContents>",
        "\t\t\t<DataLockFields/>",
        "\t\t\t<DataLockControlMode>Managed</DataLockControlMode>",
        "\t\t\t<FullTextSearch>Use</FullTextSearch>",
        "\t\t\t<ObjectPresentation/>",
        "\t\t\t<ExtendedObjectPresentation/>",
        "\t\t\t<ListPresentation/>",
        "\t\t\t<ExtendedListPresentation/>",
        "\t\t\t<Explanation/>",
        "\t\t\t<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>",
        "\t\t\t<DataHistory>DontUse</DataHistory>",
        "\t\t\t<UpdateDataHistoryImmediatelyAfterWrite>false</UpdateDataHistoryImmediatelyAfterWrite>",
        "\t\t\t<ExecuteAfterWriteDataHistoryVersionProcessing>false</ExecuteAfterWriteDataHistoryVersionProcessing>",
        "\t\t</Properties>",
        "\t\t<ChildObjects>",
    ]
    for spec in attributes:
        body.append(render_attribute(name, spec))
    body += ["\t\t</ChildObjects>", "\t</Document>", "</MetaDataObject>\n"]
    write(os.path.join(SRC, "Documents", name + ".xml"), "\n".join(body))


def field_block(kind, owner, spec):
    tag = {"dimension": "Dimension", "resource": "Resource", "attribute": "Attribute"}[kind]
    extra = ""
    if kind == "dimension":
        extra = (
            "\t\t\t\t\t<Master>false</Master>\n"
            "\t\t\t\t\t<MainFilter>true</MainFilter>\n"
            "\t\t\t\t\t<DenyIncompleteValues>true</DenyIncompleteValues>\n"
            "\t\t\t\t\t<TypeReductionMode>TransformValues</TypeReductionMode>\n"
        )
    multiline = spec.get("multiline") or (spec["kind"] == "string" and spec.get("length", 10) == 0)
    return "\n".join([
        '\t\t\t<%s uuid="%s">' % (tag, uid(owner + "." + kind + "." + spec["name"])),
        "\t\t\t\t<Properties>",
        "\t\t\t\t\t<Name>%s</Name>" % spec["name"],
        synonym(spec["title"], "\t\t\t\t\t"),
        "\t\t\t\t\t<Comment/>",
        type_xml(spec["kind"], spec.get("ref"), spec.get("length", 10), spec.get("fraction", 0),
                 spec.get("sign", "Nonnegative"), spec.get("date", "DateTime")),
        "\t\t\t\t\t<PasswordMode>false</PasswordMode>",
        "\t\t\t\t\t<Format/>",
        "\t\t\t\t\t<EditFormat/>",
        "\t\t\t\t\t<ToolTip/>",
        "\t\t\t\t\t<MarkNegatives>false</MarkNegatives>",
        "\t\t\t\t\t<Mask/>",
        "\t\t\t\t\t<MultiLine>%s</MultiLine>" % ("true" if multiline else "false"),
        "\t\t\t\t\t<ExtendedEdit>%s</ExtendedEdit>" % ("true" if multiline else "false"),
        '\t\t\t\t\t<MinValue xsi:nil="true"/>',
        '\t\t\t\t\t<MaxValue xsi:nil="true"/>',
        "\t\t\t\t\t<FillFromFillingValue>false</FillFromFillingValue>",
        fill_value(spec["kind"], "\t\t\t\t\t"),
        "\t\t\t\t\t<FillChecking>DontCheck</FillChecking>",
        "\t\t\t\t\t<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>",
        "\t\t\t\t\t<ChoiceParameterLinks/>",
        "\t\t\t\t\t<ChoiceParameters/>",
        "\t\t\t\t\t<QuickChoice>Auto</QuickChoice>",
        "\t\t\t\t\t<CreateOnInput>Auto</CreateOnInput>",
        "\t\t\t\t\t<ChoiceForm/>",
        "\t\t\t\t\t<LinkByType/>",
        "\t\t\t\t\t<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>",
        "\t\t\t\t\t<Indexing>%s</Indexing>" % ("Index" if kind == "dimension" else "DontIndex"),
        "\t\t\t\t\t<FullTextSearch>DontUse</FullTextSearch>",
        "\t\t\t\t\t<DataHistory>DontUse</DataHistory>",
        extra.rstrip("\n"),
        "\t\t\t\t</Properties>",
        "\t\t\t</%s>" % tag,
    ])


def register_xml(name, title, dimensions, resources, attributes):
    body = [HEADER, '\t<InformationRegister uuid="%s">' % uid("InformationRegister." + name)]
    body.append(generated([
        ("InformationRegisterRecord." + name, "Record"),
        ("InformationRegisterManager." + name, "Manager"),
        ("InformationRegisterSelection." + name, "Selection"),
        ("InformationRegisterList." + name, "List"),
        ("InformationRegisterRecordSet." + name, "RecordSet"),
        ("InformationRegisterRecordKey." + name, "RecordKey"),
        ("InformationRegisterRecordManager." + name, "RecordManager"),
    ]))
    body += [
        "\t\t<Properties>",
        "\t\t\t<Name>%s</Name>" % name,
        synonym(title, "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<UseStandardCommands>true</UseStandardCommands>",
        "\t\t\t<EditType>InDialog</EditType>",
        "\t\t\t<DefaultRecordForm/>",
        "\t\t\t<DefaultListForm/>",
        "\t\t\t<AuxiliaryRecordForm/>",
        "\t\t\t<AuxiliaryListForm/>",
        "\t\t\t<InformationRegisterPeriodicity>Nonperiodical</InformationRegisterPeriodicity>",
        "\t\t\t<WriteMode>Independent</WriteMode>",
        "\t\t\t<MainFilterOnPeriod>false</MainFilterOnPeriod>",
        "\t\t\t<IncludeHelpInContents>false</IncludeHelpInContents>",
        "\t\t\t<DataLockControlMode>Managed</DataLockControlMode>",
        "\t\t\t<FullTextSearch>DontUse</FullTextSearch>",
        "\t\t\t<EnableTotalsSliceFirst>false</EnableTotalsSliceFirst>",
        "\t\t\t<EnableTotalsSliceLast>false</EnableTotalsSliceLast>",
        "\t\t\t<RecordPresentation/>",
        "\t\t\t<ExtendedRecordPresentation/>",
        "\t\t\t<ListPresentation/>",
        "\t\t\t<ExtendedListPresentation/>",
        "\t\t\t<Explanation/>",
        "\t\t\t<DataHistory>DontUse</DataHistory>",
        "\t\t\t<UpdateDataHistoryImmediatelyAfterWrite>false</UpdateDataHistoryImmediatelyAfterWrite>",
        "\t\t\t<ExecuteAfterWriteDataHistoryVersionProcessing>false</ExecuteAfterWriteDataHistoryVersionProcessing>",
        "\t\t</Properties>",
        "\t\t<ChildObjects>",
    ]
    for spec in dimensions:
        body.append(field_block("dimension", name, spec))
    for spec in resources:
        body.append(field_block("resource", name, spec))
    for spec in attributes:
        body.append(field_block("attribute", name, spec))
    body += ["\t\t</ChildObjects>", "\t</InformationRegister>", "</MetaDataObject>\n"]
    write(os.path.join(SRC, "InformationRegisters", name + ".xml"), "\n".join(body))


def processor_xml(name, title):
    body = [
        HEADER,
        '\t<DataProcessor uuid="%s">' % uid("DataProcessor." + name),
        generated([
            ("DataProcessorObject." + name, "Object"),
            ("DataProcessorManager." + name, "Manager"),
        ]),
        "\t\t<Properties>",
        "\t\t\t<Name>%s</Name>" % name,
        synonym(title, "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<UseStandardCommands>true</UseStandardCommands>",
        "\t\t\t<DefaultForm>DataProcessor.%s.Form.Форма</DefaultForm>" % name,
        "\t\t\t<AuxiliaryForm/>",
        "\t\t\t<IncludeHelpInContents>false</IncludeHelpInContents>",
        "\t\t\t<ExtendedPresentation/>",
        "\t\t\t<Explanation/>",
        "\t\t</Properties>",
        "\t\t<ChildObjects>",
        "\t\t\t<Form>Форма</Form>",
        "\t\t</ChildObjects>",
        "\t</DataProcessor>",
        "</MetaDataObject>\n",
    ]
    write(os.path.join(SRC, "DataProcessors", name + ".xml"), "\n".join(body))
    form_meta = [
        HEADER,
        '\t<Form uuid="%s">' % uid("Form." + name),
        "\t\t<Properties>",
        "\t\t\t<Name>Форма</Name>",
        synonym("Форма", "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<FormType>Managed</FormType>",
        "\t\t\t<IncludeHelpInContents>false</IncludeHelpInContents>",
        "\t\t\t<UsePurposes>",
        '\t\t\t\t<v8:Value xsi:type="app:ApplicationUsePurpose">PlatformApplication</v8:Value>',
        "\t\t\t</UsePurposes>",
        "\t\t\t<ExtendedPresentation/>",
        "\t\t</Properties>",
        "\t</Form>",
        "</MetaDataObject>\n",
    ]
    write(os.path.join(SRC, "DataProcessors", name, "Forms", "Форма.xml"), "\n".join(form_meta))


def http_service():
    body = [
        HEADER,
        '\t<HTTPService uuid="%s">' % uid("HTTPService.ПриемОбращений"),
        "\t\t<Properties>",
        "\t\t\t<Name>ПриемОбращений</Name>",
        synonym("Прием обращений", "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<RootURL>appeals</RootURL>",
        "\t\t\t<ReuseSessions>AutoUse</ReuseSessions>",
        "\t\t\t<SessionMaxAge>20</SessionMaxAge>",
        "\t\t</Properties>",
        "\t\t<ChildObjects>",
        '\t\t\t<URLTemplate uuid="%s">' % uid("HTTPService.ПриемОбращений.Создать"),
        "\t\t\t\t<Properties>",
        "\t\t\t\t\t<Name>Создать</Name>",
        synonym("Создать", "\t\t\t\t\t"),
        "\t\t\t\t\t<Comment/>",
        "\t\t\t\t\t<Template>/create</Template>",
        "\t\t\t\t</Properties>",
        "\t\t\t\t<ChildObjects>",
        '\t\t\t\t\t<Method uuid="%s">' % uid("HTTPService.ПриемОбращений.Создать.POST"),
        "\t\t\t\t\t\t<Properties>",
        "\t\t\t\t\t\t\t<Name>POST</Name>",
        synonym("POST", "\t\t\t\t\t\t\t"),
        "\t\t\t\t\t\t\t<Comment/>",
        "\t\t\t\t\t\t\t<HTTPMethod>POST</HTTPMethod>",
        "\t\t\t\t\t\t\t<Handler>Создать</Handler>",
        "\t\t\t\t\t\t</Properties>",
        "\t\t\t\t\t</Method>",
        "\t\t\t\t</ChildObjects>",
        "\t\t\t</URLTemplate>",
        '\t\t\t<URLTemplate uuid="%s">' % uid("HTTPService.ПриемОбращений.Статус"),
        "\t\t\t\t<Properties>",
        "\t\t\t\t\t<Name>Статус</Name>",
        synonym("Статус", "\t\t\t\t\t"),
        "\t\t\t\t\t<Comment/>",
        "\t\t\t\t\t<Template>/status</Template>",
        "\t\t\t\t</Properties>",
        "\t\t\t\t<ChildObjects>",
        '\t\t\t\t\t<Method uuid="%s">' % uid("HTTPService.ПриемОбращений.Статус.GET"),
        "\t\t\t\t\t\t<Properties>",
        "\t\t\t\t\t\t\t<Name>GET</Name>",
        synonym("GET", "\t\t\t\t\t\t\t"),
        "\t\t\t\t\t\t\t<Comment/>",
        "\t\t\t\t\t\t\t<HTTPMethod>GET</HTTPMethod>",
        "\t\t\t\t\t\t\t<Handler>Статус</Handler>",
        "\t\t\t\t\t\t</Properties>",
        "\t\t\t\t\t</Method>",
        "\t\t\t\t</ChildObjects>",
        "\t\t\t</URLTemplate>",
        "\t\t</ChildObjects>",
        "\t</HTTPService>",
        "</MetaDataObject>\n",
    ]
    write(os.path.join(SRC, "HTTPServices", "ПриемОбращений.xml"), "\n".join(body))


def scheduled_job():
    body = [
        HEADER,
        '\t<ScheduledJob uuid="%s">' % uid("ScheduledJob.ПолучениеПочты"),
        "\t\t<Properties>",
        "\t\t\t<Name>ПолучениеПочты</Name>",
        synonym("Получение почты", "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<MethodName>CommonModule.РаботаСПочтой.ПолучитьВходящиеРегламент</MethodName>",
        "\t\t\t<Description>Получение новых писем IMAP</Description>",
        "\t\t\t<Key/>",
        "\t\t\t<Use>false</Use>",
        "\t\t\t<Predefined>true</Predefined>",
        "\t\t\t<RestartCountOnFailure>3</RestartCountOnFailure>",
        "\t\t\t<RestartIntervalOnFailure>10</RestartIntervalOnFailure>",
        "\t\t</Properties>",
        "\t</ScheduledJob>",
        "</MetaDataObject>\n",
    ]
    write(os.path.join(SRC, "ScheduledJobs", "ПолучениеПочты.xml"), "\n".join(body))


def role_file(name, title, rights_text):
    body = [
        HEADER,
        '\t<Role uuid="%s">' % uid("Role." + name),
        "\t\t<Properties>",
        "\t\t\t<Name>%s</Name>" % name,
        synonym(title, "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t</Properties>",
        "\t</Role>",
        "</MetaDataObject>\n",
    ]
    write(os.path.join(SRC, "Roles", name + ".xml"), "\n".join(body))
    write(os.path.join(SRC, "Roles", name, "Ext", "Rights.xml"), rights_text)


def rights_document(objects, for_new):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Rights xmlns="http://v8.1c.ru/8.2/roles" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Rights" version="2.18">',
        "\t<setForNewObjects>%s</setForNewObjects>" % ("true" if for_new else "false"),
        "\t<setForAttributesByDefault>true</setForAttributesByDefault>",
        "\t<independentRightsOfChildObjects>false</independentRightsOfChildObjects>",
    ]
    for object_name, rights in objects:
        lines.append("\t<object>")
        lines.append("\t\t<name>%s</name>" % object_name)
        for right in rights:
            lines.append("\t\t<right><name>%s</name><value>true</value></right>" % right)
        lines.append("\t</object>")
    lines += ["</Rights>", ""]
    return "\n".join(lines)


def subsystem_xml(content_names):
    body = [
        HEADER,
        '\t<Subsystem uuid="%s">' % uid("Subsystem.ЦентрОбращений"),
        "\t\t<Properties>",
        "\t\t\t<Name>ЦентрОбращений</Name>",
        synonym("Центр обращений", "\t\t\t"),
        "\t\t\t<Comment/>",
        "\t\t\t<IncludeHelpInContents>true</IncludeHelpInContents>",
        "\t\t\t<IncludeInCommandInterface>true</IncludeInCommandInterface>",
        "\t\t\t<UseOneCommand>false</UseOneCommand>",
        "\t\t\t<Explanation/>",
        "\t\t\t<Picture/>",
        "\t\t\t<Content>",
    ]
    for item in content_names:
        body.append('\t\t\t\t<xr:Item xsi:type="xr:MDObjectRef">%s</xr:Item>' % item)
    body += ["\t\t\t</Content>", "\t\t</Properties>", "\t\t<ChildObjects/>", "\t</Subsystem>", "</MetaDataObject>\n"]
    write(os.path.join(SRC, "Subsystems", "ЦентрОбращений.xml"), "\n".join(body))
    commands = [
        ("DataProcessor.НачальнаяСтраница.StandardCommand.Open", "NavigationPanelImportant"),
        ("DataProcessor.РабочееМестоОператора.StandardCommand.Open", "NavigationPanelImportant"),
        ("DataProcessor.ПанельРуководителя.StandardCommand.Open", "NavigationPanelImportant"),
        ("Document.Обращение.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("Catalog.Контрагенты.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("Catalog.Договоры.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("Catalog.Сотрудники.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("Catalog.Номенклатура.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("Catalog.КатегорииОбращений.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("Catalog.УчетныеЗаписиПочты.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("InformationRegister.ЖурналВызововИИ.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("InformationRegister.ИсправленияКлассификации.StandardCommand.OpenList", "NavigationPanelOrdinary"),
        ("DataProcessor.НастройкиПодключения.StandardCommand.Open", "NavigationPanelSeeAlso"),
    ]
    rows = ["\t<CommandsPlacement>"]
    for name, group in commands:
        rows.append('\t\t<Command name="%s">' % name)
        rows.append("\t\t\t<CommandGroup>%s</CommandGroup>" % group)
        rows.append("\t\t\t<Placement>Auto</Placement>")
        rows.append("\t\t</Command>")
    rows.append("\t</CommandsPlacement>")
    rows.append("\t<CommandsOrder>")
    for name, group in commands:
        rows.append('\t\t<Command name="%s">' % name)
        rows.append("\t\t\t<CommandGroup>%s</CommandGroup>" % group)
        rows.append("\t\t</Command>")
    rows.append("\t</CommandsOrder>")
    write(os.path.join(SRC, "Subsystems", "ЦентрОбращений", "Ext", "CommandInterface.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n<CommandInterface xmlns="http://v8.1c.ru/8.3/xcf/extrnprops" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.18">\n'
          + "\n".join(rows) + "\n</CommandInterface>\n")


def patch_configuration(children):
    text = read_text(TEMPLATE_CONFIG)
    text = text.replace("АссистентКомиссии", "ЦентрОбращений")
    text = text.replace("Ассистент комиссии", "Центр интеллектуальной обработки клиентских обращений")
    child_xml = "\n".join("\t\t\t<%s>%s</%s>" % (kind, name, kind) for kind, name in children)
    start = text.index("<ChildObjects>")
    end = text.index("</ChildObjects>") + len("</ChildObjects>")
    text = text[:start] + "<ChildObjects>\n" + child_xml + "\n\t\t</ChildObjects>" + text[end:]
    write(os.path.join(SRC, "Configuration.xml"), text)
    write(os.path.join(SRC, "Languages", "Русский.xml"), read_text(TEMPLATE_LANG))


def interface_files():
    write(os.path.join(SRC, "Ext", "CommandInterface.xml"), '''<?xml version="1.0" encoding="UTF-8"?>
<CommandInterface xmlns="http://v8.1c.ru/8.3/xcf/extrnprops" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.18">
	<SubsystemsOrder>
		<Subsystem>Subsystem.ЦентрОбращений</Subsystem>
	</SubsystemsOrder>
</CommandInterface>
''')
    write(os.path.join(SRC, "Ext", "HomePageWorkArea.xml"), '''<?xml version="1.0" encoding="UTF-8"?>
<HomePageWorkArea xmlns="http://v8.1c.ru/8.3/xcf/extrnprops" xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.18">
	<WorkingAreaTemplate>OneColumn</WorkingAreaTemplate>
	<Column>
		<Item>
			<Form>DataProcessor.НачальнаяСтраница.Form.Форма</Form>
			<Height>10</Height>
			<Visibility>
				<xr:Common>true</xr:Common>
			</Visibility>
		</Item>
	</Column>
</HomePageWorkArea>
''')
    write(os.path.join(SRC, "ConfigDumpInfo.xml"), '''<?xml version="1.0" encoding="UTF-8"?>
<ConfigDumpInfo xmlns="http://v8.1c.ru/8.3/xcf/dumpinfo" xmlns:xen="http://v8.1c.ru/8.3/xcf/enums" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" format="Hierarchical" version="2.18">
	<ConfigVersions/>
</ConfigDumpInfo>
''')
    write(os.path.join(SRC, "Ext", "ManagedApplicationModule.bsl"), """Процедура ПриНачалеРаботыСистемы()
	
	Если ПараметрЗапуска = "Самопроверка" Тогда
		ПодключитьОбработчикОжидания("ЗапуститьСамопроверку", 0.1, Истина);
	ИначеЕсли ПараметрЗапуска = "Демо" Тогда
		ПодключитьОбработчикОжидания("ЗаполнитьДемоИЗавершить", 0.1, Истина);
	КонецЕсли;
	
КонецПроцедуры

Процедура ЗапуститьСамопроверку() Экспорт
	
	Текст = ОбработкаОбращений.Самопроверка();
	Запись = Новый ТекстовыйДокумент;
	Запись.УстановитьТекст(Текст);
	Запись.Записать("C:\\Users\\Dan\\1c-marathon\\appeals\\selfcheck.txt", КодировкаТекста.UTF8);
	ЗавершитьРаботуСистемы(Ложь);
	
КонецПроцедуры

Процедура ЗаполнитьДемоИЗавершить() Экспорт
	
	Попытка
		ДемонстрационныеДанные.Заполнить();
	Исключение
		Запись = Новый ТекстовыйДокумент;
		Запись.УстановитьТекст(ПодробноеПредставлениеОшибки(ИнформацияОбОшибке()));
		Запись.Записать("C:\\Users\\Dan\\1c-marathon\\appeals\\demo-error.txt", КодировкаТекста.UTF8);
	КонецПопытки;
	ЗавершитьРаботуСистемы(Ложь);
	
КонецПроцедуры
""")


class FormBuilder(object):
    def __init__(self, title):
        self.title = title
        self.items = []
        self.attributes = []
        self.commands = []
        self._id = 10

    def nid(self):
        self._id += 1
        return self._id

    def decoration(self, name, text):
        item_id = self.nid()
        self.items.append(
            '\t\t<LabelDecoration name="%s" id="%s">\n'
            '\t\t\t<Title formatted="false">\n%s\n\t\t\t</Title>\n'
            '\t\t\t<ContextMenu name="%sКонтекстноеМеню" id="%s"/>\n'
            '\t\t\t<ExtendedTooltip name="%sРасширеннаяПодсказка" id="%s"/>\n'
            '\t\t</LabelDecoration>' % (name, item_id, syn_item(text, "\t\t\t\t"), name, self.nid(), name, self.nid())
        )

    def field(self, name, path, title, kind, ref=None, length=0, fraction=0, sign="Nonnegative",
              multiline=False, password=False, read_only=False):
        item_id = self.nid()
        extra = ""
        if password:
            extra += "\t\t\t<PasswordMode>true</PasswordMode>\n"
        if read_only:
            extra += "\t\t\t<ReadOnly>true</ReadOnly>\n"
        if multiline:
            extra += "\t\t\t<AutoMaxHeight>false</AutoMaxHeight>\n\t\t\t<Height>4</Height>\n\t\t\t<MultiLine>true</MultiLine>\n"
        self.items.append(
            '\t\t<InputField name="%s" id="%s">\n'
            '\t\t\t<DataPath>%s</DataPath>\n'
            '%s'
            '\t\t\t<ContextMenu name="%sКонтекстноеМеню" id="%s"/>\n'
            '\t\t\t<ExtendedTooltip name="%sРасширеннаяПодсказка" id="%s"/>\n'
            '\t\t</InputField>' % (name, item_id, path, extra, name, self.nid(), name, self.nid())
        )
        self.attributes.append(self._attribute(name, title, kind, ref, length, fraction, sign))

    def check(self, name, path, title):
        item_id = self.nid()
        self.items.append(
            '\t\t<CheckBoxField name="%s" id="%s">\n'
            '\t\t\t<DataPath>%s</DataPath>\n'
            '\t\t\t<TitleLocation>Right</TitleLocation>\n'
            '\t\t\t<CheckBoxType>Auto</CheckBoxType>\n'
            '\t\t\t<ContextMenu name="%sКонтекстноеМеню" id="%s"/>\n'
            '\t\t\t<ExtendedTooltip name="%sРасширеннаяПодсказка" id="%s"/>\n'
            '\t\t</CheckBoxField>' % (name, item_id, path, name, self.nid(), name, self.nid())
        )
        self.attributes.append(self._attribute(name, title, "boolean"))

    def buttons(self, pairs):
        children = []
        for name, title, action in pairs:
            item_id = self.nid()
            children.append(
                '\t\t\t\t<Button name="%s" id="%s">\n'
                '\t\t\t\t\t<Type>UsualButton</Type>\n'
                '\t\t\t\t\t<CommandName>Form.Command.%s</CommandName>\n'
                '\t\t\t\t\t<ExtendedTooltip name="%sРасширеннаяПодсказка" id="%s"/>\n'
                '\t\t\t\t</Button>' % (name, item_id, name, name, self.nid())
            )
            self.commands.append((name, title, action))
        group_id = self.nid()
        self.items.append(
            '\t\t<UsualGroup name="Группа%s" id="%s">\n'
            '\t\t\t<Group>AlwaysHorizontal</Group>\n'
            '\t\t\t<Representation>None</Representation>\n'
            '\t\t\t<ShowTitle>false</ShowTitle>\n'
            '\t\t\t<ExtendedTooltip name="Группа%sРасширеннаяПодсказка" id="%s"/>\n'
            '\t\t\t<ChildItems>\n%s\n\t\t\t</ChildItems>\n'
            '\t\t</UsualGroup>' % (group_id, group_id, group_id, self.nid(), "\n".join(children))
        )

    def table(self, name, title, columns):
        item_id = self.nid()
        fields = []
        col_xml = []
        col_id = 1
        for col_name, col_title, kind, ref, length in columns:
            field_id = self.nid()
            fields.append(
                '\t\t\t\t<InputField name="%s%s" id="%s">\n'
                '\t\t\t\t\t<DataPath>%s.%s</DataPath>\n'
                '\t\t\t\t\t<ContextMenu name="%s%sКонтекстноеМеню" id="%s"/>\n'
                '\t\t\t\t\t<ExtendedTooltip name="%s%sРасширеннаяПодсказка" id="%s"/>\n'
                '\t\t\t\t</InputField>' % (name, col_name, field_id, name, col_name, name, col_name, self.nid(), name, col_name, self.nid())
            )
            col_xml.append(
                '\t\t\t<Column name="%s" id="%s">\n'
                '%s\n'
                '%s\n'
                '\t\t\t</Column>' % (col_name, col_id, self._title(col_title, "\t\t\t\t"), self._type(kind, ref, length, 0, "Nonnegative", "\t\t\t\t"))
            )
            col_id += 1
        additions = []
        for suffix in ("СтрокаПоиска", "СостояниеПросмотра", "УправлениеПоиском"):
            additions.append(
                '\t\t\t<%s name="%s%s" id="%s">\n'
                '\t\t\t\t<ContextMenu name="%s%sКонтекстноеМеню" id="%s"/>\n'
                '\t\t\t\t<ExtendedTooltip name="%s%sРасширеннаяПодсказка" id="%s"/>\n'
                '\t\t\t</%s>' % (
                    {"СтрокаПоиска": "SearchStringAddition", "СостояниеПросмотра": "ViewStatusAddition", "УправлениеПоиском": "SearchControlAddition"}[suffix],
                    name, suffix, self.nid(), name, suffix, self.nid(), name, suffix, self.nid(),
                    {"СтрокаПоиска": "SearchStringAddition", "СостояниеПросмотра": "ViewStatusAddition", "УправлениеПоиском": "SearchControlAddition"}[suffix],
                )
            )
        event = ""
        if name == "Очередь":
            event = '\t\t\t<Events>\n\t\t\t\t<Event name="OnActivateRow">ОчередьПриАктивизацииСтроки</Event>\n\t\t\t</Events>\n'
        self.items.append(
            '\t\t<Table name="%s" id="%s">\n'
            '\t\t\t<DataPath>%s</DataPath>\n'
            '\t\t\t<ContextMenu name="%sКонтекстноеМеню" id="%s"/>\n'
            '\t\t\t<AutoCommandBar name="%sКоманднаяПанель" id="%s"/>\n'
            '%s\n%s'
            '\t\t\t<ChildItems>\n%s\n\t\t\t</ChildItems>\n'
            '\t\t</Table>' % (name, item_id, name, name, self.nid(), name, self.nid(), "\n".join(additions), event, "\n".join(fields))
        )
        self.attributes.append(
            '\t\t<Attribute name="%s" id="%s">\n'
            '%s\n'
            '\t\t\t<Type>\n\t\t\t\t<v8:Type>v8:ValueTable</v8:Type>\n\t\t\t</Type>\n'
            '\t\t\t<Columns>\n%s\n\t\t\t</Columns>\n'
            '\t\t</Attribute>' % (name, self.nid(), self._title(title, "\t\t\t"), "\n".join(col_xml))
        )

    def _title(self, title, indent):
        return "%s<Title>\n%s\n%s</Title>" % (indent, syn_item(title, indent + "\t"), indent)

    def _type(self, kind, ref, length, fraction, sign, indent):
        if kind == "string":
            return (
                "%s<Type>\n%s\t<v8:Type>xs:string</v8:Type>\n%s\t<v8:StringQualifiers>\n"
                "%s\t\t<v8:Length>%s</v8:Length>\n%s\t\t<v8:AllowedLength>Variable</v8:AllowedLength>\n"
                "%s\t</v8:StringQualifiers>\n%s</Type>" % (indent, indent, indent, indent, length, indent, indent, indent)
            )
        if kind == "number":
            return (
                "%s<Type>\n%s\t<v8:Type>xs:decimal</v8:Type>\n%s\t<v8:NumberQualifiers>\n"
                "%s\t\t<v8:Digits>10</v8:Digits>\n%s\t\t<v8:FractionDigits>%s</v8:FractionDigits>\n"
                "%s\t\t<v8:AllowedSign>%s</v8:AllowedSign>\n%s\t</v8:NumberQualifiers>\n%s</Type>"
                % (indent, indent, indent, indent, indent, fraction, indent, sign, indent, indent)
            )
        if kind == "boolean":
            return "%s<Type>\n%s\t<v8:Type>xs:boolean</v8:Type>\n%s</Type>" % (indent, indent, indent)
        return "%s<Type>\n%s\t<v8:Type>%s</v8:Type>\n%s</Type>" % (indent, indent, ref, indent)

    def _attribute(self, name, title, kind, ref=None, length=0, fraction=0, sign="Nonnegative"):
        return (
            '\t\t<Attribute name="%s" id="%s">\n%s\n%s\n\t\t</Attribute>'
            % (name, self.nid(), self._title(title, "\t\t\t"), self._type(kind, ref, length, fraction, sign, "\t\t\t"))
        )

    def xml(self):
        commands = []
        for name, title, action in self.commands:
            commands.append(
                '\t\t<Command name="%s" id="%s">\n%s\n\t\t\t<Action>%s</Action>\n\t\t</Command>'
                % (name, self.nid(), self._title(title, "\t\t\t"), action)
            )
        title = "\t<Title>\n%s\n\t</Title>\n" % syn_item(self.title, "\t\t")
        return (
            FORM_NS +
            title +
            "\t<AutoTitle>false</AutoTitle>\n"
            '\t<AutoCommandBar name="ФормаКоманднаяПанель" id="-1"/>\n'
            '\t<Events>\n\t\t<Event name="OnCreateAtServer">ПриСозданииНаСервере</Event>\n\t</Events>\n'
            "\t<ChildItems>\n" + "\n".join(self.items) + "\n\t</ChildItems>\n"
            "\t<Attributes>\n" + "\n".join(self.attributes) + "\n\t</Attributes>\n"
            "\t<Commands>\n" + "\n".join(commands) + "\n\t</Commands>\n</Form>\n"
        )


def write_forms():
    home = FormBuilder("Центр обращений")
    home.decoration("Пояснение", "ТехноСервис. Оператор ведёт очередь и ответы. Руководитель смотрит панель. Ключ модели вводит администратор в настройках подключения.")
    home.buttons([
        ("ОткрытьОчередь", "Очередь оператора", "ОткрытьОчередь"),
        ("ОткрытьПанель", "Панель руководителя", "ОткрытьПанель"),
        ("ОткрытьНастройки", "Настройки модели", "ОткрытьНастройки"),
        ("ЗаполнитьДемо", "Заполнить демо-данные", "ЗаполнитьДемо"),
    ])
    write(os.path.join(SRC, "DataProcessors", "НачальнаяСтраница", "Forms", "Форма", "Ext", "Form.xml"), home.xml())

    settings = FormBuilder("Настройки подключения к модели")
    settings.decoration("Пояснение", "YandexGPT и GigaChat — готовые контуры. OpenAI-совместимый адрес принимает любую модель с тем же JSON. Ключ хранится в константе и в журнал не пишется.")
    settings.field("ВидПодключенияИИ", "ВидПодключенияИИ", "Вид подключения", "ref", "cfg:EnumRef.ВидыПодключенияИИ")
    settings.field("КлючAPI", "КлючAPI", "Ключ API", "string", length=500, password=True)
    settings.field("ИдентификаторКаталога", "ИдентификаторКаталога", "Идентификатор каталога Yandex", "string", length=80)
    settings.field("ИмяМодели", "ИмяМодели", "Модель", "string", length=150)
    settings.field("АдресAPI", "АдресAPI", "Адрес API", "string", length=300)
    settings.field("СхемаАвторизации", "СхемаАвторизации", "Схема авторизации", "string", length=40)
    settings.field("ОбластьДоступаGigaChat", "ОбластьДоступаGigaChat", "Scope GigaChat", "string", length=80)
    settings.field("ТаймаутСекунд", "ТаймаутСекунд", "Таймаут, секунд", "number")
    settings.field("МаксимумТокенов", "МаксимумТокенов", "Максимум токенов", "number")
    settings.field("Температура", "Температура", "Температура", "number", fraction=2, sign="Any")
    settings.field("КоличествоПримеров", "КоличествоПримеров", "Примеров в промпте", "number")
    settings.check("ОбезличиватьПередОтправкой", "ОбезличиватьПередОтправкой", "Обезличивать обращение перед отправкой")
    settings.buttons([
        ("Сохранить", "Сохранить", "Сохранить"),
        ("ПроверитьСоединение", "Проверить соединение", "ПроверитьСоединение"),
        ("ЗначенияПоУмолчанию", "Значения по умолчанию", "ЗначенияПоУмолчанию"),
    ])
    settings.field("РезультатПроверки", "РезультатПроверки", "Результат", "string", multiline=True, read_only=True)
    write(os.path.join(SRC, "DataProcessors", "НастройкиПодключения", "Forms", "Форма", "Ext", "Form.xml"), settings.xml())

    panel = FormBuilder("Панель руководителя")
    panel.decoration("Пояснение", "Объём за день и неделю, доли категорий, среднее время до ответа, точность модели по подтверждениям оператора, необработанные и узкие места.")
    panel.buttons([
        ("ЗаСегодня", "За сегодня", "ЗаСегодня"),
        ("ЗаНеделю", "За 7 дней", "ЗаНеделю"),
    ])
    panel.field("Сводка", "Сводка", "Сводка", "string", multiline=True, read_only=True)
    write(os.path.join(SRC, "DataProcessors", "ПанельРуководителя", "Forms", "Форма", "Ext", "Form.xml"), panel.xml())

    desk = FormBuilder("Рабочее место оператора")
    desk.decoration("Пояснение", "Почта забирается по IMAP, веб-форма пишет в тот же документ, звонок вставляется текстом расшифровки. Ответ на почту уходит письмом, ответ формы публикуется по номеру обращения и дублируется на почту, если адрес есть. По звонку фиксируется, что клиенту сообщили.")
    desk.field("Канал", "Канал", "Канал", "ref", "cfg:EnumRef.КаналыОбращений")
    desk.field("Контрагент", "Контрагент", "Контрагент", "ref", "cfg:CatalogRef.Контрагенты")
    desk.field("Тема", "Тема", "Тема", "string", length=200)
    desk.field("АдресОтвета", "АдресОтвета", "Адрес для ответа", "string", length=150)
    desk.field("Текст", "Текст", "Текст обращения", "string", multiline=True)
    desk.buttons([
        ("Принять", "Принять обращение", "Принять"),
        ("ПринятьВебФорму", "Принять как веб-форму", "ПринятьВебФорму"),
        ("ПолучитьПочту", "Получить почту", "ПолучитьПочту"),
        ("Обновить", "Обновить очередь", "Обновить"),
    ])
    desk.table("Задачи", "Задачи на сегодня", [
        ("Номер", "Номер", "string", None, 12),
        ("Приоритет", "Приоритет", "number", None, 1),
        ("Уровень", "Уровень", "string", None, 40),
        ("Тема", "Тема", "string", None, 200),
        ("Исполнитель", "Исполнитель", "string", None, 150),
        ("Ожидание", "Ожидание, ч", "number", None, 10),
        ("Ссылка", "Ссылка", "ref", "cfg:DocumentRef.Обращение", 0),
    ])
    desk.table("Очередь", "Очередь", [
        ("Номер", "Номер", "string", None, 12),
        ("Канал", "Канал", "string", None, 40),
        ("Контрагент", "Контрагент", "string", None, 150),
        ("Категория", "Категория", "string", None, 150),
        ("Приоритет", "Приоритет", "number", None, 1),
        ("Тональность", "Тональность", "string", None, 40),
        ("Исполнитель", "Исполнитель", "string", None, 150),
        ("Статус", "Статус", "string", None, 40),
        ("Ссылка", "Ссылка", "ref", "cfg:DocumentRef.Обращение", 0),
    ])
    desk.field("ТекущееПредставление", "ТекущееПредставление", "Выбранное обращение", "string", length=300, read_only=True)
    desk.field("Категория", "Категория", "Категория", "ref", "cfg:CatalogRef.КатегорииОбращений")
    desk.field("Тональность", "Тональность", "Тональность", "ref", "cfg:EnumRef.ТональностьОбращения")
    desk.field("Приоритет", "Приоритет", "Приоритет", "number")
    desk.field("Исполнитель", "Исполнитель", "Исполнитель", "ref", "cfg:CatalogRef.Сотрудники")
    desk.field("Пояснение", "Пояснение", "Пояснение", "string", multiline=True, read_only=True)
    desk.field("ЧерновикОтвета", "ЧерновикОтвета", "Черновик ответа", "string", multiline=True)
    desk.check("ТакжеНаПочту", "ТакжеНаПочту", "По звонку дополнительно отправить текст на почту")
    desk.buttons([
        ("Классифицировать", "Классифицировать", "Классифицировать"),
        ("Подтвердить", "Подтвердить исправления", "Подтвердить"),
        ("Черновик", "Черновик по номенклатуре", "Черновик"),
        ("Отправить", "Отправить ответ", "Отправить"),
        ("Сообщено", "Ответ сообщён по звонку", "Сообщено"),
        ("ОткрытьДокумент", "Открыть документ", "ОткрытьДокумент"),
    ])
    desk.field("Сообщение", "Сообщение", "Сообщение", "string", multiline=True, read_only=True)
    desk.attributes.append(desk._attribute("ТекущееОбращение", "Текущее обращение", "ref", "cfg:DocumentRef.Обращение"))
    write(os.path.join(SRC, "DataProcessors", "РабочееМестоОператора", "Forms", "Форма", "Ext", "Form.xml"), desk.xml())


def spec(name, title, kind, **kwargs):
    value = {"name": name, "title": title, "kind": kind}
    value.update(kwargs)
    return value


def main():
    os.makedirs(SRC, exist_ok=True)
    enum_xml("ВидыПодключенияИИ", "Виды подключения ИИ", [
        ("YandexGPT", "YandexGPT"),
        ("GigaChat", "GigaChat"),
        ("OpenAIСовместимый", "OpenAI-совместимый"),
    ])
    enum_xml("КаналыОбращений", "Каналы обращений", [
        ("Почта", "Почта"),
        ("Звонок", "Звонок"),
        ("ВебФорма", "Веб-форма"),
    ])
    enum_xml("УровниКлиента", "Уровни клиента", [
        ("Обычный", "Обычный"),
        ("Приоритетный", "Приоритетный"),
        ("VIP", "VIP"),
    ])
    enum_xml("ТональностьОбращения", "Тональность обращения", [
        ("Нейтральный", "Нейтральный"),
        ("Недовольный", "Недовольный"),
        ("Раздраженный", "Раздражённый"),
    ])
    enum_xml("СтатусыОбращения", "Статусы обращения", [
        ("Новое", "Новое"),
        ("Классифицировано", "Классифицировано"),
        ("Назначено", "Назначено"),
        ("ОтветПодготовлен", "Ответ подготовлен"),
        ("ОтветОтправлен", "Ответ отправлен"),
        ("Закрыто", "Закрыто"),
        ("ОшибкаИИ", "Ошибка ИИ"),
    ])
    enum_xml("СтатусыВерификации", "Статусы верификации", [
        ("НеПроверено", "Не проверено"),
        ("Подтверждено", "Подтверждено"),
        ("Исправлено", "Исправлено"),
    ])
    enum_xml("СпособыОтвета", "Способы ответа", [
        ("ЭлектроннаяПочта", "Электронная почта"),
        ("ПубликацияВФорме", "Публикация в форме"),
        ("СообщеноПоЗвонку", "Сообщено по звонку"),
        ("ПочтаИФорма", "Почта и форма"),
    ])
    constants = [
        ("ВидПодключенияИИ", "Вид подключения ИИ", "ref", "cfg:EnumRef.ВидыПодключенияИИ", 10, 0, "Nonnegative", False),
        ("КлючAPI", "Ключ API", "string", None, 500, 0, "Nonnegative", True),
        ("ИдентификаторКаталога", "Идентификатор каталога", "string", None, 80, 0, "Nonnegative", False),
        ("ИмяМодели", "Имя модели", "string", None, 150, 0, "Nonnegative", False),
        ("АдресAPI", "Адрес API", "string", None, 300, 0, "Nonnegative", False),
        ("СхемаАвторизации", "Схема авторизации", "string", None, 40, 0, "Nonnegative", False),
        ("ТаймаутСекунд", "Таймаут, секунд", "number", None, 3, 0, "Nonnegative", False),
        ("МаксимумТокенов", "Максимум токенов ответа", "number", None, 5, 0, "Nonnegative", False),
        ("Температура", "Температура", "number", None, 3, 2, "Any", False),
        ("КоличествоПримеров", "Количество примеров в промпте", "number", None, 2, 0, "Nonnegative", False),
        ("ОбезличиватьПередОтправкой", "Обезличивать перед отправкой", "boolean", None, 1, 0, "Nonnegative", False),
        ("ОбластьДоступаGigaChat", "Область доступа GigaChat", "string", None, 80, 0, "Nonnegative", False),
    ]
    for name, title, kind, ref, length, fraction, sign, password in constants:
        constant_xml(name, title, kind, ref, length, fraction, sign, password)
    for name, title in (
        ("ИнтеграцияLLM", "Интеграция LLM"),
        ("ОбработкаОбращений", "Обработка обращений"),
        ("РаботаСПочтой", "Работа с почтой"),
        ("ДемонстрационныеДанные", "Демонстрационные данные"),
    ):
        common_module(name, title)
    s = "string"
    n = "number"
    catalog_xml("Контрагенты", "Контрагенты", [
        spec("ИНН", "ИНН", s, length=12),
        spec("ЭлектроннаяПочта", "Электронная почта", s, length=150),
        spec("Телефон", "Телефон", s, length=30),
    ])
    catalog_xml("Договоры", "Договоры", [
        spec("Контрагент", "Контрагент", "ref", ref="cfg:CatalogRef.Контрагенты"),
        spec("НомерДоговора", "Номер договора", s, length=50),
        spec("ДатаНачала", "Дата начала", "date", date="Date"),
        spec("ДатаОкончания", "Дата окончания", "date", date="Date"),
        spec("УровеньКлиента", "Уровень клиента", "ref", ref="cfg:EnumRef.УровниКлиента"),
        spec("Действует", "Действует", "boolean"),
    ])
    catalog_xml("ТегиКомпетенций", "Теги компетенций", [])
    catalog_xml("Сотрудники", "Сотрудники", [
        spec("ЭтоИнженер", "Это инженер", "boolean"),
        spec("Доступен", "Доступен", "boolean"),
        spec("ЭлектроннаяПочта", "Электронная почта", s, length=150),
        spec("Телефон", "Телефон", s, length=30),
    ], [("Компетенции", "Компетенции", [
        spec("Тег", "Тег", "ref", ref="cfg:CatalogRef.ТегиКомпетенций"),
        spec("Вес", "Вес", n, length=1),
    ])])
    catalog_xml("КатегорииОбращений", "Категории обращений", [
        spec("ОсновнойТег", "Основной тег", "ref", ref="cfg:CatalogRef.ТегиКомпетенций"),
        spec("ТребуетЧерновик", "Требует черновик", "boolean"),
        spec("Подсказка", "Подсказка классификатору", s, length=300),
    ], [("СмежныеТеги", "Смежные теги", [
        spec("Тег", "Тег", "ref", ref="cfg:CatalogRef.ТегиКомпетенций"),
    ])])
    catalog_xml("Номенклатура", "Номенклатура", [
        spec("Артикул", "Артикул", s, length=40),
        spec("Описание", "Описание", s, length=500, multiline=True),
        spec("Остаток", "Остаток", n, length=10),
        spec("Цена", "Цена", n, length=12, fraction=2),
        spec("КлючевыеСлова", "Ключевые слова", s, length=300),
    ])
    catalog_xml("УчетныеЗаписиПочты", "Учетные записи почты", [
        spec("АдресПочты", "Адрес почты", s, length=150),
        spec("СерверIMAP", "Сервер IMAP", s, length=150),
        spec("ПортIMAP", "Порт IMAP", n, length=5),
        spec("СерверSMTP", "Сервер SMTP", s, length=150),
        spec("ПортSMTP", "Порт SMTP", n, length=5),
        spec("Пользователь", "Пользователь", s, length=150),
        spec("Пароль", "Пароль", s, length=150, password=True, fulltext="DontUse"),
        spec("ИспользоватьSSL", "Использовать SSL", "boolean"),
        spec("Используется", "Используется", "boolean"),
    ])
    document_xml("Обращение", "Обращение", [
        spec("Канал", "Канал", "ref", ref="cfg:EnumRef.КаналыОбращений", fill="ShowError"),
        spec("Контрагент", "Контрагент", "ref", ref="cfg:CatalogRef.Контрагенты"),
        spec("Договор", "Договор", "ref", ref="cfg:CatalogRef.Договоры"),
        spec("УровеньКлиента", "Уровень клиента", "ref", ref="cfg:EnumRef.УровниКлиента"),
        spec("Тема", "Тема", s, length=200),
        spec("Текст", "Текст", s, length=0, multiline=True, fill="ShowError"),
        spec("АдресОтвета", "Адрес ответа", s, length=150),
        spec("ВнешнийИдентификатор", "Внешний идентификатор", s, length=180, index="Index", fulltext="DontUse"),
        spec("Категория", "Категория", "ref", ref="cfg:CatalogRef.КатегорииОбращений"),
        spec("СрочностьТекста", "Срочность текста", n, length=1),
        spec("Тональность", "Тональность", "ref", ref="cfg:EnumRef.ТональностьОбращения"),
        spec("Приоритет", "Приоритет", n, length=1),
        spec("ПояснениеПриоритета", "Пояснение приоритета", s, length=0, multiline=True),
        spec("Исполнитель", "Исполнитель", "ref", ref="cfg:CatalogRef.Сотрудники"),
        spec("ОценкаНазначения", "Оценка назначения", n, length=6, sign="Any"),
        spec("ПояснениеНазначения", "Пояснение назначения", s, length=0, multiline=True),
        spec("КатегорияИИ", "Категория ИИ", "ref", ref="cfg:CatalogRef.КатегорииОбращений"),
        spec("СрочностьИИ", "Срочность ИИ", n, length=1),
        spec("ТональностьИИ", "Тональность ИИ", "ref", ref="cfg:EnumRef.ТональностьОбращения"),
        spec("ПриоритетИИ", "Приоритет ИИ", n, length=1),
        spec("ИсполнительИИ", "Исполнитель ИИ", "ref", ref="cfg:CatalogRef.Сотрудники"),
        spec("ЧерновикОтвета", "Черновик ответа", s, length=0, multiline=True),
        spec("ТекстОтвета", "Текст ответа", s, length=0, multiline=True),
        spec("Статус", "Статус", "ref", ref="cfg:EnumRef.СтатусыОбращения"),
        spec("СтатусВерификации", "Статус верификации", "ref", ref="cfg:EnumRef.СтатусыВерификации"),
        spec("СпособОтвета", "Способ ответа", "ref", ref="cfg:EnumRef.СпособыОтвета"),
        spec("КомментарийОшибки", "Комментарий ошибки", s, length=0, multiline=True),
        spec("ДатаПоступления", "Дата поступления", "date"),
        spec("ДатаКлассификации", "Дата классификации", "date"),
        spec("ДатаНазначения", "Дата назначения", "date"),
        spec("ДатаОтвета", "Дата ответа", "date"),
        spec("ДатаЗакрытия", "Дата закрытия", "date"),
        spec("ХешТекста", "Хеш текста", s, length=64, fulltext="DontUse"),
        spec("Метка", "Метка", s, length=40),
        spec("Комментарий", "Комментарий", s, length=500),
    ])
    register_xml("ЖурналВызововИИ", "Журнал вызовов ИИ", [
        spec("Идентификатор", "Идентификатор", s, length=36),
    ], [
        spec("Успех", "Успех", "boolean"),
        spec("КодСостояния", "Код состояния", n, length=5),
        spec("ДлительностьМс", "Длительность, мс", n, length=10),
    ], [
        spec("Дата", "Дата", "date"),
        spec("Обращение", "Обращение", "ref", ref="cfg:DocumentRef.Обращение"),
        spec("Назначение", "Назначение", s, length=40),
        spec("Модель", "Модель", s, length=150),
        spec("Промпт", "Промпт", s, length=0, multiline=True),
        spec("Ответ", "Ответ", s, length=0, multiline=True),
        spec("ТекстОшибки", "Текст ошибки", s, length=0, multiline=True),
    ])
    register_xml("ИсправленияКлассификации", "Исправления классификации", [
        spec("Идентификатор", "Идентификатор", s, length=36),
    ], [
        spec("ИспользоватьВПромпте", "Использовать в промпте", "boolean"),
    ], [
        spec("Дата", "Дата", "date"),
        spec("Обращение", "Обращение", "ref", ref="cfg:DocumentRef.Обращение"),
        spec("ТекстОбращения", "Текст обращения", s, length=0, multiline=True),
        spec("ОтветИИ", "Ответ ИИ", s, length=0, multiline=True),
        spec("ИсправленныйОтвет", "Исправленный ответ", s, length=0, multiline=True),
    ])
    for name, title in (
        ("НачальнаяСтраница", "Начальная страница"),
        ("РабочееМестоОператора", "Рабочее место оператора"),
        ("ПанельРуководителя", "Панель руководителя"),
        ("НастройкиПодключения", "Настройки подключения"),
    ):
        processor_xml(name, title)
    http_service()
    scheduled_job()
    client_rights = [
        "ThinClient", "WebClient", "MobileClient", "SaveUserData", "Output",
        "MainWindowModeNormal", "MainWindowModeWorkplace", "MainWindowModeEmbeddedWorkplace",
        "MainWindowModeFullscreenWorkplace", "MainWindowModeKiosk", "AnalyticsSystemClient",
    ]
    doc_write = ["Read", "Insert", "Update", "View", "Edit", "InteractiveInsert", "InputByString", "ReadDataHistory"]
    doc_read = ["Read", "View", "InputByString", "ReadDataHistory"]
    cat_read = ["Read", "View", "InputByString"]
    cat_write = cat_read + ["Insert", "Update", "Edit", "InteractiveInsert"]
    reg_write = ["Read", "Update", "View", "Edit"]
    reg_read = ["Read", "View"]
    use = ["Use", "View"]
    operator_objects = [("Configuration.ЦентрОбращений", client_rights)]
    operator_objects += [
        ("Document.Обращение", doc_write),
        ("Catalog.Контрагенты", cat_write),
        ("Catalog.Договоры", cat_read),
        ("Catalog.Сотрудники", cat_read),
        ("Catalog.ТегиКомпетенций", cat_read),
        ("Catalog.КатегорииОбращений", cat_read),
        ("Catalog.Номенклатура", cat_read),
        ("Catalog.УчетныеЗаписиПочты", cat_read),
        ("InformationRegister.ЖурналВызововИИ", reg_write),
        ("InformationRegister.ИсправленияКлассификации", reg_write),
        ("DataProcessor.НачальнаяСтраница", use),
        ("DataProcessor.РабочееМестоОператора", use),
        ("HTTPService.ПриемОбращений", ["Use"]),
    ]
    manager_objects = [("Configuration.ЦентрОбращений", client_rights)]
    manager_objects += [
        ("Document.Обращение", doc_read),
        ("Catalog.Контрагенты", cat_read),
        ("Catalog.Договоры", cat_read),
        ("Catalog.Сотрудники", cat_read),
        ("Catalog.ТегиКомпетенций", cat_read),
        ("Catalog.КатегорииОбращений", cat_read),
        ("Catalog.Номенклатура", cat_read),
        ("Catalog.УчетныеЗаписиПочты", cat_read),
        ("InformationRegister.ЖурналВызововИИ", reg_read),
        ("InformationRegister.ИсправленияКлассификации", reg_read + ["Update", "Edit"]),
        ("DataProcessor.НачальнаяСтраница", use),
        ("DataProcessor.ПанельРуководителя", use),
        ("DataProcessor.РабочееМестоОператора", use),
        ("HTTPService.ПриемОбращений", ["Use"]),
    ]
    admin_rights = [
        "Administration", "DataAdministration", "UpdateDataBaseConfiguration",
        "ThickClient", "ExternalConnection", "Automation", "TechnicalSpecialistMode",
        "ThinClient", "WebClient", "MobileClient", "MainWindowModeNormal",
        "MainWindowModeWorkplace", "MainWindowModeEmbeddedWorkplace",
        "MainWindowModeFullscreenWorkplace", "MainWindowModeKiosk",
        "AnalyticsSystemClient", "SaveUserData", "Output",
        "InteractiveOpenExtDataProcessors", "InteractiveOpenExtReports",
    ]
    role_file("ПолныеПрава", "Полные права", rights_document([("Configuration.ЦентрОбращений", admin_rights)], True))
    role_file("ОператорПоддержки", "Оператор поддержки", rights_document(operator_objects, False))
    role_file("Руководитель", "Руководитель", rights_document(manager_objects, False))
    content = [
        "DataProcessor.НачальнаяСтраница",
        "DataProcessor.РабочееМестоОператора",
        "DataProcessor.ПанельРуководителя",
        "DataProcessor.НастройкиПодключения",
        "Document.Обращение",
        "Catalog.Контрагенты",
        "Catalog.Договоры",
        "Catalog.Сотрудники",
        "Catalog.ТегиКомпетенций",
        "Catalog.КатегорииОбращений",
        "Catalog.Номенклатура",
        "Catalog.УчетныеЗаписиПочты",
        "InformationRegister.ЖурналВызововИИ",
        "InformationRegister.ИсправленияКлассификации",
        "Constant.ВидПодключенияИИ",
        "Constant.КлючAPI",
        "Constant.ИдентификаторКаталога",
        "Constant.ИмяМодели",
        "Constant.АдресAPI",
        "Constant.СхемаАвторизации",
        "Constant.ТаймаутСекунд",
        "Constant.МаксимумТокенов",
        "Constant.Температура",
        "Constant.КоличествоПримеров",
        "Constant.ОбезличиватьПередОтправкой",
        "Constant.ОбластьДоступаGigaChat",
    ]
    subsystem_xml(content)
    children = [("Language", "Русский"), ("Subsystem", "ЦентрОбращений")]
    for name in ("ПолныеПрава", "ОператорПоддержки", "Руководитель"):
        children.append(("Role", name))
    for name in ("ИнтеграцияLLM", "ОбработкаОбращений", "РаботаСПочтой", "ДемонстрационныеДанные"):
        children.append(("CommonModule", name))
    children.append(("HTTPService", "ПриемОбращений"))
    children.append(("ScheduledJob", "ПолучениеПочты"))
    for item in constants:
        children.append(("Constant", item[0]))
    for name in ("Контрагенты", "Договоры", "ТегиКомпетенций", "Сотрудники", "КатегорииОбращений", "Номенклатура", "УчетныеЗаписиПочты"):
        children.append(("Catalog", name))
    children.append(("Document", "Обращение"))
    for name in ("ВидыПодключенияИИ", "КаналыОбращений", "УровниКлиента", "ТональностьОбращения", "СтатусыОбращения", "СтатусыВерификации", "СпособыОтвета"):
        children.append(("Enum", name))
    for name in ("НачальнаяСтраница", "РабочееМестоОператора", "ПанельРуководителя", "НастройкиПодключения"):
        children.append(("DataProcessor", name))
    children.append(("InformationRegister", "ЖурналВызововИИ"))
    children.append(("InformationRegister", "ИсправленияКлассификации"))
    patch_configuration(children)
    interface_files()
    write_forms()
    print("generated", SRC)


if __name__ == "__main__":
    main()
