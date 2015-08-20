<%!
	import datetime

	def esc(text):
		out = text
		out = out.replace("<*", "*")
		out = out.replace("*>", "*")

		return out
%><%page expression_filter="esc"/>---
title: "Curriculum Vitae"
description: "Curriculum Vitae"
date: "${datetime.date.today().isoformat()}"
slug: "cv"
---

[Download .PDF ⬇](${config["download_pdf"]})

> *“${quote["line"]}”* – ${quote["author"]}

* **Phone:** ${personal_info["mobile"]}
* **Email:** [${personal_info["email"]}](${personal_info["email"]})
% for web in personal_info["webs"]:
* **${web["name"]}:** [${web["url"]}](${web["url"]})
% endfor
* **Date of birth:** ${personal_info["birth"]}

Summary
=======

${summary}

Education
=========

% for edu in education:
* ${edu["range"]} **${edu["title"]}**, ${edu["organization"]}.
% if "comments" in edu and edu["comments"]:

	> ${edu["comments"]}
% endif
% endfor

Experience
==========

% for exp in experience:
* ${exp["range"]} **${exp["company"]}**, *${exp["position"]}*.

% if isinstance(exp["comments"], basestring):
	> ${exp["comments"]}
% else:
% for comment in exp["comments"]:
	+ ${comment}
% endfor
% endif
% endfor
% for thes in thesis:

${thes["name"]}
===============

**Title:**
	*“${thes["title"]}”*

**Supervisors:**
	${thes["supervisors"]}

**Description:**
	${thes["description"]}
% endfor

Free Software Projects
======================

% for proj in free_software:
* ${proj["range"]} **${proj["name"]}**, <${proj["url"]}>.

	> ${proj["description"]}
% endfor

Languages
=========

% for lang in languages:
* **${lang["lang"]}** ${lang["level"]}
% endfor

Qualities
=========

Computer skills
---------------
% for skills in computer_skills:

**${skills.keys()[0]}:**
	${skills.values()[0]}
% endfor

Personal skills
---------------
% for skills in personal_skills:

${"### " + skills.keys()[0]}:

% for desc in skills.values()[0]:
* ${desc}
% endfor
% endfor

Interests
=========

${interests}
