import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { LoginCredentials } from '../types/auth';

// Demo user accounts for easy testing
const DEMO_USERS = [
  {
    name: 'John Admin',
    role: 'Admin (TechCorp)',
    credentials: { username: 'admin_techcorp', password: 'Demo123!', tenant_code: 'techcorp' },
    color: 'bg-red-500 hover:bg-red-600'
  },
  {
    name: 'Sarah Johnson', 
    role: 'Portfolio Manager (TechCorp)',
    credentials: { username: 'pm_sarah', password: 'Demo123!', tenant_code: 'techcorp' },
    color: 'bg-blue-500 hover:bg-blue-600'
  },
  {
    name: 'Mike Davis',
    role: 'Project Manager (TechCorp)', 
    credentials: { username: 'mgr_mike', password: 'Demo123!', tenant_code: 'techcorp' },
    color: 'bg-green-500 hover:bg-green-600'
  },
  {
    name: 'Jane Founder',
    role: 'Admin (StartupXYZ)',
    credentials: { username: 'admin_startup', password: 'Demo123!', tenant_code: 'startupxyz' },
    color: 'bg-purple-500 hover:bg-purple-600'
  },
  {
    name: 'Alex Thompson',
    role: 'PMO Admin (StartupXYZ)',
    credentials: { username: 'cto_alex', password: 'Demo123!', tenant_code: 'startupxyz' },
    color: 'bg-indigo-500 hover:bg-indigo-600'
  },
  {
    name: 'Lisa Chang',
    role: 'PMO Admin (Enterprise)',
    credentials: { username: 'pmo_lisa', password: 'Demo123!', tenant_code: 'enterprise' },
    color: 'bg-orange-500 hover:bg-orange-600'
  }
];

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login, loading, error } = useAuth();
  const [formData, setFormData] = useState<LoginCredentials>({
    username: '',
    password: '',
    tenant_code: '',
  });
  const [showDemoUsers, setShowDemoUsers] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(formData);
      navigate('/');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleDemoLogin = async (credentials: LoginCredentials) => {
    try {
      await login(credentials);
      navigate('/');
    } catch (error) {
      console.error('Demo login failed:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="flex justify-center">
            <div className="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-2xl">A</span>
            </div>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to AtlasPM
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Enter your credentials to access your portfolio management platform
          </p>
        </div>

        {/* Demo Users Section */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-blue-900">
              🎯 Try Demo Accounts
            </h3>
            <button
              onClick={() => setShowDemoUsers(!showDemoUsers)}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
              data-testid="toggle-demo-users-btn"
            >
              {showDemoUsers ? 'Hide' : 'Show'} Demo Users
            </button>
          </div>
          
          {showDemoUsers && (
            <div className="mt-4 space-y-2">
              <p className="text-xs text-blue-700 mb-3">
                Click any button below for instant access with different user roles:
              </p>
              <div className="grid grid-cols-1 gap-2">
                {DEMO_USERS.map((user, index) => (
                  <button
                    key={index}
                    onClick={() => handleDemoLogin(user.credentials)}
                    disabled={loading}
                    className={`${user.color} text-white px-3 py-2 rounded text-sm font-medium transition-colors disabled:opacity-50 text-left`}
                    data-testid={`demo-user-${user.credentials.username}`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">{user.name}</span>
                      <span className="text-xs opacity-90">{user.role}</span>
                    </div>
                  </button>
                ))}
              </div>
              <p className="text-xs text-blue-600 mt-2">
                All demo accounts use password: <code className="bg-blue-100 px-1 rounded">Demo123!</code>
              </p>
            </div>
          )}
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">{error}</div>
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label htmlFor="tenant_code" className="block text-sm font-medium text-gray-700">
                Organization Code
              </label>
              <input
                id="tenant_code"
                name="tenant_code"
                type="text"
                required
                value={formData.tenant_code}
                onChange={handleChange}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="Enter your organization code"
                data-testid="tenant-code-input"
              />
            </div>
            
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="Enter your username"
                data-testid="username-input"
              />
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="Enter your password"
                data-testid="password-input"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              data-testid="login-submit-btn"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>

          <div className="text-center">
            <Link
              to="/register"
              className="text-sm text-primary-600 hover:text-primary-500"
            >
              Need to register your organization? Get started here
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};