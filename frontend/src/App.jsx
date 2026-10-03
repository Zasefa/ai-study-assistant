import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState("ask");

  // Separate input for each feature
  const [askQuestionText, setAskQuestionText] = useState("");
  const [pdfQuestion, setPdfQuestion] = useState("");
  const [mcqTopic, setMcqTopic] = useState("");

  const [answer, setAnswer] = useState(null);

  const [file, setFile] = useState(null);
  const [documentId, setDocumentId] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");

  const [mcqs, setMcqs] = useState(null);

  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [checkedAnswers, setCheckedAnswers] = useState({});

  const [loading, setLoading] = useState(false);


  // ==========================================
  // ASK AI
  // ==========================================

  const askQuestion = async () => {
    if (!askQuestionText.trim()) return;

    try {
      setLoading(true);
      setAnswer(null);

      const response = await axios.post(
        `${API_URL}/ask`,
        {
          question: askQuestionText
        }
      );

      setAnswer(response.data.answer);

      // Clear textbox after submitting
      setAskQuestionText("");

    } catch (error) {
      console.error("Ask AI Error:", error);

      setAnswer({
        error:
          error.response?.data?.detail?.message ||
          "Something went wrong. Please try again."
      });

    } finally {
      setLoading(false);
    }
  };


  // ==========================================
  // UPLOAD PDF
  // ==========================================

  const uploadPDF = async () => {
    if (!file) {
      setUploadMessage("Please select a PDF first.");
      return;
    }

    try {
      setLoading(true);
      setUploadMessage("");

      const formData = new FormData();

      formData.append("file", file);

      const response = await axios.post(
        `${API_URL}/upload-pdf`,
        formData
      );

      setDocumentId(
        response.data.document_id
      );

      setUploadMessage(
        `✓ ${response.data.filename} uploaded successfully`
      );

      // Clear selected file
      setFile(null);

    } catch (error) {
      console.error("PDF Upload Error:", error);

      setUploadMessage(
        error.response?.data?.detail?.message ||
        error.response?.data?.detail ||
        "PDF upload failed."
      );

    } finally {
      setLoading(false);
    }
  };


  // ==========================================
  // ASK PDF
  // ==========================================

  const askPDF = async () => {
    if (!pdfQuestion.trim()) {
      return;
    }

    if (!documentId) {
      setAnswer({
        error: "Please upload a PDF first."
      });

      return;
    }

    try {
      setLoading(true);
      setAnswer(null);

      const response = await axios.post(
        `${API_URL}/ask-pdf`,
        {
          question: pdfQuestion,
          session_id: "student1",
          document_id: documentId
        }
      );

      setAnswer({
        text: response.data.answer,
        sources: response.data.sources
      });

      // Clear PDF question
      setPdfQuestion("");

    } catch (error) {
      console.error("PDF Question Error:", error);

      setAnswer({
        error:
          error.response?.data?.detail?.message ||
          error.response?.data?.detail ||
          "Could not get an answer from the PDF."
      });

    } finally {
      setLoading(false);
    }
  };


  // ==========================================
  // GENERATE MCQS
  // ==========================================

  const generateMCQs = async () => {
    if (!mcqTopic.trim()) {
      return;
    }

    try {
      setLoading(true);

      setMcqs(null);

      setSelectedAnswers({});
      setCheckedAnswers({});

      const response = await axios.post(
        `${API_URL}/generate-mcq`,
        {
          question: mcqTopic
        }
      );

      setMcqs(response.data);

      // Clear MCQ topic
      setMcqTopic("");

    } catch (error) {
      console.error("MCQ Error:", error);

      setMcqs({
        error:
          error.response?.data?.detail?.message ||
          error.response?.data?.detail ||
          "Could not generate MCQs."
      });

    } finally {
      setLoading(false);
    }
  };


  // ==========================================
  // SELECT MCQ OPTION
  // ==========================================

  const selectAnswer = (
    questionIndex,
    option
  ) => {

    // Don't allow changing after checking
    if (checkedAnswers[questionIndex]) {
      return;
    }

    setSelectedAnswers(
      (previous) => ({
        ...previous,
        [questionIndex]: option
      })
    );
  };


  // ==========================================
  // CHECK MCQ ANSWER
  // ==========================================

  const checkAnswer = (
    questionIndex
  ) => {

    if (!selectedAnswers[questionIndex]) {
      return;
    }

    setCheckedAnswers(
      (previous) => ({
        ...previous,
        [questionIndex]: true
      })
    );
  };


  // ==========================================
  // SIDEBAR TAB CHANGE
  // ==========================================

  const changeTab = (tab) => {

    setActiveTab(tab);

    setAnswer(null);

    if (tab === "mcq") {
      setMcqs(null);
      setSelectedAnswers({});
      setCheckedAnswers({});
    }
  };


  return (
    <div className="app">


      {/* ======================================
          SIDEBAR
      ====================================== */}

      <aside className="sidebar">

        <div className="logo">

          <div className="logo-icon">
            ✦
          </div>

          <div>

            <h2>
              StudyAI
            </h2>

            <span>
              AI Study Assistant
            </span>

          </div>

        </div>


        <nav>

          <button
            className={
              activeTab === "ask"
                ? "nav-active"
                : ""
            }
            onClick={() =>
              changeTab("ask")
            }
          >

            <span>
              💡
            </span>

            Ask AI

          </button>


          <button
            className={
              activeTab === "pdf"
                ? "nav-active"
                : ""
            }
            onClick={() =>
              changeTab("pdf")
            }
          >

            <span>
              📄
            </span>

            Study PDF

          </button>


          <button
            className={
              activeTab === "mcq"
                ? "nav-active"
                : ""
            }
            onClick={() =>
              changeTab("mcq")
            }
          >

            <span>
              🧠
            </span>

            Practice MCQs

          </button>

        </nav>


        <div className="sidebar-bottom">

          <div className="student-card">

            <div className="avatar">
              S
            </div>

            <div>

              <strong>
                Student
              </strong>

              <small>
                Learning mode
              </small>

            </div>

          </div>

        </div>

      </aside>


      {/* ======================================
          MAIN
      ====================================== */}

      <main className="main">


        {/* ====================================
            TOP BAR
        ==================================== */}

        <header className="topbar">

          <div>

            <span className="eyebrow">
              YOUR PERSONAL AI TUTOR
            </span>

            <h1>
              Learn smarter,
              <span> study better.</span>
            </h1>

            <p>
              Ask questions, study your PDFs
              and practice with AI-generated MCQs.
            </p>

          </div>


          <div className="status">

            <span></span>

            AI Assistant

          </div>

        </header>


        {/* ====================================
            ASK AI
        ==================================== */}

        {activeTab === "ask" && (

          <section className="content">

            <div className="hero-card">

              <div className="hero-icon">
                ✨
              </div>

              <div>

                <h2>
                  What do you want to learn?
                </h2>

                <p>
                  Ask anything about programming,
                  AI, ML, computer science and more.
                </p>

              </div>

            </div>


            <div className="input-card">

              <textarea
                value={askQuestionText}
                onChange={(e) =>
                  setAskQuestionText(
                    e.target.value
                  )
                }
                placeholder="e.g. Explain logistic regression in simple words..."
              />


              <div className="input-footer">

                <span>
                  💬 Ask your question
                </span>


                <button
                  className="primary-btn"
                  onClick={askQuestion}
                  disabled={loading}
                >

                  {loading
                    ? "Thinking..."
                    : "Ask AI →"}

                </button>

              </div>

            </div>


            {answer && (
              <AnswerCard
                answer={answer}
              />
            )}

          </section>

        )}


        {/* ====================================
            STUDY PDF
        ==================================== */}

        {activeTab === "pdf" && (

          <section className="content">


            <div className="section-heading">

              <div>

                <span className="eyebrow">
                  DOCUMENT STUDY
                </span>

                <h2>
                  Study from your PDF
                </h2>

                <p>
                  Upload your notes, presentations
                  or study material and ask questions
                  directly from them.
                </p>

              </div>


              <div className="large-icon">
                📚
              </div>

            </div>


            {/* PDF UPLOAD */}

            <div className="upload-card">

              <div className="upload-icon">
                ↑
              </div>

              <h3>
                Upload your study material
              </h3>

              <p>
                PDF files only
              </p>


              <label className="file-button">

                Choose PDF

                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) =>
                    setFile(
                      e.target.files[0]
                    )
                  }
                />

              </label>


              {file && (

                <div className="selected-file">

                  📄 {file.name}

                </div>

              )}


              <button
                className="primary-btn"
                onClick={uploadPDF}
                disabled={loading}
              >

                {loading
                  ? "Uploading..."
                  : "Upload PDF"}

              </button>


              {uploadMessage && (

                <p className="upload-message">

                  {uploadMessage}

                </p>

              )}

            </div>


            {/* PDF QUESTION */}

            <div className="input-card pdf-question">

              <div className="pdf-label">

                <span>
                  📄
                </span>

                Ask about your document

              </div>


              <textarea
                value={pdfQuestion}
                onChange={(e) =>
                  setPdfQuestion(
                    e.target.value
                  )
                }
                placeholder="e.g. Explain the main objective of this project..."
              />


              <button
                className="primary-btn"
                onClick={askPDF}
                disabled={loading}
              >

                {loading
                  ? "Searching..."
                  : "Ask From PDF →"}

              </button>

            </div>


            {answer && (

              <AnswerCard
                answer={answer}
              />

            )}

          </section>

        )}


        {/* ====================================
            MCQ
        ==================================== */}

        {activeTab === "mcq" && (

          <section className="content">


            <div className="section-heading">

              <div>

                <span className="eyebrow">
                  PRACTICE MODE
                </span>

                <h2>
                  Test your knowledge
                </h2>

                <p>
                  Enter a topic and let AI create
                  practice questions for you.
                </p>

              </div>


              <div className="large-icon">
                🧠
              </div>

            </div>


            {/* MCQ INPUT */}

            <div className="input-card">

              <textarea
                value={mcqTopic}
                onChange={(e) =>
                  setMcqTopic(
                    e.target.value
                  )
                }
                placeholder="e.g. Machine Learning, DBMS, Operating Systems..."
              />


              <div className="input-footer">

                <span>
                  🎯 5 questions will be generated
                </span>


                <button
                  className="primary-btn"
                  onClick={generateMCQs}
                  disabled={loading}
                >

                  {loading
                    ? "Creating..."
                    : "Generate MCQs →"}

                </button>

              </div>

            </div>


            {/* MCQ RESULTS */}

            {mcqs && (

              <div className="mcq-container">

                {mcqs.error ? (

                  <div className="error-card">

                    {mcqs.error}

                  </div>

                ) : (

                  <>

                    <h2>
                      Practice Questions
                    </h2>


                    {mcqs.questions?.map(
                      (mcq, index) => {

                        const selected =
                          selectedAnswers[index];

                        const checked =
                          checkedAnswers[index];

                        const correct =
                          selected ===
                          mcq.correct_answer;


                        return (

                          <div
                            className="mcq-card"
                            key={index}
                          >

                            <span className="question-number">

                              QUESTION {index + 1}

                            </span>


                            <h3>
                              {mcq.question}
                            </h3>


                            {/* OPTIONS */}

                            <div className="options">

                              {mcq.options?.map(
                                (
                                  option,
                                  optionIndex
                                ) => (

                                  <button
                                    key={optionIndex}
                                    className={
                                      `option ${
                                        selected === option
                                          ? "selected-option"
                                          : ""
                                      }`
                                    }
                                    onClick={() =>
                                      selectAnswer(
                                        index,
                                        option
                                      )
                                    }
                                    disabled={checked}
                                  >

                                    <span>

                                      {String.fromCharCode(
                                        65 +
                                        optionIndex
                                      )}

                                    </span>

                                    {option}

                                  </button>

                                )
                              )}

                            </div>


                            {/* CHECK BUTTON */}

                            {!checked && (

                              <button
                                className="check-btn"
                                onClick={() =>
                                  checkAnswer(
                                    index
                                  )
                                }
                                disabled={!selected}
                              >

                                Check Answer

                              </button>

                            )}


                            {/* RESULT */}

                            {checked && (

                              <div
                                className={
                                  correct
                                    ? "correct-answer"
                                    : "wrong-answer"
                                }
                              >

                                {correct ? (

                                  <>

                                    <strong>
                                      ✓ Correct!
                                    </strong>

                                    <p>
                                      {mcq.explanation}
                                    </p>

                                  </>

                                ) : (

                                  <>

                                    <strong>
                                      ✗ Incorrect
                                    </strong>

                                    <p>
                                      Your answer:{" "}
                                      <strong>
                                        {selected}
                                      </strong>
                                    </p>

                                    <p>
                                      Correct answer:{" "}
                                      <strong>
                                        {mcq.correct_answer}
                                      </strong>
                                    </p>

                                    <p>
                                      {mcq.explanation}
                                    </p>

                                  </>

                                )}

                              </div>

                            )}

                          </div>

                        );

                      }
                    )}

                  </>

                )}

              </div>

            )}

          </section>

        )}

      </main>

    </div>
  );
}


// ==========================================
// ANSWER CARD
// ==========================================

function AnswerCard({ answer }) {

  // ERROR

  if (answer.error) {

    return (

      <div className="error-card">

        <strong>
          Something went wrong
        </strong>

        <p>
          {answer.error}
        </p>

      </div>

    );

  }


  // NORMAL AI ANSWER

  if (answer.definition) {

    return (

      <div className="answer-card">

        <span className="eyebrow">
          AI EXPLANATION
        </span>


        <h2>
          {answer.topic}
        </h2>


        <div className="answer-section">

          <h3>
            What is it?
          </h3>

          <p>
            {answer.definition}
          </p>

        </div>


        <div className="answer-section">

          <h3>
            How does it work?
          </h3>

          <p>
            {answer.how_it_works}
          </p>

        </div>


        <div className="answer-section">

          <h3>
            Real-world example
          </h3>

          <p>
            {answer.real_world_example}
          </p>

        </div>


        <div className="interview-box">

          <strong>
            💼 Interview Question
          </strong>

          <p>
            {answer.interview_question}
          </p>

        </div>

      </div>

    );

  }


  // PDF ANSWER

  return (

    <div className="answer-card">

      <span className="eyebrow">
        DOCUMENT ANSWER
      </span>


      <p className="pdf-answer">
        {answer.text}
      </p>


      {answer.sources?.length > 0 && (

        <div className="sources">

          <strong>
            📌 Source pages
          </strong>


          <div>

            {answer.sources.map(
              (source, index) => (

                <span key={index}>
                  Page {source.page}
                </span>

              )
            )}

          </div>

        </div>

      )}

    </div>

  );
}


export default App;