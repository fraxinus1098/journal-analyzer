# Project Root
.
├── README.md                   # Project documentation and setup instructions
├── .gitignore                 # Git ignore rules
├── .replit                    # Replit configuration
├── replit.nix                 # Nix environment for Replit
├── .env.example               # Environment variables template
├── docker-compose.yml         # PostgreSQL and service configuration
├── setup/                     # Setup and initialization scripts
│   ├── init-db.sql           # PostgreSQL initialization script
│   ├── setup-replit.sh       # Replit environment setup script
│   └── install-deps.sh       # Project dependencies installation
│
├── frontend/                  # NextJS Frontend application
│   ├── package.json          # Frontend dependencies and scripts
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   ├── next.config.js        # Next.js configuration
│   ├── public/               # Static assets and files
│   └── src/                  # Frontend source code
│       ├── app/              # Next.js 13+ App Router
│       │   ├── layout.tsx    # Root layout component
│       │   └── page.tsx      # Homepage component
│       ├── features/         # Feature-based code organization
│       │   ├── core-stats/   # Core statistics visualization
│       │   │   ├── components/
│       │   │   │   ├── CoreStats.tsx      # Main stats display
│       │   │   │   └── StatCard.tsx       # Individual stat component
│       │   │   ├── hooks/                 # Feature-specific hooks
│       │   │   └── types/                 # Type definitions
│       │   ├── emotional-analysis/        # Emotional trend analysis
│       │   │   ├── components/
│       │   │   │   ├── EmotionalAnalysis.tsx    # Main emotion analysis
│       │   │   │   ├── EmotionalTimeline.tsx    # Emotion trends over time
│       │   │   │   └── MoodPatterns.tsx         # Mood pattern visualization
│       │   │   ├── hooks/
│       │   │   └── types/
│       │   ├── topic-analysis/            # Topic clustering and analysis
│       │   │   ├── components/
│       │   │   │   ├── TopicAnalysis.tsx  # Topic analysis dashboard
│       │   │   │   └── TopicGalaxy.tsx    # 3D topic visualization
│       │   │   ├── hooks/
│       │   │   └── types/
│       │   ├── comparative-analysis/      # Year-over-year comparisons
│       │   │   ├── components/
│       │   │   │   ├── YearComparison.tsx     # Yearly comparison view
│       │   │   │   └── SeasonalPatterns.tsx   # Seasonal analysis
│       │   │   ├── hooks/
│       │   │   └── types/
│       │   ├── writing-style/             # Writing style analytics
│       │   │   ├── components/
│       │   │   │   ├── ComplexityGraph.tsx    # Writing complexity metrics
│       │   │   │   └── VocabularyGrowth.tsx   # Vocabulary analysis
│       │   │   ├── hooks/
│       │   │   └── types/
│       │   ├── personal-growth/           # Personal development tracking
│       │   │   ├── components/
│       │   │   │   ├── GoalTracker.tsx        # Goal progress tracking
│       │   │   │   └── ChallengePatterns.tsx  # Challenge analysis
│       │   │   ├── hooks/
│       │   │   └── types/
│       │   └── memory-capsule/            # Memory visualization
│       │       ├── components/
│       │       │   ├── TimeCapsule.tsx        # Memory collection view
│       │       │   └── MemoryTimeline.tsx     # Timeline visualization
│       │       ├── hooks/
│       │       └── types/
│       ├── components/       # Shared UI components
│       ├── hooks/           # Shared React hooks
│       ├── utils/           # Shared utility functions
│       └── types/           # Shared TypeScript types
│
└── backend/                  # Python/FastAPI Backend
    ├── requirements.txt      # Python package dependencies
    ├── main.py              # FastAPI application entry point
    ├── config/              # Configuration management
    │   ├── __init__.py
    │   └── settings.py      # Application settings
    ├── app/                 # Main application package
    │   ├── __init__.py
    │   ├── api/            # API endpoints and routing
    │   │   ├── __init__.py
    │   │   └── v1/         # API version 1
    │   │       ├── endpoints/  # API route handlers
    │   │       └── api.py     # API router configuration
    │   ├── core/           # Core application functionality
    │   │   ├── __init__.py
    │   │   └── config.py   # Core configuration
    │   ├── db/             # Database operations
    │   │   ├── __init__.py
    │   │   ├── init_db.py  # Database initialization
    │   │   ├── crud.py     # CRUD operations
    │   │   └── postgres.py # PostgreSQL connection
    │   ├── models/         # Data models
    │   │   ├── __init__.py
    │   │   └── journal.py  # Journal entry models
    │   ├── services/       # Business logic services
    │   │   ├── __init__.py
    │   │   ├── analysis_service.py       # Text analysis
    │   │   ├── comparative_service.py    # Comparative analytics
    │   │   ├── growth_service.py         # Growth tracking
    │   │   ├── hybrid_search_service.py  # Combined search
    │   │   ├── journal_service.py        # Journal management
    │   │   ├── openai_service.py         # OpenAI integration
    │   │   ├── retrieval_service.py      # Document retrieval
    │   │   ├── visualization_service.py  # Data visualization
    │   │   └── writing_analysis_service.py # Writing analysis
    │   └── utils/          # Utility functions
    │       ├── __init__.py
    │       ├── indexing.py               # Document indexing
    │       ├── ranking.py                # Search result ranking
    │       ├── text_processing.py        # Text preprocessing
    │       └── vector_utils.py           # Vector operations
    └── tests/              # Test suite
        ├── __init__.py
        └── test_services/  # Service unit tests