# Mental Health Journal Analysis Dashboard
## Project Overview
A web application deployed on Replit that analyzes personal journal entries to provide insights similar to Spotify Wrapped, offering various analytical perspectives on writing patterns, emotional trends, and topic evolution.

## Core Objectives
- Process and analyze journal entries from PDF files
- Generate comprehensive insights through AI/ML analysis
- Present analysis through an interactive, single-page dashboard
- Support analysis of multiple years of journal data (up to 500K words)
- Provide secure cloud-based processing with privacy considerations

## Technical Architecture Decisions

### Frontend: NextJS
- **Decision**: Implement as a NextJS web application
- **Rationale**: Provides excellent developer experience, server-side rendering capabilities, and robust routing

### Backend: Python + FastAPI
- **Decision**: Python backend with FastAPI deployed on Replit
- **Rationale**: FastAPI offers high performance, automatic API documentation, and seamless integration with async Python

### Data Storage & Retrieval: Hybrid Search System
- **Decision**: Implement hybrid search combining BM25 and vector search
- **Components**:
  - PostgreSQL with pgvector for vector storage
  - BM25 for keyword-based retrieval
  - LangChain for orchestrating the retrieval system
- **Rationale**: 
  - BM25 provides excellent keyword matching
  - Vector search captures semantic meaning
  - Hybrid approach improves accuracy of journal analysis
  - LangChain simplifies integration of multiple search approaches

### RAG Implementation with Hybrid Search
- **Storage**: 
  - PostgreSQL with pgvector for embeddings
  - BM25 index for keyword search
- **Retrieval**: 
  - EnsembleRetriever combining BM25 and vector search
  - Weighted combination (40% BM25, 60% vector search)
- **Generation**: 
  - GPT-4 for context-aware insight generation
  - Enhanced context selection using hybrid search
- **Use Cases**:
  - More accurate theme identification
  - Better pattern recognition
  - Improved contextual summaries
  - Enhanced emotional analysis

## Data Flow
1. **Input Processing**
   - PDF text extraction(PDFPlumber)
   - Date parsing and entry segmentation
   - Text cleaning and normalization

2. **Search Index Creation**
   - BM25 index creation using LangChain's BM25Retriever
   - Vector embedding generation using OpenAI API
   - Storage in PostgreSQL with pgvector

3. **Analysis Pipeline**
   - Hybrid search setup:
     - BM25Retriever for keyword matching
     - Vector retrieval for semantic search
     - EnsembleRetriever for combining results
   - Emotional analysis using OpenAI API
   - Topic extraction using hybrid search results
   - Statistical analysis computation

4. **Storage Layer**
   - Journal entries in PostgreSQL (JSON format)
   - Vector embeddings in PostgreSQL (pgvector)
   - BM25 index maintained by LangChain
   - Pre-computed analysis results in PostgreSQL

## Implementation Phases

### Phase 1 (Core Features)
1. **Core Statistics**
   - Word count analytics (Pandas DataFrame aggregation methods)
   - Writing pattern analysis (NumPy array operations + Pandas time series analysis)
   - Entry length statistics (Pandas statistical functions)
   - Writing streak tracking (Pandas DateTimeIndex + rolling window operations)
   - Time coverage analysis (Pandas date_range and resampling methods)
   - Matplotlib visualizations for trends (Matplotlib with Seaborn styling)
   - Hybrid search infrastructure (LangChain's EnsembleRetriever)
   - BM25 and vector search indexes (LangChain's BM25Retriever + PostgreSQL pgvector)

2. **Emotional & Sentiment Analysis**
   - Sentiment timeline generation (OpenAI API (GPT-4) + Pandas time series)
   - Mood pattern detection (OpenAI API for classification + NumPy pattern recognition)
   - Emotional word cloud creation (WordCloud library + Matplotlib)
   - Visual mood representation (Matplotlib color gradients + custom colormaps)
   - Sentiment shift analysis (Pandas rolling statistics + OpenAI API)

3. **Topic Analysis**
   - Theme extraction (RAG with LangChain's hybrid retrieval system)
   - Key people identification (OpenAI API Named Entity Recognition (NER))
   - Location analysis (OpenAI API NER + Pandas groupby operations)
   - Pattern recognition (NumPy + scikit-learn clustering)
   - Topic evolution tracking (OpenAI embeddings + Pandas time series analysis)
   - Topic visualization (Matplotlib network graphs + Seaborn)

### Phase 2 (Visual & Comparative Features)
1. **Comparative Analysis**
   - Year-over-year comparisons (Pandas resample + groupby operations)
   - Seasonal pattern analysis (Pandas seasonal_decompose + NumPy FFT)
   - Topic evolution tracking (OpenAI embeddings + T-SNE visualization)
   - Writing maturity assessment (OpenAI API text analysis + Pandas scoring)
   - Trend visualizations (Matplotlib with custom styling + Seaborn)

2. **Custom Visual Reports**
   - Emotional color wheel (D3.js circular visualization + custom color mapping)
   - Topic galaxy visualization (Three.js 3D clustering + force-directed layout)
   - Interactive journey map (D3.js timeline + interactive tooltips)
   - Word universe display (Three.js particle system + WebGL rendering)
   - Growth spiral representation (D3.js spiral layout + custom animation)

3. **Summary Features**
   - RAG-powered year in essence (LangChain hybrid search + GPT-4 summarization)
   - Key moments timeline (D3.js timeline + Pandas event detection)
   - Core themes identification (OpenAI API clustering + LangChain retrieval)
   - Achievement highlighting (OpenAI API sentiment analysis + NER)
   - Growth area identification (OpenAI API pattern analysis + Pandas trending)

### Phase 3 (Advanced Analysis)
1. **Writing Style Insights**
   - Writing complexity scoring (textstat)
   - Vocabulary growth tracking (OpenAI API)
   - Writing style evolution analysis (OpenAI API)
   - Writer personality classification (OpenAI API)
   - Writing pattern detection (OpenAI API)
   - Style visualization generation (Matplotlib)
   - Statistical trend computation (Pandas)
   - Word choice evolution tracking (OpenAI embeddings)

2. **Personal Growth Metrics**
   - Goal extraction and tracking (RAG with hybrid search)
   - Problem-solution pattern identification (LangChain)
   - Growth indicator detection (OpenAI API)
   - Achievement timeline visualization (D3.js)
   - Challenge pattern clustering (scikit-learn)
   - Progress tracking analysis (hybrid search)
   - Achievement detection and scoring (OpenAI NER)
   - Temporal pattern analysis (Pandas)

3. **Memory Time Capsule**
   - Key event extraction (hybrid search: BM25 + vector)
   - First mention detection (Pandas chronological analysis)
   - Impact scoring computation (OpenAI API)
   - Seasonal pattern clustering (scikit-learn)
   - Interactive timeline rendering (D3.js)
   - Memory space visualization (Three.js)
   - Topic importance calculation (RAG)
   - Temporal heat map generation (Matplotlib)

4. **AI-Generated Insights**
   - Writing style analysis (OpenAI API)
   - Theme extraction and analysis (RAG with hybrid search)
   - Personal narrative generation (GPT-4)
   - Growth trajectory computation (Pandas)
   - Insight visualization rendering (D3.js)
   - Topic correlation analysis (NumPy)
   - Personal development mapping (T-SNE)

## Technical Components

### ML/AI Components
- LangChain for:
  - BM25 retrieval
  - Hybrid search implementation
  - RAG orchestration
- OpenAI API for:
  - Text embeddings
  - RAG implementation
  - Sentiment analysis
  - Topic modeling
  - NER
- NumPy/Pandas for statistical analysis
- Matplotlib for visualization generation
- T-SNE for dimensionality reduction

### Data Visualization
- Matplotlib for static visualizations
- D3.js for interactive visualizations
- Chart.js for statistical charts
- Three.js for 3D topic visualizations

### Core Libraries
```text
Frontend:
- NextJS/React
- D3.js/Chart.js/Three.js
- TailwindCSS

Backend:
- Python 3.9+
- FastAPI
- LangChain
- Pandas/NumPy
- Matplotlib
- OpenAI API (gpt-4o-mini-2024-07-18, text-embedding-3-small at 1536 dimensions)
- PostgreSQL with pgvector using Replit's PostgreSQL database
- SQLAlchemy with Psycopg2
```

## Security Considerations
- Secure API key management in Replit
- Database encryption
- User data isolation
- Regular backups
- HTTPS enforcement

## Development Workflow
1. Setup Replit development environment
2. Configure PostgreSQL with pgvector
3. Implement PDF processing pipeline
4. Setup LangChain with hybrid search
5. Develop core analysis features
6. Create visualization components
7. Integrate RAG system
8. Testing and optimization

## Next Steps
1. Set up Replit environment
2. Create basic NextJS template
3. Configure PostgreSQL and pgvector
4. Setup LangChain and BM25
5. Implement hybrid search system
6. Begin Phase 1 feature development