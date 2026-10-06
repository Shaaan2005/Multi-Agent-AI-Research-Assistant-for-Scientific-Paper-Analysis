from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def fix_all_presentation_issues():
    pptx_path = 'Multi Agent AI Research PPr MID.pptx'
    prs = Presentation(pptx_path)

    def set_clean_text(shape, text, font_name="Calibri", font_size=None, bold=None, color_rgb=None, space_after=None):
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_top = Pt(2)
        tf.margin_bottom = Pt(2)
        tf.margin_left = Pt(4)
        tf.margin_right = Pt(4)
        
        # Clear extra paragraphs
        if len(tf.paragraphs) > 1:
            for p_extra in tf.paragraphs[1:]:
                p_extra.text = ""
        p = tf.paragraphs[0]
        p.text = text
        if space_after is not None:
            p.space_after = Pt(space_after)
        if p.runs:
            r = p.runs[0]
            if font_name:
                r.font.name = font_name
            if font_size:
                r.font.size = Pt(font_size)
            if bold is not None:
                r.font.bold = bold
            if color_rgb:
                r.font.color.rgb = color_rgb
            for r_extra in p.runs[1:]:
                r_extra.text = ""

    # =========================================================================
    # SLIDE 1: Title Slide (Fix overlaps, remove underscores)
    # =========================================================================
    s1 = prs.slides[0]
    # Shape 1: Title
    s1.shapes[1].top = Inches(1.85)
    s1.shapes[1].height = Inches(1.80)
    
    # Shape 5: Group Members (left box)
    s1.shapes[5].left = Inches(0.40)
    s1.shapes[5].top = Inches(4.00)
    s1.shapes[5].width = Inches(4.80)
    s1.shapes[5].height = Inches(0.70)
    
    # Shape 2: Supervisor (middle box - remove underscores)
    s1.shapes[2].left = Inches(5.30)
    s1.shapes[2].top = Inches(4.00)
    s1.shapes[2].width = Inches(3.80)
    s1.shapes[2].height = Inches(0.70)
    set_clean_text(s1.shapes[2], "Supervisor: Dr. O.P. Vyas", font_name="Georgia", font_size=20, bold=False)
    
    # Shape 3: Date (right box)
    s1.shapes[3].left = Inches(9.30)
    s1.shapes[3].top = Inches(4.00)
    s1.shapes[3].width = Inches(3.40)
    s1.shapes[3].height = Inches(0.70)
    set_clean_text(s1.shapes[3], "Date: 06/10/2026", font_name="Georgia", font_size=20, bold=False)

    # =========================================================================
    # SLIDE 5: Literature Review (Rebalance columns, fix title height & padding)
    # =========================================================================
    s5 = prs.slides[4]
    # Reduce title box height so it does not collide with table
    s5.shapes[0].height = Inches(0.90)
    
    # Table 48
    s5.shapes[4].top = Inches(1.55)
    s5.shapes[4].height = Inches(4.80)
    table_s5 = s5.shapes[4].table
    # Rebalance columns: total 12.15"
    table_s5.columns[0].width = Inches(2.10)
    table_s5.columns[1].width = Inches(2.30)
    table_s5.columns[2].width = Inches(1.70)
    table_s5.columns[3].width = Inches(2.40) # was 1.55", now 2.40"
    table_s5.columns[4].width = Inches(3.65)
    
    s5_table_data = [
        ["Reference", "Technique / Focus", "Data / Platform", "Key Strengths", "Observation / Limitation"],
        ["Lewis et al. (2020)\nNeurIPS", "Retrieval-Augmented Generation (RAG)", "Wikipedia / Open-domain QA", "Combines parametric & non-parametric memory", "Single monolithic retrieval; lacks multi-agent specialization for academic papers."],
        ["Wu et al. (2023)\nMicrosoft AutoGen", "Multi-Agent Conversational Framework", "Collaborative Agent LLMs", "Enables role-playing and collaborative problem solving", "General-purpose; lacks specialized PDF chunking, citation tracking, and research gap extraction."],
        ["Commercial Tools\n(ChatPDF, SciSpace)", "Single-Document Vector Search & QA", "Academic PDFs", "Fast basic QA and interactive PDF viewing", "Limited cross-paper comparative reasoning; lack transparent agent routing and structured gap synthesis."],
        ["Proposed Work\n(2026)", "Multi-Agent Hybrid RAG + Provenance Engine", "Academic Research Papers", "Specialized agents (Doc, Retrieval, Analysis, Q&A) + page citations", "Midterm validated on single-paper deep analysis; cross-corpus scaling planned for end-term."]
    ]
    for r_idx, row in enumerate(s5_table_data):
        for c_idx, val in enumerate(row):
            cell = table_s5.cell(r_idx, c_idx)
            cell.margin_top = Pt(3)
            cell.margin_bottom = Pt(3)
            cell.margin_left = Pt(5)
            cell.margin_right = Pt(5)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = "Calibri"
            r.font.size = Pt(11 if r_idx == 0 else 9.5)
            r.font.bold = (r_idx == 0)

    # Bottom Takeaway box
    s5.shapes[5].top = Inches(6.50)
    s5.shapes[5].height = Inches(0.40)
    set_clean_text(s5.shapes[5], "Research Direction: While RAG and multi-agent LLM systems exist independently, orchestrating specialized academic agents (Ingestion, Semantic Indexing, Synthesis, Gap Discovery) with strict page-level citation provenance solves current academic literature review bottlenecks.", font_name="Calibri", font_size=10.5)

    # =========================================================================
    # SLIDE 9: Proposed Framework / Methodology (FIX CARD OVERFLOW COMPLETELY)
    # =========================================================================
    s9 = prs.slides[8]
    # Reduce title placeholder height
    s9.shapes[0].height = Inches(0.85)

    # 8 Steps data: (card_shape, oval_shape, num_shape, title_shape, desc_shape, title_text, desc_text)
    step_indices = [
        (4, 5, 6, 7, 8, "Paper Ingestion", "PDF upload / parsing\nMetadata extraction"),
        (10, 11, 12, 13, 14, "Document Agent", "900-char chunking\nPage-level mapping"),
        (16, 17, 18, 19, 20, "Vector Indexing", "Dense vector index\nChromaDB & TF-IDF"),
        (22, 23, 24, 25, 26, "Orchestrator", "Intent classification\nAgent dispatching"),
        (28, 29, 30, 31, 32, "Retrieval Agent", "Semantic vector search\nTop-k relevant chunks"),
        (34, 35, 36, 37, 38, "Analysis Agent", "Methodology review\nResearch gap synthesis"),
        (40, 41, 42, 43, 44, "Grounded Q&A", "Contextual answers\nPage-level citations"),
        (46, 47, 48, 49, 50, "UI & Activity Log", "Interactive Streamlit\nLive agent audit log"),
    ]

    for (c_idx, o_idx, n_idx, t_idx, d_idx, title_txt, desc_txt) in step_indices:
        card = s9.shapes[c_idx]
        oval = s9.shapes[o_idx]
        num_box = s9.shapes[n_idx]
        title_box = s9.shapes[t_idx]
        desc_box = s9.shapes[d_idx]

        # 1. Expand Card Height so it encloses text comfortably
        card.top = Inches(1.32)
        card.height = Inches(1.68) # expanded from 1.48" to 1.68" (bottom = 3.00")

        # 2. Adjust circle and number
        oval.top = Inches(1.42)
        num_box.top = Inches(1.44)

        # 3. Adjust Title
        title_box.top = Inches(1.88)
        title_box.height = Inches(0.36)
        set_clean_text(title_box, title_txt, font_name="Calibri", font_size=11.5, bold=True)

        # 4. Adjust Description text box & font size & padding
        desc_box.top = Inches(2.26)
        desc_box.height = Inches(0.68)
        desc_tf = desc_box.text_frame
        desc_tf.word_wrap = True
        desc_tf.margin_top = Pt(1)
        desc_tf.margin_bottom = Pt(1)
        desc_tf.margin_left = Pt(2)
        desc_tf.margin_right = Pt(2)
        
        # Clear extra paragraphs
        if len(desc_tf.paragraphs) > 1:
            for p_extra in desc_tf.paragraphs[1:]:
                p_extra.text = ""
        p = desc_tf.paragraphs[0]
        p.text = desc_txt
        if p.runs:
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(9.0) # reduced from 10.5pt to 9.0pt for crisp fit
            for r_extra in p.runs[1:]:
                r_extra.text = ""

    # Section header: Core Multi-Agent System Layers
    s9.shapes[51].top = Inches(3.20)
    s9.shapes[51].height = Inches(0.35)

    # 5 Bottom Layers: Adjust positions & padding
    layer_data = [
        (52, 53, 54, "Ingestion Layer", "PyPDF & text cleaning"),
        (55, 56, 57, "Indexing Layer", "ChromaDB + TF-IDF fallback"),
        (58, 59, 60, "Agentic Layer", "Autonomous specialized agents"),
        (61, 62, 63, "Generation Layer", "Grounded LLM (Ollama / Fallback)"),
        (64, 65, 66, "Attribution Layer", "Exact page & chunk citations")
    ]
    for (box_idx, title_idx, sub_idx, t_txt, s_txt) in layer_data:
        box = s9.shapes[box_idx]
        t_box = s9.shapes[title_idx]
        s_box = s9.shapes[sub_idx]
        
        box.top = Inches(3.68)
        box.height = Inches(1.10)
        
        t_box.top = Inches(3.80)
        t_box.height = Inches(0.30)
        set_clean_text(t_box, t_txt, font_name="Calibri", font_size=12.5, bold=True)
        
        s_box.top = Inches(4.18)
        s_box.height = Inches(0.48)
        set_clean_text(s_box, s_txt, font_name="Calibri", font_size=9.5, bold=False)

    # Multi-Agent Execution Pipeline summary box
    s9.shapes[67].top = Inches(5.15)
    s9.shapes[67].height = Inches(0.80)
    set_clean_text(s9.shapes[67], "Multi-Agent Execution Pipeline: User query -> Orchestrator classifies intent -> Retrieval Agent fetches semantic chunks with page provenance -> Analysis / Q&A Agent synthesizes grounded response -> Activity Logger records multi-agent execution.", font_name="Calibri", font_size=13.5, bold=False)

    # =========================================================================
    # SLIDE 10: Data / Database Description (FIX SUBTITLE/TABLE COLLISION COMPLETELY)
    # =========================================================================
    s10 = prs.slides[9]
    # Reduce title placeholder height
    s10.shapes[0].height = Inches(0.85)

    # Shape 5: Subtitle
    sub_s10 = s10.shapes[5]
    sub_s10.top = Inches(1.42) # positioned safely above table
    sub_s10.left = Inches(0.65)
    sub_s10.width = Inches(11.80)
    sub_s10.height = Inches(0.42)
    set_clean_text(sub_s10, "Academic research papers processed into persistent vector indices and lexical stores with metadata for grounded attribution.", font_name="Calibri", font_size=12.5, bold=False)

    # Shape 4: Table 73
    table_shp_s10 = s10.shapes[4]
    table_shp_s10.top = Inches(2.15) # moved down to 2.15" giving 0.31" clear gap
    table_shp_s10.left = Inches(0.65)
    table_shp_s10.width = Inches(11.80)
    table_shp_s10.height = Inches(4.25)
    
    table_s10 = table_shp_s10.table
    # Rebalance column widths: total 11.80"
    table_s10.columns[0].width = Inches(2.10)
    table_s10.columns[1].width = Inches(2.40)
    table_s10.columns[2].width = Inches(3.40)
    table_s10.columns[3].width = Inches(3.90)

    s10_table_data = [
        ["System Component", "Configuration / Scope", "Schema / Attributes", "Functional Role"],
        ["PDF Ingestion Corpus", "1+ benchmark papers\n(e.g., LoRA 26-page PDF)", "Raw text, page numbers, title, total pages", "Source research papers for document decomposition"],
        ["Chunking Store", "900-character chunks with 150-char overlap", "chunk_id, page_number, text, char_length", "Granular semantic units preserving page-level attribution"],
        ["ChromaDB Vector Store", "Collection: research_papers\n(all-MiniLM-L6-v2)", "chunk_id, vector_embedding, metadata, document", "High-dimensional semantic similarity vector search"],
        ["TF-IDF Lexical Index", "In-memory sparse term-frequency matrix", "Vocabulary terms, document frequencies, scores", "Resilient keyword search fallback when vector store is unavailable"],
        ["Agent Execution State", "Real-time session state & execution log", "timestamp, agent_name, action, detail, status", "Live execution transparency and multi-agent coordination audit"]
    ]
    for r_idx, row in enumerate(s10_table_data):
        for c_idx, val in enumerate(row):
            cell = table_s10.cell(r_idx, c_idx)
            cell.margin_top = Pt(4)
            cell.margin_bottom = Pt(4)
            cell.margin_left = Pt(6)
            cell.margin_right = Pt(6)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.name = "Calibri"
            r.font.size = Pt(11 if r_idx == 0 else 9.5)
            r.font.bold = (r_idx == 0)

    # =========================================================================
    # SLIDE 11: Experimental Results & Discussion (Refine padding & fonts)
    # =========================================================================
    s11 = prs.slides[10]
    s11.shapes[0].height = Inches(0.85)
    # Subtitle
    set_clean_text(s11.shapes[4], "Midterm Status: Full multi-agent pipeline implemented, verified across 10 validation checks with 100% test pass rate, and deployed on interactive web UI.", font_name="Calibri", font_size=15.0, bold=False)

    # 6 Cards descriptions font size to 9.5pt with zero padding
    for d_idx in [8, 12, 16, 20, 24, 28]:
        shp = s11.shapes[d_idx]
        shp.text_frame.margin_top = Pt(1)
        shp.text_frame.margin_bottom = Pt(1)
        if shp.text_frame.paragraphs and shp.text_frame.paragraphs[0].runs:
            shp.text_frame.paragraphs[0].runs[0].font.size = Pt(9.5)

    # =========================================================================
    # SLIDE 13: Plan of Action (Eliminate horizontal overlap between Title and Desc)
    # =========================================================================
    s13 = prs.slides[12]
    s13.shapes[1].height = Inches(0.85)

    phase_boxes = [
        (6, 7, 8, "Phase 1", "Multi-Paper Corpus Scaling", "Enable simultaneous indexing and cross-referencing across 20+ papers in shared workspace."),
        (10, 11, 12, "Phase 2", "Live Academic API Ingestion", "Integrate ArXiv, Semantic Scholar, and OpenAlex APIs for real-time paper retrieval."),
        (14, 15, 16, "Phase 3", "Automated Literature Review Writer", "Generate multi-section survey drafts complete with BibTeX and APA citations."),
        (18, 19, 20, "Phase 4", "Comparative Matrix Engine", "Synthesize structured comparison tables of datasets, architectures, and empirical findings."),
        (22, 23, 24, "Phase 5", "Advanced Agent Reasoning", "Implement critique/reflection agents with domain-fine-tuned embeddings (SciBERT)."),
        (26, 27, 28, "Phase 6", "Comprehensive Evaluation & Demo", "Conduct quantitative latency/accuracy benchmarks, user study, and final thesis defense.")
    ]

    for (p_idx, t_idx, d_idx, p_txt, t_txt, d_txt) in phase_boxes:
        p_box = s13.shapes[p_idx]
        t_box = s13.shapes[t_idx]
        d_box = s13.shapes[d_idx]

        # Phase badge: left=0.82", w=1.40"
        p_box.left = Inches(0.82)
        p_box.width = Inches(1.40)
        
        # Phase Title: left=2.45", w=2.65" (ends at 5.10")
        t_box.left = Inches(2.45)
        t_box.width = Inches(2.65)
        set_clean_text(t_box, t_txt, font_name="Calibri", font_size=13.5, bold=True)
        
        # Phase Desc: left=5.25", w=6.85" (starts at 5.25", 0.15" clear gap)
        d_box.left = Inches(5.25)
        d_box.width = Inches(6.85)
        set_clean_text(d_box, d_txt, font_name="Calibri", font_size=11.5, bold=False)

    # Save presentation
    updated_path = 'Multi Agent AI Research PPr MID_Updated.pptx'
    prs.save(updated_path)
    print(f"Saved cleanly to {updated_path}")

    # Try saving to original path as well
    import shutil
    try:
        prs.save(pptx_path)
        print(f"Also saved directly to {pptx_path}")
    except PermissionError:
        print(f"Note: {pptx_path} is currently locked (open in PowerPoint).")
        print(f"Saved full clean version to {updated_path}!")

if __name__ == '__main__':
    fix_all_presentation_issues()
