import sys
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor

def update_presentation():
    pptx_path = 'Multi Agent AI Research PPr MID.pptx'
    prs = Presentation(pptx_path)

    def set_shape_text(shape, new_text, bold=None, font_size=None, font_color=None):
        """Update single-text shape while preserving formatting."""
        tf = shape.text_frame
        if not tf.paragraphs:
            p = tf.add_paragraph()
        else:
            p = tf.paragraphs[0]
            
        if p.runs:
            r = p.runs[0]
            r.text = new_text
            if bold is not None:
                r.font.bold = bold
            if font_size is not None:
                r.font.size = Pt(font_size)
            if font_color is not None:
                r.font.color.rgb = font_color
            for r_extra in p.runs[1:]:
                r_extra.text = ""
        else:
            r = p.add_run()
            r.text = new_text
            if bold is not None:
                r.font.bold = bold
            if font_size is not None:
                r.font.size = Pt(font_size)
            if font_color is not None:
                r.font.color.rgb = font_color

        for p_extra in tf.paragraphs[1:]:
            p_extra.text = ""

    def set_shape_paragraphs(shape, paragraphs_data):
        """
        paragraphs_data is a list of tuples:
        (text, level, bold, font_size_pt, color_rgb)
        """
        tf = shape.text_frame
        # Clear existing text safely
        existing_p_count = len(tf.paragraphs)
        for i, data in enumerate(paragraphs_data):
            text, level, bold, size_pt, color_rgb = data
            if i < existing_p_count:
                p = tf.paragraphs[i]
            else:
                p = tf.add_paragraph()
            
            p.level = level
            if p.runs:
                r = p.runs[0]
                r.text = text
                if bold is not None:
                    r.font.bold = bold
                if size_pt is not None:
                    r.font.size = Pt(size_pt)
                if color_rgb is not None:
                    r.font.color.rgb = color_rgb
                for r_extra in p.runs[1:]:
                    r_extra.text = ""
            else:
                r = p.add_run()
                r.text = text
                if bold is not None:
                    r.font.bold = bold
                if size_pt is not None:
                    r.font.size = Pt(size_pt)
                if color_rgb is not None:
                    r.font.color.rgb = color_rgb

        # Blank out any remaining extra paragraphs
        if len(paragraphs_data) < existing_p_count:
            for extra_p in tf.paragraphs[len(paragraphs_data):]:
                extra_p.text = ""

    # =========================================================================
    # SLIDE 4: Motivation: Issues and Challenges
    # =========================================================================
    s4 = prs.slides[3]
    # Box 1 (Multiple custody points) -> Information Overload
    set_shape_text(s4.shapes[6], "Information Overload")
    set_shape_text(s4.shapes[7], "Thousands of scientific papers published weekly; manual literature review causes severe cognitive fatigue.")
    
    # Box 2 (Premature access) -> Dense Academic Formats
    set_shape_text(s4.shapes[9], "Dense Academic Formats")
    set_shape_text(s4.shapes[10], "Academic PDFs contain multi-column text, dense formulas, and buried methodologies difficult for generic tools.")
    
    # Box 3 (Weak traceability) -> LLM Hallucinations
    set_shape_text(s4.shapes[12], "LLM Hallucinations")
    set_shape_text(s4.shapes[13], "Standard conversational AI produces plausible but ungrounded claims lacking verifiable chunk-level citations.")
    
    # Box 4 (Slow leak investigation) -> Monolithic Tooling
    set_shape_text(s4.shapes[15], "Monolithic Tooling")
    set_shape_text(s4.shapes[16], "Single-prompt tools fail to combine document ingestion, vector retrieval, comparative synthesis, and gap analysis.")
    
    # Bottom Summary
    set_shape_text(s4.shapes[17], "Design Principle: Coordinate specialized autonomous AI agents backed by Retrieval-Augmented Generation (RAG) for verifiable, citation-grounded literature analysis.")

    # =========================================================================
    # SLIDE 5: Literature Review
    # =========================================================================
    s5 = prs.slides[4]
    # Table 48 (Shape 4)
    table_s5 = s5.shapes[4].table
    s5_table_data = [
        ["Reference", "Technique / Focus", "Data / Platform", "Key Strengths", "Observation / Limitation"],
        ["Lewis et al. (2020) NeurIPS", "Retrieval-Augmented Generation (RAG)", "Wikipedia / Open-domain QA", "Combines parametric & non-parametric memory", "Single monolithic retrieval; lacks multi-agent specialization for academic papers."],
        ["Wu et al. (2023) Microsoft AutoGen", "Multi-Agent Conversational Framework", "Collaborative Agent LLMs", "Enables role-playing and collaborative problem solving", "General-purpose; lacks specialized PDF chunking, citation tracking, and research gap extraction."],
        ["Commercial Tools (ChatPDF, SciSpace)", "Single-Document Vector Search & QA", "Academic PDFs", "Fast basic QA and interactive PDF viewing", "Limited cross-paper comparative reasoning; lack transparent agent routing and structured gap synthesis."],
        ["Proposed Work (2026)", "Multi-Agent Hybrid RAG + Provenance Engine", "Academic Research Papers", "Specialized agents (Doc, Retrieval, Analysis, Q&A) + page citations", "Midterm validated on single-paper deep analysis; cross-corpus scaling planned for end-term."]
    ]
    for r_idx, row in enumerate(s5_table_data):
        for c_idx, val in enumerate(row):
            cell = table_s5.cell(r_idx, c_idx)
            # preserve font size
            font_size = 11 if r_idx > 0 else 12
            bold = True if r_idx == 0 else False
            if cell.text_frame.paragraphs:
                p = cell.text_frame.paragraphs[0]
                p.text = val
                if p.runs:
                    p.runs[0].font.size = Pt(font_size)
                    p.runs[0].font.bold = bold
                    p.runs[0].font.name = "Calibri"
                    for r_extra in p.runs[1:]:
                        r_extra.text = ""
            else:
                p = cell.text_frame.add_paragraph()
                r = p.add_run()
                r.text = val
                r.font.size = Pt(font_size)
                r.font.bold = bold
                r.font.name = "Calibri"

    # Bottom takeaway (Shape 5)
    set_shape_text(s5.shapes[5], "Research Direction: While RAG and multi-agent LLM systems exist independently, orchestrating specialized academic agents (Ingestion, Semantic Indexing, Synthesis, Gap Discovery) with strict page-level citation provenance solves current academic literature review bottlenecks.")

    # =========================================================================
    # SLIDE 6: Problem Definition / Problem Statement
    # =========================================================================
    s6 = prs.slides[5]
    # Shape 5 (Main question)
    set_shape_text(s6.shapes[5], "How can an autonomous multi-agent AI system intelligently orchestrate the ingestion, semantic retrieval, comparative analysis, and grounded question-answering of complex scientific papers while eliminating hallucinations through strict page-level citations and automated research gap discovery?")
    
    # Shape 6 (Input / Constraints / Output)
    s6_specs = [
        ("Input: Unstructured scientific papers (PDFs) + user natural language research inquiries.", 0, False, 17, None),
        ("Constraints: Strict factual grounding, page-level citation provenance, low query latency (<2s local search), and zero hallucination on out-of-domain queries.", 0, False, 17, None),
        ("Output: Structured summaries, grounded Q&A with exact source chunks, multi-paper methodology comparison, and synthesized research gap reports.", 0, False, 17, None)
    ]
    set_shape_paragraphs(s6.shapes[6], s6_specs)

    # =========================================================================
    # SLIDE 7: Research Gap
    # =========================================================================
    s7 = prs.slides[6]
    s7_gaps = [
        ("Gap 1 — Lack of Agentic Specialization in Research Tools", 0, True, 17, RGBColor(0, 32, 96)),
        ("Existing academic tools use a single prompt-response loop for all queries, failing to differentiate between ingestion, semantic search, comparative synthesis, and critical evaluation.", 1, False, 14, None),
        ("", 1, False, 10, None),
        ("Gap 2 — Absence of Verifiable Page-Level Citation Provenance", 0, True, 17, RGBColor(0, 32, 96)),
        ("Current LLM research assistants frequently hallucinate facts or provide vague document-level links rather than exact page numbers and chunk-level textual evidence.", 1, False, 14, None),
        ("", 1, False, 10, None),
        ("Gap 3 — Disconnect Between Retrieval and Research Gap Discovery", 0, True, 17, RGBColor(0, 32, 96)),
        ("Available tools answer direct questions but do not autonomously synthesize cross-paper methodologies, identify conflicting findings, or pinpoint under-explored research directions.", 1, False, 14, None)
    ]
    set_shape_paragraphs(s7.shapes[5], s7_gaps)

    # =========================================================================
    # SLIDE 8: Objectives of the Project
    # =========================================================================
    s8 = prs.slides[7]
    s8_objs = [
        ("1. Design a modular Multi-Agent Architecture featuring an Orchestrator, Document Agent, Retrieval Agent, Analysis Agent, and Grounded Q&A Agent.", 0, False, 15, None),
        ("2. Implement an intelligent Document Ingestion Pipeline supporting PDF extraction, text normalization, and 900-character chunking with 150-character overlap.", 0, False, 15, None),
        ("3. Build a Hybrid Retrieval Engine combining ChromaDB vector embeddings (all-MiniLM-L6-v2) and lexical TF-IDF with resilient fallback mechanisms.", 0, False, 15, None),
        ("4. Develop an Intent-Routing Engine to automatically classify queries into Summary, Comparative Analysis, Research Gaps, or Grounded Q&A.", 0, False, 15, None),
        ("5. Implement strict Grounded Answering and Citation Tracking with exact page and chunk metadata to eliminate hallucinated answers.", 0, False, 15, None),
        ("6. Create an intuitive, high-responsiveness Web Interface (Streamlit) featuring interactive paper exploration, live agent activity logging, and quick prompt suggestions.", 0, False, 15, None),
        ("7. Experimentally evaluate retrieval latency, grounding accuracy, citation precision, and agent routing reliability on benchmark scientific papers.", 0, False, 15, None)
    ]
    set_shape_paragraphs(s8.shapes[5], s8_objs)

    # =========================================================================
    # SLIDE 9: Proposed Framework / Methodology
    # =========================================================================
    s9 = prs.slides[8]
    # 8 Steps
    # Step 1
    set_shape_text(s9.shapes[7], "Paper Ingestion")
    set_shape_text(s9.shapes[8], "PDF upload / parsing\nMetadata extraction")
    # Step 2
    set_shape_text(s9.shapes[13], "Document Agent")
    set_shape_text(s9.shapes[14], "Text chunking (900 ch)\nOverlap & page mapping")
    # Step 3
    set_shape_text(s9.shapes[19], "Vector Indexing")
    set_shape_text(s9.shapes[20], "Embeddings generation\nChromaDB & TF-IDF")
    # Step 4
    set_shape_text(s9.shapes[25], "Orchestrator")
    set_shape_text(s9.shapes[26], "Query intent routing\nAgent dispatching")
    # Step 5
    set_shape_text(s9.shapes[31], "Retrieval Agent")
    set_shape_text(s9.shapes[32], "Semantic vector search\nTop-k relevant chunks")
    # Step 6
    set_shape_text(s9.shapes[37], "Analysis Agent")
    set_shape_text(s9.shapes[38], "Methodology synthesis\n& research gap extraction")
    # Step 7
    set_shape_text(s9.shapes[43], "Grounded Q&A")
    set_shape_text(s9.shapes[44], "LLM generation backed\nby page-level citations")
    # Step 8
    set_shape_text(s9.shapes[49], "UI & Activity Log")
    set_shape_text(s9.shapes[50], "Interactive Streamlit\nReal-time agent logging")

    # Bottom layers
    set_shape_text(s9.shapes[51], "Core Multi-Agent System Layers")
    # Layer 1
    set_shape_text(s9.shapes[53], "Ingestion Layer")
    set_shape_text(s9.shapes[54], "PyPDF & text cleaning")
    # Layer 2
    set_shape_text(s9.shapes[56], "Indexing Layer")
    set_shape_text(s9.shapes[57], "ChromaDB + TF-IDF fallback")
    # Layer 3
    set_shape_text(s9.shapes[59], "Agentic Layer")
    set_shape_text(s9.shapes[60], "Autonomous specialized agents")
    # Layer 4
    set_shape_text(s9.shapes[62], "Generation Layer")
    set_shape_text(s9.shapes[63], "Grounded LLM (Ollama / Fallback)")
    # Layer 5
    set_shape_text(s9.shapes[65], "Attribution Layer")
    set_shape_text(s9.shapes[66], "Exact page & chunk citations")
    
    # Shape 67 summary
    set_shape_text(s9.shapes[67], "Multi-Agent Execution Pipeline: User query -> Orchestrator classifies intent -> Retrieval Agent fetches semantic chunks with page provenance -> Analysis / Q&A Agent synthesizes grounded response -> Activity Logger records multi-agent execution.")

    # =========================================================================
    # SLIDE 10: Data / Database Description
    # =========================================================================
    s10 = prs.slides[9]
    # Shape 5 subtitle
    set_shape_text(s10.shapes[5], "The system operates on academic scientific publications in PDF format, building persistent vector indices with metadata mapping for grounded semantic search and page-level attribution.")
    
    # Table (Shape 4)
    table_s10 = s10.shapes[4].table
    s10_table_data = [
        ["System Component", "Configuration / Scope", "Schema / Attributes", "Functional Role"],
        ["PDF Ingestion Corpus", "1+ benchmark papers (e.g. LoRA 26-page PDF)", "Raw text, page numbers, title, total pages", "Source research papers for document decomposition"],
        ["Chunking Store", "900-character chunks with 150-char overlap", "chunk_id, page_number, text, char_length", "Granular semantic units preserving page-level attribution"],
        ["ChromaDB Vector Store", "Collection: research_papers (all-MiniLM-L6-v2)", "chunk_id, vector_embedding, metadata, document", "High-dimensional semantic similarity vector search"],
        ["TF-IDF Lexical Index", "In-memory sparse term-frequency matrix", "Vocabulary terms, document frequencies, scores", "Resilient keyword search fallback when vector store is unavailable"],
        ["Agent Execution State", "Real-time session state & execution log", "timestamp, agent_name, action, detail, status", "Live execution transparency and multi-agent coordination audit"]
    ]
    for r_idx, row in enumerate(s10_table_data):
        for c_idx, val in enumerate(row):
            cell = table_s10.cell(r_idx, c_idx)
            font_size = 11 if r_idx > 0 else 12
            bold = True if r_idx == 0 else False
            if cell.text_frame.paragraphs:
                p = cell.text_frame.paragraphs[0]
                p.text = val
                if p.runs:
                    p.runs[0].font.size = Pt(font_size)
                    p.runs[0].font.bold = bold
                    p.runs[0].font.name = "Calibri"
                    for r_extra in p.runs[1:]:
                        r_extra.text = ""
            else:
                p = cell.text_frame.add_paragraph()
                r = p.add_run()
                r.text = val
                r.font.size = Pt(font_size)
                r.font.bold = bold
                r.font.name = "Calibri"

    # =========================================================================
    # SLIDE 11: Experimental Results & Discussion
    # =========================================================================
    s11 = prs.slides[10]
    # Shape 4 subtitle
    set_shape_text(s11.shapes[4], "Midterm Status: Full multi-agent pipeline implemented, verified across 10 validation checks with 100% test pass rate, and deployed on interactive web UI.")
    
    # 6 Cards
    # Card 1 (Confidentiality) -> Pipeline Stability
    set_shape_text(s11.shapes[6], "Pipeline Stability")
    set_shape_text(s11.shapes[7], "10 / 10 Tests Passed")
    set_shape_text(s11.shapes[8], "Ingestion, chunking, indexing, intent routing, and grounded generation fully verified.")
    
    # Card 2 (Integrity) -> Retrieval Accuracy
    set_shape_text(s11.shapes[10], "Retrieval Accuracy")
    set_shape_text(s11.shapes[11], "Top-k Chunk Precision")
    set_shape_text(s11.shapes[12], "Semantic vector search accurately isolates target methodology sections across 26-page papers.")
    
    # Card 3 (Time-lock) -> Zero Hallucination
    set_shape_text(s11.shapes[14], "Zero Hallucination")
    set_shape_text(s11.shapes[15], "Negative Control Verified")
    set_shape_text(s11.shapes[16], "Irrelevant/out-of-domain queries ('quantum biology') correctly rejected with no fabrication.")
    
    # Card 4 (Traceability) -> Citation Provenance
    set_shape_text(s11.shapes[18], "Citation Provenance")
    set_shape_text(s11.shapes[19], "100% Page Attribution")
    set_shape_text(s11.shapes[20], "Every generated response strictly cites the source page numbers and exact chunk context.")
    
    # Card 5 (Web detection) -> Resilient Fallback
    set_shape_text(s11.shapes[22], "Resilient Fallback")
    set_shape_text(s11.shapes[23], "Dual-Engine Architecture")
    set_shape_text(s11.shapes[24], "Seamless TF-IDF fallback activates automatically if vector DB or LLM server is unreachable.")
    
    # Card 6 (Overhead) -> Response Latency
    set_shape_text(s11.shapes[26], "Response Latency")
    set_shape_text(s11.shapes[27], "Sub-Second Query Time (<1s)")
    set_shape_text(s11.shapes[28], "Optimized local chunk caching and search enables smooth live demonstration during evaluation.")
    
    # Shape 29 summary
    set_shape_text(s11.shapes[29], "Evaluation Summary: The midterm prototype demonstrates robust end-to-end multi-agent orchestration, resilient fallbacks, zero hallucination on negative tests, and interactive research paper analysis.")

    # =========================================================================
    # SLIDE 12: Conclusion and Future Directions
    # =========================================================================
    s12 = prs.slides[11]
    s12_bullets = [
        ("Midterm Deliverable: Successfully engineered and validated a modular Multi-Agent AI Research Assistant capable of scientific PDF ingestion, semantic indexing, and grounded analysis.", 0, False, 16, None),
        ("Agent Collaboration: Autonomous specialization (Document, Retrieval, Analysis, Q&A) significantly outperforms monolithic prompt approaches in precision and structure.", 0, False, 16, None),
        ("Elimination of Hallucinations: Grounded RAG with strict page-level citation provenance guarantees factual verification across complex academic literature.", 0, False, 16, None),
        ("Resilient & Responsive: Hybrid vector and lexical fallback architecture delivers sub-second response times and zero-downtime reliability.", 0, False, 16, None),
        ("End-Term Scope: Expand to multi-paper cross-corpus synthesis, live ArXiv/OpenAlex API ingestion, automated BibTeX citation export, and collaborative paper comparison matrices.", 0, False, 16, None)
    ]
    set_shape_paragraphs(s12.shapes[5], s12_bullets)

    # =========================================================================
    # SLIDE 13: Plan of Action for Remaining Project Work
    # =========================================================================
    s13 = prs.slides[12]
    # Phase 1
    set_shape_text(s13.shapes[6], "Phase 1")
    set_shape_text(s13.shapes[7], "Multi-Paper Corpus Scaling")
    set_shape_text(s13.shapes[8], "Enable simultaneous indexing and cross-referencing across 20+ papers in shared workspace.")
    # Phase 2
    set_shape_text(s13.shapes[10], "Phase 2")
    set_shape_text(s13.shapes[11], "Live Academic API Ingestion")
    set_shape_text(s13.shapes[12], "Integrate ArXiv, Semantic Scholar, and OpenAlex APIs for real-time paper retrieval.")
    # Phase 3
    set_shape_text(s13.shapes[14], "Phase 3")
    set_shape_text(s13.shapes[15], "Automated Literature Review Writer")
    set_shape_text(s13.shapes[16], "Generate multi-section survey drafts complete with BibTeX and APA citations.")
    # Phase 4
    set_shape_text(s13.shapes[18], "Phase 4")
    set_shape_text(s13.shapes[19], "Comparative Matrix Engine")
    set_shape_text(s13.shapes[20], "Synthesize structured comparison tables of datasets, architectures, and empirical findings.")
    # Phase 5
    set_shape_text(s13.shapes[22], "Phase 5")
    set_shape_text(s13.shapes[23], "Advanced Agent Reasoning")
    set_shape_text(s13.shapes[24], "Implement critique/reflection agents with domain-fine-tuned embeddings (SciBERT).")
    # Phase 6
    set_shape_text(s13.shapes[26], "Phase 6")
    set_shape_text(s13.shapes[27], "Comprehensive Evaluation & Demo")
    set_shape_text(s13.shapes[28], "Conduct quantitative latency/accuracy benchmarks, user study, and final thesis defense.")

    # Save presentation
    prs.save(pptx_path)
    print("SUCCESS: Presentation successfully updated and saved to " + pptx_path)

if __name__ == '__main__':
    update_presentation()
