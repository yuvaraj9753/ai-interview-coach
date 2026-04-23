from dotenv import load_dotenv
import os
from groq import Groq
from prompts import QUESTION_PROMPT, EVALUATION_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------- QUESTION ----------
def generate_question(resume, jd, domain, history, mode):

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": QUESTION_PROMPT.format(
                resume=resume[:1500],
                jd=jd[:1000],
                domain=domain,
                mode=mode,
                history=history[-5:]
            )
        }],
        temperature=0.6,
        max_tokens=120
    )

    return res.choices[0].message.content.strip()


# ---------- EVALUATION ----------
def evaluate_answer(question, answer, mode):

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": EVALUATION_PROMPT.format(
                question=question,
                answer=answer,
                mode=mode
            )
        }],
        temperature=0.2,
        max_tokens=200
    )

    return res.choices[0].message.content.strip()