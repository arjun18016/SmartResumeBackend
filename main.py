from fastapi import FastAPI, UploadFile, File
import pdfplumber

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Smart Resume Reviewer Backend Running"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    text = ""

    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        return {"error": "Only PDF supported right now"}

    # 🔥 Case insensitive
    text = text.lower()

    # 🎯 Weighted scoring system (Total = 100)
    weights = {
        "education": 20,
        "experience": 30,
        "skills": 20,
        "projects": 15,
        "certifications": 15
    }

    detected_sections = {}
    score = 0

    for section, weight in weights.items():
        if section in text:
            detected_sections[section] = True
            score += weight
        else:
            detected_sections[section] = False

    missing_sections = [
        section for section, present in detected_sections.items() if not present
    ]

    # 🔥 AI-style suggestions
    suggestions = []

    if "experience" not in text:
        suggestions.append("Add detailed work experience with achievements.")

    if "skills" not in text:
        suggestions.append("Include technical and soft skills section.")

    if "projects" not in text:
        suggestions.append("Add projects with measurable results.")

    if "certifications" not in text:
        suggestions.append("Mention relevant certifications to boost credibility.")

    if score >= 80:
        level = "Excellent Resume"
    elif score >= 60:
        level = "Good Resume"
    elif score >= 40:
        level = "Average Resume"
    else:
        level = "Needs Improvement"

    return {
        "detected_sections": detected_sections,
        "missing_sections": missing_sections,
        "resume_score": score,
        "resume_level": level,
        "suggestions": suggestions
    }
