# MediPath AI

**Multi-Doctor AI Second Opinion + Cost-Optimized Diagnosis Engine**

MediPath AI is an advanced backend-heavy medical inference engine that simulates multiple specialist AI agents, aggregates their beliefs, optimizes for diagnostic cost, and ultimately generates a comprehensive final diagnosis.

## Architecture Structure

- **Backend**: Python + FastAPI
- **Frontend**: React + TailwindCSS + Vite
- **LLM/Agents**: Groq API (`llama3-70b-8192`) running asynchronously.

## Startup Instructions

### Backend Route

1. `cd backend`
2. Configure environment with `set GROQ_API_KEY=your_key_here` (or `.env` file)
3. Install dependencies: `pip install -r requirements.txt`
4. Run FastAPI server: `uvicorn main:app --reload`
   Server will be available at `http://localhost:8000`

### Frontend Route

1. `cd frontend`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`
   Vite UI will start at `http://localhost:5173`

## Key Engine Features

1. **Multi-Doctor AI Agents**: General Physician, Pulmonologist, Infectious Specialist running asynchronously and providing distinct structured predictions.
2. **Belief Aggregator**: Combines weighted probabilities from different agents.
3. **Cost Optimization**: Recommends the highest information-gain diagnostic tests while keeping the cost relatively minimal based on test recommendations.
4. **Final Reasoning Engine**: Acts as a Chief Medical Officer, assimilating everything into a final patient briefing and prescribing next steps.
