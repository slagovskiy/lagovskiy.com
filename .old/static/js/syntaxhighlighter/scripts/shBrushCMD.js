/**
 * SyntaxHighlighter
 * http://alexgorbatchev.com/SyntaxHighlighter
 *
 * SyntaxHighlighter is donationware. If you are using it, please donate.
 * http://alexgorbatchev.com/SyntaxHighlighter/donate.html
 *
 * @version
 * 3.0.83 (July 02 2010)
 * 
 * @copyright
 * Copyright (C) 2004-2010 Alex Gorbatchev.
 *
 * @license
 * Dual licensed under the MIT and GPL licenses.
 */
;(function()
{
	// CommonJS
	typeof(require) != 'undefined' ? SyntaxHighlighter = require('shCore').SyntaxHighlighter : null;

	function Brush()
	{
		var keywords =	'DO ELSE ERRORLEVEL EXIST IN NOT OFF ON LOADHIGH SET EXIT EOF';
        keywords = keywords + ' ' + keywords.toLocaleLowerCase();
		var commands =  'ASSOC AT ATTRIB BREAK CACLS CALL CD CHCP CHDIR CHKDSK CHKNTFS CLS CMD COLOR COMP' +
                'COMPACT CONVERT COPY DATE DEL DIR DISKCOMP DISKCOPY DOSKEY ECHO ENDLOCAL ERASE FC FIND FINDSTR' +
                'FOR FORMAT FTYPE GOTO GRAFTABL HELP IF LABEL MD MKDIR MODE MORE MOVE PATH PAUSE POPD PRINT PROMPT' +
                'PUSHD RD RECOVER REN RENAME REPLACE RMDIR SETLOCAL SHIFT SORT START SUBST TIME TITLE TREE' +
                'TYPE VER VERIFY VOL XCOPY PROMPT';
        commands = commands + ' ' + commands.toLocaleLowerCase();

		this.regexList = [
			{ regex: /^#=!.*$/gm,											css: 'preprocessor bold' },
            { regex: /REM.*$/gm,										    css: 'comments' },      // one line comments
            { regex: SyntaxHighlighter.regexLib.doubleQuotedString,			css: 'string' },		// double quoted strings
			{ regex: SyntaxHighlighter.regexLib.singleQuotedString,			css: 'string' },		// single quoted strings
			{ regex: new RegExp(this.getKeywords(keywords), 'gm'),			css: 'keyword' },		// keywords
            { regex: new RegExp('(\\$|%)\\w+', 'g'),				        css: 'variable' },
            { regex: /=(.*)$/gm,											css: 'variable' },
			{ regex: new RegExp(this.getKeywords(commands), 'gm'),			css: 'functions' }		// commands
			];
	}

	Brush.prototype	= new SyntaxHighlighter.Highlighter();
	Brush.aliases	= ['cmd'];

	SyntaxHighlighter.brushes.Bash = Brush;

	// CommonJS
	typeof(exports) != 'undefined' ? exports.Brush = Brush : null;
})();
