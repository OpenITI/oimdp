# mARkdown tag library

META = "#META#"
METAEND = "#META#Header#End#"
PAGE = "PageV"
HEMI = "%~%"
LINE = "~~"
MILESTONE = "Milestone300"
HEADER1 = "### |"
HEADER2 = "### ||"
HEADER3 = "### |||"
HEADER4 = "### ||||"
HEADER5 = "### |||||"
EDITORIAL = "### |EDITOR|"
DIC = "### $DIC_"
DIC_NIS = "### $DIC_NIS$"
DIC_TOP = "### $DIC_TOP$"
DIC_LEX = "### $DIC_LEX$"
DIC_BIB = "### $DIC_BIB$"
BIO_MAN = "### $"
BIO_MAN_FULL = "### $BIO_MAN$"
BIO_WOM = "### $$"
BIO_WOM_FULL = "### $BIO_WOM$"
BIO_REF = "### $$$"
BIO_REF_FULL = "### $BIO_REF$"
LIST_NAMES = "### $$$$"
LIST_NAMES_FULL = "### $BIO_NLI$"
EVENT = "### @"
EVENT_FULL = "### $CHR_EVE$"
LIST_EVENTS = "### @ RAW"
LIST_EVENTS_FULL = "### $CHR_RAW$"
DOX = "### $DOX_"
DOX_POS = "### $DOX_POS$"
DOX_SEC = "### $DOX_SEC$"
NE = "@"
YEAR_BIRTH = "YB"
YEAR_DEATH = "YD"
YEAR_OTHER = "YY"
YEAR_AGE = "YA"
TOP = "T"
TOP_FULL = "TOP"
PER = "P"
PER_FULL = "PER"
SRC = "SRC"
PROV = "#$#PROV"
GEO_TYPE = "#$#TYPE"
REG = "#$#REG"
STTL = "#$#STTL"
DIST_FROM = "#$#FROM"
DIST_TO = "#$#TOWA"
DIST = "#$#DIST"
RWY = "# $RWY$"
MATN = "@MATN@"
HUKM = "@HUKM@"

# GROUPS
# NB these are listed to allow safe replacement, e.g. "### ||" before "### |"
HEADERS = [HEADER5, HEADER4, HEADER3, HEADER2, HEADER1]
DICTIONARIES = [DIC_NIS, DIC_TOP, DIC_LEX, DIC_BIB]
BIOS_EVENTS = [LIST_NAMES, BIO_WOM, BIO_MAN, BIO_REF, LIST_EVENTS, EVENT,
               BIO_MAN_FULL, BIO_WOM_FULL, BIO_REF_FULL, LIST_NAMES_FULL,
               EVENT_FULL, LIST_EVENTS_FULL]
DOXOGRAPHICAL = [DOX_POS, DOX_SEC]
NAMED_ENTITIES = [YEAR_BIRTH, YEAR_DEATH, YEAR_OTHER, YEAR_AGE, TOP, TOP_FULL,
                  PER, PER_FULL, SRC]
PHRASE_LV_TAGS = [HEMI, MILESTONE, *NAMED_ENTITIES]
