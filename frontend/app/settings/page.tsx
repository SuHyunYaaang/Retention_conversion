'use client';

import React, { useState, useEffect } from 'react';
import Header from '../../components/Header';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Input from '../../components/ui/Input';
import { 
  Database, 
  Server, 
  Settings, 
  Save, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle,
  Eye,
  EyeOff,
  Shield,
  Activity
} from 'lucide-react';

interface SystemStatus {
  database: 'connected' | 'disconnected' | 'error';
  backend: 'running' | 'stopped' | 'error';
  postgrest: 'running' | 'stopped' | 'error';
  frontend: 'running' | 'stopped' | 'error';
}

interface DatabaseConfig {
  host: string;
  port: string;
  database: string;
  username: string;
  password: string;
}

interface ApiConfig {
  backendUrl: string;
  postgrestUrl: string;
  timeout: string;
}

const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('database');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    database: 'disconnected',
    backend: 'stopped',
    postgrest: 'stopped',
    frontend: 'running'
  });

  const [databaseConfig, setDatabaseConfig] = useState<DatabaseConfig>({
    host: 'localhost',
    port: '2',
    database: 'retention_db',
    username: 'retention_user',
    password: 'retention_password'
  });

  const [apiConfig, setApiConfig] = useState<ApiConfig>({
    backendUrl: 'http://localhost:8000',
    postgrestUrl: 'http://localhost:3001',
    timeout: '30'
  });

  // 시스템 상태 체크
  const checkSystemStatus = async () => {
    setIsLoading(true);
    try {
      // 실제로는 각 서비스에 ping을 보내서 상태를 확인
      // 여기서는 시뮬레이션
      setTimeout(() => {
        setSystemStatus({
          database: 'connected',
          backend: 'running',
          postgrest: 'running',
          frontend: 'running'
        });
        setIsLoading(false);
      }, 2000);
    } catch (error) {
      console.error('시스템 상태 확인 실패:', error);
      setIsLoading(false);
    }
  };

  // 설정 저장
  const saveSettings = async () => {
    setIsLoading(true);
    try {
      // 실제로는 API를 통해 설정을 저장
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('설정이 저장되었습니다.');
    } catch (error) {
      alert('설정 저장에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  // 데이터베이스 연결 테스트
  const testDatabaseConnection = async () => {
    setIsLoading(true);
    try {
      // 실제로는 데이터베이스 연결을 테스트
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('데이터베이스 연결이 성공했습니다.');
    } catch (error) {
      alert('데이터베이스 연결에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkSystemStatus();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
      case 'running':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'disconnected':
      case 'stopped':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Activity className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'connected':
      case 'running':
        return '정상';
      case 'disconnected':
      case 'stopped':
        return '중지됨';
      case 'error':
        return '오류';
      default:
        return '알 수 없음';
    }
  };

  const tabs = [
    { id: 'database', name: '데이터베이스', icon: Database },
    { id: 'api', name: 'API 설정', icon: Server },
    { id: 'system', name: '시스템 상태', icon: Activity },
    { id: 'security', name: '보안', icon: Shield },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-white">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">관리자 설정</h1>
          <p className="text-slate-600">시스템 설정 및 상태를 관리합니다.</p>
        </div>

        {/* 탭 네비게이션 */}
        <div className="mb-8">
          <nav className="flex space-x-8 border-b border-slate-200">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-accent-500 text-accent-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* 탭 컨텐츠 */}
        <div className="space-y-6">
          {/* 데이터베이스 설정 */}
          {activeTab === 'database' && (
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-slate-900">데이터베이스 설정</h2>
                <Button
                  onClick={testDatabaseConnection}
                  disabled={isLoading}
                  className="flex items-center space-x-2"
                >
                  <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                  <span>연결 테스트</span>
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    호스트
                  </label>
                  <Input
                    type="text"
                    value={databaseConfig.host}
                    onChange={(e) => setDatabaseConfig({
                      ...databaseConfig,
                      host: e.target.value
                    })}
                    placeholder="localhost"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    포트
                  </label>
                  <Input
                    type="text"
                    value={databaseConfig.port}
                    onChange={(e) => setDatabaseConfig({
                      ...databaseConfig,
                      port: e.target.value
                    })}
                    placeholder="5432"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    데이터베이스명
                  </label>
                  <Input
                    type="text"
                    value={databaseConfig.database}
                    onChange={(e) => setDatabaseConfig({
                      ...databaseConfig,
                      database: e.target.value
                    })}
                    placeholder="retention_db"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    사용자명
                  </label>
                  <Input
                    type="text"
                    value={databaseConfig.username}
                    onChange={(e) => setDatabaseConfig({
                      ...databaseConfig,
                      username: e.target.value
                    })}
                    placeholder="retention_user"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    비밀번호
                  </label>
                  <div className="relative">
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      value={databaseConfig.password}
                      onChange={(e) => setDatabaseConfig({
                        ...databaseConfig,
                        password: e.target.value
                      })}
                      placeholder="••••••••"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      {showPassword ? (
                        <EyeOff className="w-4 h-4 text-slate-400" />
                      ) : (
                        <Eye className="w-4 h-4 text-slate-400" />
                      )}
                    </button>
                  </div>
                </div>
              </div>
            </Card>
          )}

          {/* API 설정 */}
          {activeTab === 'api' && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold text-slate-900 mb-6">API 설정</h2>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    백엔드 API URL
                  </label>
                  <Input
                    type="url"
                    value={apiConfig.backendUrl}
                    onChange={(e) => setApiConfig({
                      ...apiConfig,
                      backendUrl: e.target.value
                    })}
                    placeholder="http://localhost:8000"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    PostgREST API URL
                  </label>
                  <Input
                    type="url"
                    value={apiConfig.postgrestUrl}
                    onChange={(e) => setApiConfig({
                      ...apiConfig,
                      postgrestUrl: e.target.value
                    })}
                    placeholder="http://localhost:3001"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    요청 타임아웃 (초)
                  </label>
                  <Input
                    type="number"
                    value={apiConfig.timeout}
                    onChange={(e) => setApiConfig({
                      ...apiConfig,
                      timeout: e.target.value
                    })}
                    placeholder="30"
                  />
                </div>
              </div>
            </Card>
          )}

          {/* 시스템 상태 */}
          {activeTab === 'system' && (
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-slate-900">시스템 상태</h2>
                <Button
                  onClick={checkSystemStatus}
                  disabled={isLoading}
                  className="flex items-center space-x-2"
                >
                  <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                  <span>새로고침</span>
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.entries(systemStatus).map(([service, status]) => (
                  <div key={service} className="bg-slate-50 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-700 capitalize">
                        {service === 'postgrest' ? 'PostgREST' : 
                         service === 'ml-dashboard' ? 'ML Dashboard' : service}
                      </span>
                      {getStatusIcon(status)}
                    </div>
                    <p className="text-sm text-slate-600">
                      {getStatusText(status)}
                    </p>
                  </div>
                ))}
              </div>

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="text-sm font-medium text-blue-900 mb-2">시스템 정보</h3>
                <div className="text-sm text-blue-800 space-y-1">
                  <p>• PostgreSQL 포트: 5432</p>
                  <p>• 백엔드 API 포트: 8000</p>
                  <p>• PostgREST 포트: 3001</p>
                  <p>• 프론트엔드 포트: 3000</p>
                  <p>• Nginx 프록시 포트: 8090</p>
                </div>
              </div>
            </Card>
          )}

          {/* 보안 설정 */}
          {activeTab === 'security' && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold text-slate-900 mb-6">보안 설정</h2>

              <div className="space-y-6">
                <div className="p-4 bg-yellow-50 rounded-lg">
                  <h3 className="text-sm font-medium text-yellow-900 mb-2">보안 권장사항</h3>
                  <ul className="text-sm text-yellow-800 space-y-1">
                    <li>• 강력한 비밀번호 사용</li>
                    <li>• 정기적인 비밀번호 변경</li>
                    <li>• HTTPS 사용 권장</li>
                    <li>• 방화벽 설정 확인</li>
                    <li>• 로그 모니터링 활성화</li>
                  </ul>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    JWT 시크릿 키
                  </label>
                  <div className="relative">
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      placeholder="JWT 시크릿 키를 입력하세요"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      {showPassword ? (
                        <EyeOff className="w-4 h-4 text-slate-400" />
                      ) : (
                        <Eye className="w-4 h-4 text-slate-400" />
                      )}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    세션 타임아웃 (분)
                  </label>
                  <Input
                    type="number"
                    placeholder="30"
                  />
                </div>
              </div>
            </Card>
          )}
        </div>

        {/* 저장 버튼 */}
        <div className="mt-8 flex justify-end">
          <Button
            onClick={saveSettings}
            disabled={isLoading}
            className="flex items-center space-x-2"
          >
            <Save className="w-4 h-4" />
            <span>설정 저장</span>
          </Button>
        </div>
      </main>
    </div>
  );
};

export default SettingsPage;
