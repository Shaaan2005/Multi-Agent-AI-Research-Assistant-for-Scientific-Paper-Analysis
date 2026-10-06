tikz_code = r"""
\begin{figure*}[t]
\centering
\begin{tikzpicture}[
    >=Stealth,
    font=\sffamily\footnotesize,
    node distance=0.8cm and 1.2cm,
    block/.style={rectangle, draw=#1!75!black, fill=#1!8, thick, rounded corners=3pt, minimum width=2.8cm, minimum height=1.0cm, align=center},
    store/.style={cylinder, draw=purple!75!black, fill=purple!8, thick, shape border rotate=90, minimum width=2.6cm, minimum height=1.1cm, align=center, aspect=0.25},
    subbox/.style={draw=#1!50!black, fill=#1!3, dashed, thick, rounded corners=6pt, inner sep=8pt},
    arr/.style={->, thick, draw=gray!75!black},
    darr/.style={<->, thick, draw=blue!75!black}
]

% TIER 1: Ingestion & Indexing Pipeline (Top)
\node[block=teal] (doc) at (0, 2.2) {\textbf{Document Agent}\\\scriptsize PyPDF Extraction};
\node[block=teal] (chunk) at (4.2, 2.2) {\textbf{Chunking Engine}\\\scriptsize 900-ch / 150 Overlap};
\node[store] (vstore) at (8.6, 2.2) {\textbf{Hybrid Vector Store}\\\scriptsize ChromaDB + TF-IDF};

% TIER 2: Live Multi-Agent Reasoning Pipeline (Bottom)
\node[block=green!60!black] (ui) at (-3.8, 0) {\textbf{Streamlit Web UI}\\\scriptsize User Query \& Logs};
\node[block=blue] (orch) at (0, 0) {\textbf{Research Orchestrator}\\\scriptsize Intent Classification};
\node[block=blue] (ret) at (4.2, 0) {\textbf{Retrieval Agent}\\\scriptsize Top-$k$ Ranking};
\node[block=indigo] (agents) at (8.6, 0) {\textbf{Specialized Agents}\\\scriptsize Summary / Analysis};
\node[block=red!70!black] (ans) at (12.8, 0) {\textbf{Grounded Answer Agent}\\\scriptsize Anti-Hallucination QA};

% Background grouping boxes
\begin{scope}[on background layer]
    \node[subbox=teal, fit=(doc) (chunk) (vstore), label={[teal!70!black, font=\scriptsize\bfseries]above:Document Ingestion \& Hybrid Indexing Subsystem}] {};
    \node[subbox=blue, fit=(orch) (ret) (agents) (ans), label={[blue!70!black, font=\scriptsize\bfseries]below:Multi-Agent Intent Routing \& Grounded Synthesis Core}] {};
\end{scope}

% Tier 1 Horizontal Connections
\draw[arr] (-2.2, 2.2) -- node[above, font=\scriptsize] {Upload PDF} (doc);
\draw[arr] (doc) -- node[above, font=\scriptsize] {Clean Text} (chunk);
\draw[arr] (chunk) -- node[above, font=\scriptsize] {Metadata Chunks} (vstore);

% Tier 2 Horizontal Connections
\draw[arr] (ui) -- node[above, font=\scriptsize] {Query} (orch);
\draw[arr] (orch) -- node[above, font=\scriptsize] {Intent Tag} (ret);
\draw[arr] (ret) -- node[above, font=\scriptsize] {Context Excerpts} (agents);
\draw[arr] (agents) -- node[above, font=\scriptsize] {Structured Synthesis} (ans);

% Inter-Tier Vertical Connection (Data to Retrieval)
\draw[arr, ultra thick, draw=purple!80!black] (vstore.south) -- node[right, font=\scriptsize] {Semantic Chunks} (agents.north -| vstore.south) |- (ret.east);

% Feedback to UI
\draw[arr, thick, draw=green!60!black] (ans.south) -- ++(0,-0.7) -| node[above, font=\scriptsize, pos=0.25] {Citation-Backed Grounded Response: [Page $X$]} (ui.south);

\end{tikzpicture}
\caption{End-to-End Multi-Agent Architecture showing the decoupled execution flow: document parsing and chunk indexing (top), query intent routing and semantic retrieval (center), and grounded synthesis with page citations returned to the interactive UI (right-to-left).}
\label{fig:pipeline}
\end{figure*}
"""

print("TikZ code prepared, length:", len(tikz_code))
