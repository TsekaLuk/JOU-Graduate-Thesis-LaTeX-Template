\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{jougraduate}[2026/03/10 Jiangsu Ocean University Graduate Thesis Template]

\newif\ifjousupercite
\jousupercitefalse
\def\jouNatbibOptions{numbers,sort&compress}

\DeclareOption{supercite}{%
    \jousupercitetrue
    \def\jouNatbibOptions{super,numbers,sort&compress}%
}
\DeclareOption{inlinecite}{%
    \jousupercitefalse
    \def\jouNatbibOptions{numbers,sort&compress}%
}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexbook}}
\ProcessOptions\relax

\LoadClass[a4paper,zihao=-4,openany,oneside,fontset=none]{ctexbook}

\RequirePackage{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{titletoc}
\RequirePackage{graphicx}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{mathtools}
\RequirePackage[\jouNatbibOptions]{natbib}
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{longtable}
\RequirePackage{listings}
\RequirePackage{xcolor}
\RequirePackage{setspace}
\RequirePackage{indentfirst}
\RequirePackage{lastpage}
\RequirePackage{enumitem}
\RequirePackage{caption}
\RequirePackage[preferwps]{styles/joufonts}
\RequirePackage{styles/jougraduateheadings}
\RequirePackage{hyperref}
\RequirePackage{bookmark}
\RequirePackage[capitalize,nameinlink,noabbrev]{cleveref}

\geometry{
    a4paper,
    top=2.54cm,
    bottom=2.54cm,
    left=3.18cm,
    right=3.18cm,
    headheight=0.8cm,
    headsep=0.5cm,
    footskip=1cm
}
\linespread{1.25}

\DeclareCaptionFont{jouthesiscaption}{\zihao{5}\songti}
\captionsetup{
    font=jouthesiscaption,
    labelsep=quad,
    skip=6pt
}
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}

\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.25}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}

\lstdefinestyle{joucode}{
    basicstyle=\small\ttfamily,
    keywordstyle=\color{blue!60!black}\bfseries,
    commentstyle=\color{green!40!black},
    stringstyle=\color{red!60!black},
    numbers=left,
    numberstyle=\tiny\color{gray},
    stepnumber=1,
    numbersep=8pt,
    frame=single,
    rulecolor=\color{black!30},
    breaklines=true,
    showstringspaces=false,
    columns=fullflexible,
    keepspaces=true,
    tabsize=4,
    captionpos=t
}
\lstset{style=joucode}

\setlist{
    nosep,
    topsep=0pt,
    partopsep=0pt,
    itemsep=0pt,
    parsep=0pt
}

\newcommand{\jou@frontmatterstyle}{%
    \fancyhf{}%
    \fancyfoot[C]{\zihao{5}\thepage}%
    \renewcommand{\headrulewidth}{0pt}%
    \renewcommand{\footrulewidth}{0pt}%
}
\newcommand{\jou@bodystyle}{%
    \fancyhf{}%
    \fancyhead[C]{\JOUMakeGraduateHeader{\textwidth}{\JOUHeadingBodyHeaderRight{\thepage}}}%
    \renewcommand{\headrulewidth}{0.4pt}%
    \renewcommand{\footrulewidth}{0pt}%
}

\fancypagestyle{frontmatterstyle}{\jou@frontmatterstyle}
\fancypagestyle{thesisbody}{\jou@bodystyle}
\fancypagestyle{plain}{\jou@frontmatterstyle}
\pagestyle{frontmatterstyle}

\newcommand{\usebodypagestyle}{%
    \pagestyle{thesisbody}%
    \fancypagestyle{plain}{\jou@bodystyle}%
}
\let\jou@origmainmatter\mainmatter
\renewcommand{\mainmatter}{%
    \jou@origmainmatter
    \usebodypagestyle
}

\JOUApplyBodySectioning
\JOUApplyBodyTextLayout
\JOUApplyBodyTocLayout
\JOUApplyBodyReferenceNames

\hypersetup{
    colorlinks=true,
    linkcolor=black,
    citecolor=black,
    urlcolor=blue,
    bookmarksnumbered=true,
    pdfstartview=FitH
}
\bookmarksetup{numbered=true,open=true}

\renewcommand{\bibsection}{\JOUBackmatterHeadingOnly{\bibname}}
\newcommand{\JOUPrintBibliography}[1][references/refs]{%
    \addcontentsline{toc}{chapter}{参考文献}%
    \renewcommand{\bibname}{参考文献}%
    \bibliographystyle{gbt7714-numerical}%
    \bibliography{#1}%
}

\def\JOUChineseTitle{论文题目}
\def\JOUEnglishTitle{English Title}
\def\JOUAuthorName{作者姓名}
\def\JOUStudentId{学号}
\def\JOUCollege{学院名称}
\def\JOUProgram{学科专业}
\def\JOUResearchDirection{研究方向}
\def\JOUDegree{工学硕士}
\def\JOUSupervisorName{导师姓名}
\def\JOUSupervisorTitle{导师职称}
\def\JOUClassificationNumber{}
\def\JOUUDC{}
\def\JOUConfidentiality{公开}
\def\JOUUniversityCode{11641}
\def\JOUDefenseChair{待定}
\def\JOUReviewers{待定}
\def\JOUDate{二〇二六年六月}
\def\JOUProgramDuration{3年}
\def\JOUGrantInfo{无}
\def\JOUSubmissionDate{2026年6月}

\newcommand{\cnthesistitle}[1]{\gdef\JOUChineseTitle{#1}}
\newcommand{\entitle}[1]{\gdef\JOUEnglishTitle{#1}}
\newcommand{\graduateauthor}[1]{\gdef\JOUAuthorName{#1}}
\newcommand{\studentid}[1]{\gdef\JOUStudentId{#1}}
\newcommand{\college}[1]{\gdef\JOUCollege{#1}}
\newcommand{\program}[1]{\gdef\JOUProgram{#1}}
\newcommand{\researchdirection}[1]{\gdef\JOUResearchDirection{#1}}
\newcommand{\degree}[1]{\gdef\JOUDegree{#1}}
\newcommand{\supervisor}[1]{\gdef\JOUSupervisorName{#1}}
\newcommand{\supervisortitle}[1]{\gdef\JOUSupervisorTitle{#1}}
\newcommand{\classificationnumber}[1]{\gdef\JOUClassificationNumber{#1}}
\newcommand{\udc}[1]{\gdef\JOUUDC{#1}}
\newcommand{\confidentiality}[1]{\gdef\JOUConfidentiality{#1}}
\newcommand{\universitycode}[1]{\gdef\JOUUniversityCode{#1}}
\newcommand{\defensechair}[1]{\gdef\JOUDefenseChair{#1}}
\newcommand{\reviewers}[1]{\gdef\JOUReviewers{#1}}
\newcommand{\coverdate}[1]{\gdef\JOUDate{#1}}
\newcommand{\programduration}[1]{\gdef\JOUProgramDuration{#1}}
\newcommand{\grantinfo}[1]{\gdef\JOUGrantInfo{#1}}
\newcommand{\submissiondate}[1]{\gdef\JOUSubmissionDate{#1}}

\newcommand{\JOUApplySharedMetadata}{%
    \cnthesistitle{\JOUSharedTitleCN}%
    \entitle{\JOUSharedTitleEN}%
    \graduateauthor{\JOUSharedAuthorName}%
    \studentid{\JOUSharedStudentId}%
    \college{\JOUSharedCollege}%
    \program{\JOUSharedProgram}%
    \researchdirection{\JOUSharedResearchDirection}%
    \degree{\JOUSharedDegree}%
    \supervisor{\JOUSharedSupervisorName}%
    \supervisortitle{\JOUSharedSupervisorTitle}%
    \classificationnumber{\JOUSharedClassificationNumber}%
    \udc{\JOUSharedUDC}%
    \confidentiality{\JOUSharedConfidentiality}%
    \universitycode{\JOUSharedUniversityCode}%
    \defensechair{\JOUSharedDefenseChair}%
    \reviewers{\JOUSharedReviewers}%
    \coverdate{\JOUSharedDate}%
    \programduration{\JOUSharedProgramDuration}%
    \grantinfo{\JOUSharedGrantInfo}%
    \submissiondate{\JOUSharedSubmissionDate}%
}

\newcommand{\JOUFrontmatterTitle}[1]{%
    {\centering\JOUHeadingHei\bfseries\zihao{-2}#1\par}%
    \vspace{0.6\baselineskip}%
}
\newcommand{\JOUFrontmatterEnglishTitle}[1]{%
    {\centering\rmfamily\bfseries\fontsize{18pt}{22pt}\selectfont #1\par}%
    \vspace{0.6\baselineskip}%
}
\newcommand{\JOUChapterEnglishLine}[1]{%
    {\centering\rmfamily\bfseries\zihao{-2}#1\par}%
    \vspace{0.4\baselineskip}%
}
\newcommand{\JOUSectionEnglishLine}[1]{%
    {\rmfamily\bfseries\zihao{-3}#1\par}%
    \vspace{0.3\baselineskip}%
}
\newcommand{\JOUCNKeywords}[1]{%
    \par\vspace{0.9\baselineskip}%
    \noindent{\JOUHeadingHei\bfseries\zihao{-4}关键词：}{\zihao{-4}\songti #1}%
}
\newcommand{\JOUENKeywords}[1]{%
    \par\vspace{0.9\baselineskip}%
    \noindent{\rmfamily\bfseries\zihao{-4}Keywords: }{\rmfamily\zihao{-4}#1}%
}
\newcommand{\JOUUnderlineBox}[2]{%
    \makebox[0pt][l]{\raisebox{-0.52ex}{\rule{#1}{0.35pt}}}%
    \makebox[#1][l]{#2\hfill}%
}

\newcommand{\figref}[1]{\cref{#1}}
\newcommand{\tabref}[1]{\cref{#1}}
\newcommand{\eqnref}[1]{\cref{#1}}
\newcommand{\coderef}[1]{\cref{#1}}
\ifjousupercite
    \newcommand{\upcite}[1]{\cite{#1}}
\else
    \newcommand{\upcite}[1]{\textsuperscript{\cite{#1}}}
\fi

\endinput
