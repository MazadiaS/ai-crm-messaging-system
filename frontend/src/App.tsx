import { BrowserRouter as Router } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuthStore } from './stores/authStore'

function App() {
  const { token, fetchUser } = useAuthStore()

  useEffect(() => {
    if (token) {
      fetchUser()
    }
  }, [token, fetchUser])

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              AI CRM Messaging System
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Production-ready full-stack application with Claude AI
            </p>
            <div className="space-y-4">
              <div className="p-6 bg-white rounded-lg shadow-md">
                <h2 className="text-2xl font-semibold mb-4">Backend is Ready!</h2>
                <div className="space-y-2 text-left">
                  <p className="text-green-600">✓ FastAPI with async support</p>
                  <p className="text-green-600">✓ PostgreSQL database with SQLAlchemy</p>
                  <p className="text-green-600">✓ JWT authentication</p>
                  <p className="text-green-600">✓ Claude AI integration</p>
                  <p className="text-green-600">✓ Complete REST API</p>
                  <p className="text-green-600">✓ Database models and schemas</p>
                  <p className="text-green-600">✓ Analytics endpoints</p>
                </div>
              </div>

              <div className="p-6 bg-white rounded-lg shadow-md">
                <h2 className="text-2xl font-semibold mb-4">Frontend Foundation</h2>
                <div className="space-y-2 text-left">
                  <p className="text-green-600">✓ React 18 + TypeScript</p>
                  <p className="text-green-600">✓ Vite build setup</p>
                  <p className="text-green-600">✓ TailwindCSS configured</p>
                  <p className="text-green-600">✓ API client ready</p>
                  <p className="text-green-600">✓ Auth store with Zustand</p>
                  <p className="text-green-600">✓ Type definitions complete</p>
                  <p className="text-yellow-600">⊙ UI components (in progress)</p>
                </div>
              </div>

              <div className="p-6 bg-white rounded-lg shadow-md">
                <h2 className="text-2xl font-semibold mb-4">Infrastructure</h2>
                <div className="space-y-2 text-left">
                  <p className="text-green-600">✓ Docker Compose configuration</p>
                  <p className="text-green-600">✓ PostgreSQL + Redis containers</p>
                  <p className="text-green-600">✓ Comprehensive documentation</p>
                  <p className="text-green-600">✓ Deployment guides</p>
                  <p className="text-green-600">✓ Seed data script</p>
                </div>
              </div>

              <div className="mt-8 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold mb-2">Quick Start:</h3>
                <ol className="text-left text-sm space-y-1">
                  <li>1. Set ANTHROPIC_API_KEY in backend/.env</li>
                  <li>2. Run: <code className="bg-gray-200 px-2 py-1 rounded">docker-compose up -d</code></li>
                  <li>3. Seed data: <code className="bg-gray-200 px-2 py-1 rounded">docker-compose exec backend python seed_data.py</code></li>
                  <li>4. API docs: <a href="http://localhost:8000/api/docs" className="text-blue-600 underline">http://localhost:8000/api/docs</a></li>
                </ol>
              </div>

              <div className="mt-8 text-gray-500 text-sm">
                <p>Built for CROWE interview demonstration</p>
                <p className="mt-2">
                  <a href="https://github.com/yourusername/ai-crm-messaging-system" className="text-blue-600 hover:underline">
                    View on GitHub
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Router>
  )
}

export default App
