import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './store/AuthContext';
import { Sidebar } from './components/Layout/Sidebar';
import { Header } from './components/Layout/Header';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Portfolios } from './pages/Portfolios';
import { PortfolioDashboard } from './components/Portfolio/PortfolioDashboard';
import { PortfolioList } from './components/Portfolio/PortfolioList';
import { ProjectDetail } from './components/Project/ProjectDetail';
import './App.css';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header />
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

const AppContent: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={
        isAuthenticated ? <Navigate to="/" replace /> : <Login />
      } />
      
      <Route path="/" element={
        <ProtectedRoute>
          <Layout>
            <Dashboard />
          </Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/portfolios" element={
        <ProtectedRoute>
          <Layout>
            <Portfolios />
          </Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/projects" element={
        <ProtectedRoute>
          <Layout>
            <div className="p-6">
              <h1 className="text-2xl font-semibold text-gray-900">Projects</h1>
              <p className="mt-2 text-gray-600">Projects management will be implemented in Phase 2.</p>
            </div>
          </Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/users" element={
        <ProtectedRoute>
          <Layout>
            <div className="p-6">
              <h1 className="text-2xl font-semibold text-gray-900">Users</h1>
              <p className="mt-2 text-gray-600">User management will be implemented in Phase 2.</p>
            </div>
          </Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/reports" element={
        <ProtectedRoute>
          <Layout>
            <div className="p-6">
              <h1 className="text-2xl font-semibold text-gray-900">Reports</h1>
              <p className="mt-2 text-gray-600">Reporting features will be implemented in Phase 4.</p>
            </div>
          </Layout>
        </ProtectedRoute>
      } />
      
      <Route path="/admin" element={
        <ProtectedRoute>
          <Layout>
            <div className="p-6">
              <h1 className="text-2xl font-semibold text-gray-900">Administration</h1>
              <p className="mt-2 text-gray-600">Admin features will be implemented in Phase 2.</p>
            </div>
          </Layout>
        </ProtectedRoute>
      } />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
};

export default App;