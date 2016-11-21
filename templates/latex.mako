<%!
	def esc(text):
		out = text
		out = out.replace("&", "\&")
		out = out.replace("#", "\#")
		out = out.replace("%", "\%")

		out = out.replace("<*", "\emph{")
		out = out.replace("*>", "}")

		return out
%>
<%page expression_filter="esc"/>
\documentclass[11pt,${config["paper"]}paper]{moderncv}

%% moderncv themes
\moderncvtheme[${config["color"]}]{classic} % optional argument are 'blue' (default), 'orange', 'green', 'red', 'purple', 'grey' and 'roman' (for roman fonts, instead of sans serif fonts)

\usepackage[utf8]{inputenc}
\usepackage{color}

\usepackage[scale=0.8]{geometry}

\renewcommand{\labelitemi}{--}

\firstname{${first_name}}
\familyname{${family_name}}
%%\title{}
\mobile{${personal_info["mobile"]}}
%%\phone{}
%%\fax{}
\email{${personal_info["email"]}}
\homepage{${personal_info["webs"][0]["url"]}}
\extrainfo{${personal_info["birth"]}}
\photo[104pt][0.0pt]{${personal_info["photo"]}} % '64pt' is the height the picture must be resized to, 0.4pt is the thickness of the frame around it (put it to 0pt for no frame) and 'picture' is the name of the picture file; optional, remove the line if not wanted
\quote{``${quote["line"]}'' -- ${quote["author"]}}

\begin{document}
\maketitle

\section{Summary}
\cvline{}{${summary}}

\section{Education}
% for edu in education:
\cventry{${edu["range"]}}{${edu["title"]}}{${edu["organization"]}}{}{}{${edu["comments"] if "comments" in edu and edu["comments"] else ""}}
% endfor

\section{Experience}
% for exp in experience:
\cventry{${exp["range"]}}{${exp["company"]}}{${exp["position"]}}{}{}{
% if isinstance(exp["comments"], basestring):
${exp["comments"]}
% else:
	\begin{itemize}
% for comment in exp["comments"]:
		\item ${comment}
% endfor
	\end{itemize}
% endif
}
% endfor
% for thes in thesis:

\section{${thes["name"]}}
\cvline{Title}{\emph{``${thes["title"]}''}}
\cvline{Supervisors}{${thes["supervisors"]}}
\cvline{Description}{\small ${thes["description"]}}
% endfor

\section{Personal projects}
% for proj in personal_projects:
\cventry{${proj["range"]}}{${proj["name"]}}{\href{${proj["url"]}}{${proj["url"]}}}{}{}{${proj["description"]}}
% endfor

\section{Free Software Projects}
% for proj in free_software:
\cventry{${proj["range"]}}{${proj["name"]}}{\href{${proj["url"]}}{${proj["url"]}}}{}{}{${proj["description"]}}
% endfor

\section{Languages}
% for lang in languages:
\cvlanguage{${lang["lang"]}}{${lang["level"]}}{}
% endfor

\section{Qualities}

\subsection{Computer skills}
% for skills in computer_skills:
\cvline{${skills.keys()[0]}:}{\small ${skills.values()[0]}}
% endfor

\subsection{Personal skills}
% for skills in personal_skills:
\cvline{${skills.keys()[0]}}{
	\begin{itemize}
% for desc in skills.values()[0]:
		\item ${desc}
% endfor
	\end{itemize}
}
% endfor

\subsection{Interests}
\cvline{}{${interests}}

\end{document}
