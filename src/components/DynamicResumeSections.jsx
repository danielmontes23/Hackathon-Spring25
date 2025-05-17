import React, { useState, useEffect } from "react";

const getInitial = (key, fallback) => {
  if (typeof window !== "undefined") {
    const saved = localStorage.getItem(key);
    if (saved) return JSON.parse(saved);
  }
  return fallback;
};

export default function DynamicResumeSections() {
  // High School and College fields
  const [highSchool, setHighSchool] = useState(() => getInitial("highSchool", { name: "", grad: "" }));
  const [college, setCollege] = useState(() => getInitial("college", { name: "", degree: "", grad: "" }));
  const [noCollege, setNoCollege] = useState(() => getInitial("noCollege", false));

  // Dynamic additional schools
  const [education, setEducation] = useState(() => getInitial("education", []));

  // Experience and Skills (unchanged)
  const [experience, setExperience] = useState(() => getInitial("experience", [
    { company: "", role: "", start: "", end: "" }
  ]));
  const [skills, setSkills] = useState(() => getInitial("skills", [""]));
  const [customSections, setCustomSections] = useState(() => getInitial("customSections", [
    { label: "", content: "" }
  ]));

  // Persist to localStorage
  useEffect(() => { localStorage.setItem("highSchool", JSON.stringify(highSchool)); }, [highSchool]);
  useEffect(() => { localStorage.setItem("college", JSON.stringify(college)); }, [college]);
  useEffect(() => { localStorage.setItem("noCollege", JSON.stringify(noCollege)); }, [noCollege]);
  useEffect(() => { localStorage.setItem("education", JSON.stringify(education)); }, [education]);
  useEffect(() => { localStorage.setItem("experience", JSON.stringify(experience)); }, [experience]);
  useEffect(() => { localStorage.setItem("skills", JSON.stringify(skills)); }, [skills]);
  useEffect(() => { localStorage.setItem("customSections", JSON.stringify(customSections)); }, [customSections]);

  // Handlers for dynamic education
  const addEducation = () =>
    setEducation([...education, { school: "", degree: "", grad: "", notApplicable: false }]);
  const removeEducation = idx =>
    education.length > 1 && setEducation(education.filter((_, i) => i !== idx));
  const handleEducation = (idx, field, value) => {
    const updated = [...education];
    updated[idx][field] = value;
    setEducation(updated);
  };

  // Experience handlers
  const addExperience = () =>
    setExperience([...experience, { company: "", role: "", start: "", end: "" }]);
  const removeExperience = idx =>
    experience.length > 1 && setExperience(experience.filter((_, i) => i !== idx));
  const handleExperience = (idx, field, value) => {
    const updated = [...experience];
    updated[idx][field] = value;
    setExperience(updated);
  };

  // Skills handlers
  const addSkill = () => setSkills([...skills, ""]);
  const removeSkill = idx =>
    skills.length > 1 && setSkills(skills.filter((_, i) => i !== idx));
  const handleSkill = (idx, value) => {
    const updated = [...skills];
    updated[idx] = value;
    setSkills(updated);
  };

  // Custom sections handlers
  const addCustomSection = () =>
    setCustomSections([...customSections, { label: "", content: "" }]);
  const removeCustomSection = idx =>
    customSections.length > 1 && setCustomSections(customSections.filter((_, i) => i !== idx));
  const handleCustomSection = (idx, field, value) => {
    const updated = [...customSections];
    updated[idx][field] = value;
    setCustomSections(updated);
  };

  return (
    <>
      <section>
        <h2>Education</h2>
        {/* High School */}
        <div style={{border: "1px solid #eee", padding: "1rem", borderRadius: "6px", marginBottom: "1rem"}}>
          <h3>High School</h3>
          <label>
            School Name:
            <input
              type="text"
              name="high_school_name"
              value={highSchool.name}
              onChange={e => setHighSchool({ ...highSchool, name: e.target.value })}
              required
            />
          </label>
          <label>
            Start Year:
            <input
              type="text"
              name="high_school_start"
              value={highSchool.start || ""}
              onChange={e => setHighSchool({ ...highSchool, start: e.target.value })}
              required
            />
          </label>
          <label>
            Graduation Year:
            <input
              type="text"
              name="high_school_grad"
              value={highSchool.grad}
              onChange={e => setHighSchool({ ...highSchool, grad: e.target.value })}
              required
            />
          </label>
        </div>
        {/* College */}
        <div style={{border: "1px solid #eee", padding: "1rem", borderRadius: "6px", marginBottom: "1rem"}}>
          <h3>College</h3>
          <label style={{display: "flex", alignItems: "center", gap: "0.5rem"}}>
            <input
              type="checkbox"
              checked={noCollege}
              onChange={e => setNoCollege(e.target.checked)}
            />
            I did not attend college
          </label>
          <label>
            College/University Name:
            <input
              type="text"
              name="college_name"
              value={college.name}
              onChange={e => setCollege({ ...college, name: e.target.value })}
              disabled={noCollege}
              required={!noCollege}
            />
          </label>
          <label>
            Start Year:
            <input
              type="text"
              name="college_start"
              value={college.start || ""}
              onChange={e => setCollege({ ...college, start: e.target.value })}
              disabled={noCollege}
              required={!noCollege}
            />
          </label>
          <label>
            Graduation Year:
            <input
              type="text"
              name="college_grad"
              value={college.grad}
              onChange={e => setCollege({ ...college, grad: e.target.value })}
              disabled={noCollege}
              required={!noCollege}
            />
          </label>
          <label>
            Degree:
            <input
              type="text"
              name="college_degree"
              value={college.degree}
              onChange={e => setCollege({ ...college, degree: e.target.value })}
              disabled={noCollege}
              required={!noCollege}
            />
          </label>
        </div>
        {/* Other Schools */}
        {education.length > 0 && (
          <>
            <h3>Other Schools</h3>
            {education.map((edu, idx) => (
              <div key={idx} style={{border: "1px solid #eee", padding: "1rem", marginBottom: "1rem", borderRadius: "6px"}}>
                <label style={{display: "flex", alignItems: "center", gap: "0.5rem"}}>
                  <input
                    type="checkbox"
                    checked={edu.notApplicable || false}
                    onChange={e => handleEducation(idx, "notApplicable", e.target.checked)}
                  />
                  Not Applicable
                </label>
                <label>
                  School Name:
                  <input
                    type="text"
                    name={`education_school_${idx}`}
                    value={edu.school}
                    onChange={e => handleEducation(idx, "school", e.target.value)}
                    required
                    disabled={edu.notApplicable}
                  />
                </label>
                <label>
                  Degree:
                  <input
                    type="text"
                    name={`education_degree_${idx}`}
                    value={edu.degree}
                    onChange={e => handleEducation(idx, "degree", e.target.value)}
                    required
                    disabled={edu.notApplicable}
                  />
                </label>
                <label>
                  Graduation Year:
                  <input
                    type="text"
                    name={`education_grad_${idx}`}
                    value={edu.grad}
                    onChange={e => handleEducation(idx, "grad", e.target.value)}
                    required
                    disabled={edu.notApplicable}
                  />
                </label>
                <button type="button" onClick={() => removeEducation(idx)} disabled={education.length === 1}>Delete</button>
              </div>
            ))}
          </>
        )}
        <button type="button" onClick={addEducation}>Add Another School</button>
      </section>

      <section>
        <h2>Experience</h2>
        {experience.map((exp, idx) => (
          <div key={idx} style={{border: "1px solid #eee", padding: "1rem", marginBottom: "1rem", borderRadius: "6px"}}>
            <label>
              Company:
              <input type="text" name={`experience_company_${idx}`} value={exp.company}
                onChange={e => handleExperience(idx, "company", e.target.value)} required />
            </label>
            <label>
              Role:
              <input type="text" name={`experience_role_${idx}`} value={exp.role}
                onChange={e => handleExperience(idx, "role", e.target.value)} required />
            </label>
            <label>
              Start Date:
              <input type="text" name={`experience_start_${idx}`} value={exp.start}
                onChange={e => handleExperience(idx, "start", e.target.value)} required />
            </label>
            <label>
              End Date:
              <input type="text" name={`experience_end_${idx}`} value={exp.end}
                onChange={e => handleExperience(idx, "end", e.target.value)} required />
            </label>
            <button type="button" onClick={() => removeExperience(idx)} disabled={experience.length === 1}>Delete</button>
          </div>
        ))}
        <button type="button" onClick={addExperience}>Add Experience</button>
      </section>

      <section>
        <h2>Skills</h2>
        {skills.map((skill, idx) => (
          <div key={idx} style={{display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem"}}>
            <input type="text" name={`skill_${idx}`} value={skill}
              onChange={e => handleSkill(idx, e.target.value)} required />
            <button type="button" onClick={() => removeSkill(idx)} disabled={skills.length === 1}>Delete</button>
          </div>
        ))}
        <button type="button" onClick={addSkill}>Add Skill</button>
      </section>

      <section>
        <h2>Custom Sections</h2>
        {customSections.map((section, idx) => (
          <div key={idx} style={{border: "1px solid #eee", padding: "1rem", marginBottom: "1rem", borderRadius: "6px"}}>
            <label>
              Section Label:
              <input type="text" name={`custom_section_label_${idx}`} value={section.label}
                onChange={e => handleCustomSection(idx, "label", e.target.value)} required />
            </label>
            <label>
              Content:
              <textarea name={`custom_section_content_${idx}`} value={section.content}
                onChange={e => handleCustomSection(idx, "content", e.target.value)} required />
            </label>
            <button type="button" onClick={() => removeCustomSection(idx)} disabled={customSections.length === 1}>Delete</button>
          </div>
        ))}
        <button type="button" onClick={addCustomSection}>Add Custom Section</button>
      </section>
    </>
  );
}