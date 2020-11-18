import re, os
from os.path import abspath, join
import sys


class Parser():
    dct = {}

    def __init__(self):
        self.__fill_dct()

    def parse_file(self, pth):
        """
        Full parse with cyrillic characters
        :parameter text str without encode
        :return str
        """
        text = self.read_file(pth)
        text = self.rtf_to_txt(text)
        return self.cyrillic_translate(text)

    def __get_path(self):
        """
        Return current dir path
        :return:
        """
        from os.path import realpath, split

        cur_path = realpath(__file__)
        return split(cur_path)[0]

    def parse_all(self):
        """
        Parse all files in dir
        :parameter text str without encode
        :return str
        """

        cur_path = self.__get_path()
        files = os.listdir(abspath(cur_path))
        for f in files:
            if f.endswith(".rtf"):
                pth = join(abspath(cur_path), f)
                res = self.parse_file(pth)
                name = f.replace(".rtf", ".txt")
                self.__save_result(res, name)

    def __save_result(self, txt, name):
        cur_dir = self.__get_path()

        target_dir = abspath(join(cur_dir, "txt_output"))
        pth = abspath(join(target_dir, name))

        os.makedirs(target_dir, exist_ok=True)

        with open(pth, "w", encoding="utf-8") as f:
            f.write(txt)

    def rtf_to_txt(self, text):
        """
        Extract text in RTF Files. Refactored to use with Python 3.x
        Code created by Markus Jarderot
        :parameter text str without encode
        :return str
        """
        text = text.encode("utf-8")

        pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
        destinations = frozenset((
            'aftncn', 'aftnsep', 'aftnsepc', 'annotation', 'atnauthor', 'atndate', 'atnicn', 'atnid',
            'atnparent', 'atnref', 'atntime', 'atrfend', 'atrfstart', 'author', 'background',
            'bkmkend', 'bkmkstart', 'blipuid', 'buptim', 'category', 'colorschememapping',
            'colortbl', 'comment', 'company', 'creatim', 'datafield', 'datastore', 'defchp', 'defpap',
            'do', 'doccomm', 'docvar', 'dptxbxtext', 'ebcend', 'ebcstart', 'factoidname', 'falt',
            'fchars', 'ffdeftext', 'ffentrymcr', 'ffexitmcr', 'ffformat', 'ffhelptext', 'ffl',
            'ffname', 'ffstattext', 'field', 'file', 'filetbl', 'fldinst', 'fldrslt', 'fldtype',
            'fname', 'fontemb', 'fontfile', 'fonttbl', 'footer', 'footerf', 'footerl', 'footerr',
            'footnote', 'formfield', 'ftncn', 'ftnsep', 'ftnsepc', 'g', 'generator', 'gridtbl',
            'header', 'headerf', 'headerl', 'headerr', 'hl', 'hlfr', 'hlinkbase', 'hlloc', 'hlsrc',
            'hsv', 'htmltag', 'info', 'keycode', 'keywords', 'latentstyles', 'lchars', 'levelnumbers',
            'leveltext', 'lfolevel', 'linkval', 'list', 'listlevel', 'listname', 'listoverride',
            'listoverridetable', 'listpicture', 'liststylename', 'listtable', 'listtext',
            'lsdlockedexcept', 'macc', 'maccPr', 'mailmerge', 'maln', 'malnScr', 'manager', 'margPr',
            'mbar', 'mbarPr', 'mbaseJc', 'mbegChr', 'mborderBox', 'mborderBoxPr', 'mbox', 'mboxPr',
            'mchr', 'mcount', 'mctrlPr', 'md', 'mdeg', 'mdegHide', 'mden', 'mdiff', 'mdPr', 'me',
            'mendChr', 'meqArr', 'meqArrPr', 'mf', 'mfName', 'mfPr', 'mfunc', 'mfuncPr', 'mgroupChr',
            'mgroupChrPr', 'mgrow', 'mhideBot', 'mhideLeft', 'mhideRight', 'mhideTop', 'mhtmltag',
            'mlim', 'mlimloc', 'mlimlow', 'mlimlowPr', 'mlimupp', 'mlimuppPr', 'mm', 'mmaddfieldname',
            'mmath', 'mmathPict', 'mmathPr', 'mmaxdist', 'mmc', 'mmcJc', 'mmconnectstr',
            'mmconnectstrdata', 'mmcPr', 'mmcs', 'mmdatasource', 'mmheadersource', 'mmmailsubject',
            'mmodso', 'mmodsofilter', 'mmodsofldmpdata', 'mmodsomappedname', 'mmodsoname',
            'mmodsorecipdata', 'mmodsosort', 'mmodsosrc', 'mmodsotable', 'mmodsoudl',
            'mmodsoudldata', 'mmodsouniquetag', 'mmPr', 'mmquery', 'mmr', 'mnary', 'mnaryPr',
            'mnoBreak', 'mnum', 'mobjDist', 'moMath', 'moMathPara', 'moMathParaPr', 'mopEmu',
            'mphant', 'mphantPr', 'mplcHide', 'mpos', 'mr', 'mrad', 'mradPr', 'mrPr', 'msepChr',
            'mshow', 'mshp', 'msPre', 'msPrePr', 'msSub', 'msSubPr', 'msSubSup', 'msSubSupPr', 'msSup',
            'msSupPr', 'mstrikeBLTR', 'mstrikeH', 'mstrikeTLBR', 'mstrikeV', 'msub', 'msubHide',
            'msup', 'msupHide', 'mtransp', 'mtype', 'mvertJc', 'mvfmf', 'mvfml', 'mvtof', 'mvtol',
            'mzeroAsc', 'mzeroDesc', 'mzeroWid', 'nesttableprops', 'nextfile', 'nonesttables',
            'objalias', 'objclass', 'objdata', 'object', 'objname', 'objsect', 'objtime', 'oldcprops',
            'oldpprops', 'oldsprops', 'oldtprops', 'oleclsid', 'operator', 'panose', 'password',
            'passwordhash', 'pgp', 'pgptbl', 'picprop', 'pict', 'pn', 'pnseclvl', 'pntext', 'pntxta',
            'pntxtb', 'printim', 'private', 'propname', 'protend', 'protstart', 'protusertbl', 'pxe',
            'result', 'revtbl', 'revtim', 'rsidtbl', 'rxe', 'shp', 'shpgrp', 'shpinst',
            'shppict', 'shprslt', 'shptxt', 'sn', 'sp', 'staticval', 'stylesheet', 'subject', 'sv',
            'svb', 'tc', 'template', 'themedata', 'title', 'txe', 'ud', 'upr', 'userprops',
            'wgrffmtfilter', 'windowcaption', 'writereservation', 'writereservhash', 'xe', 'xform',
            'xmlattrname', 'xmlattrvalue', 'xmlclose', 'xmlname', 'xmlnstbl',
            'xmlopen',
        ))

        specialchars = {
            'par': '\n',
            'sect': '\n\n',
            'page': '\n\n',
            'line': '\n',
            'tab': '\t',
            'emdash': '\u2014',
            'endash': '\u2013',
            'emspace': '\u2003',
            'enspace': '\u2002',
            'qmspace': '\u2005',
            'bullet': '\u2022',
            'lquote': '\u2018',
            'rquote': '\u2019',
            'ldblquote': '\201C',
            'rdblquote': '\u201D',
        }
        stack = []
        ignorable = False
        ucskip = 1
        curskip = 0
        out = []
        for match in pattern.finditer(text.decode()):
            word, arg, hex, char, brace, tchar = match.groups()
            if brace:
                curskip = 0
                if brace == '{':
                    stack.append((ucskip, ignorable))
                elif brace == '}':
                    ucskip, ignorable = stack.pop()
            elif char:
                curskip = 0
                if char == '~':
                    if not ignorable:
                        out.append('\xA0')
                elif char in '{}\\':
                    if not ignorable:
                        out.append(char)
                elif char == '*':
                    ignorable = True
            elif word:
                curskip = 0
                if word in destinations:
                    ignorable = True
                elif ignorable:
                    pass
                elif word in specialchars:
                    out.append(specialchars[word])
                elif word == 'uc':
                    ucskip = int(arg)
                elif word == 'u':
                    c = int(arg)
                    if c < 0: c += 0x10000
                    if c > 127:
                        out.append(chr(c))
                    else:
                        out.append(chr(c))
                    curskip = ucskip
            elif hex:
                if curskip > 0:
                    curskip -= 1
                elif not ignorable:
                    c = int(hex, 16)
                    if c > 127:
                        out.append(chr(c))
                    else:
                        out.append(chr(c))
            elif tchar:
                if curskip > 0:
                    curskip -= 1
                elif not ignorable:
                    out.append(tchar)
        return ''.join(out)

    def cyrillic_translate(self, text):
        """
           Hardcode cyrillic replace
           :return str
        """
        for k in self.dct:
            text = text.replace(k, self.dct[k])
        return text

    def __fill_dct(self):
        code = "àáâãäå¸æçèéêëìíîïðñòóôõö÷øùúüýûþÿÀÁÂÃÄÅ¨ÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÜÝÛÞß"
        alpha = "абвгдеёжзийклмнопрстуфхцчшщъьэыюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЭЫЮЯ"
        for unexpected, chr in zip(code, alpha):
            self.dct[unexpected] = chr

    def read_file(self, pth):
        with open(pth, "r") as f:
            rtf = f.read()
        return rtf


if len(sys.argv) == 2:
    p = Parser()
    arg = sys.argv[1]
    if str(arg).lower().strip() == "all":
        p.parse_all()
    if arg.lower().strip().endswith(".rtf"):
        txt = p.parse_file(arg)
        tf = arg.replace(".rtf", "_from_rft.txt")
        with open(tf, "w", encoding="utf-8") as f:
            f.write(txt)
