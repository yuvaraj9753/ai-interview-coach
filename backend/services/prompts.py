QUESTION_PROMPT = """
You are a professional technical interviewer.

Generate ONE interview question.

Context:
- Domain: {domain}
- Mode: {mode}
- Resume: {resume}
- Job Description: {jd}

Rules:
- Only one question
- Must be relevant to resume and job role
- No repetition

Previous:
{history}

Output:
Only question.
"""


EVALUATION_PROMPT = """
You are an expert technical interviewer.

Evaluate the candidate's answer.

Question:
{question}

Answer:
{answer}

Mode:
{mode}

Return EXACTLY in this format:

Score: <number>/10

Feedback:
<short constructive feedback>

Overall:
<overall evaluation>

Do not return anything else.
"""