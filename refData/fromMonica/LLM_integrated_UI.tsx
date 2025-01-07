import React, { useState } from 'react';
import { 
  Home,
  Bot,
  History,
  Users,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

const Sidebar = () => {
  const [expandedModel, setExpandedModel] = useState(false);

  return (
    <div className="w-[20%] h-screen bg-slate-800 text-white p-4 flex flex-col">
      {/* Logo 區域 */}
      <div className="mb-8">
        <h1 className="text-xl font-bold">LLM 服務平台</h1>
      </div>

      {/* 主導航區域 */}
      <nav className="flex-1">
        <div className="space-y-2">
          {/* 首頁 */}
          <div className="flex items-center p-2 rounded hover:bg-slate-700 cursor-pointer">
            <Home className="w-5 h-5 mr-2" />
            <span>首頁</span>
          </div>

          {/* 模型選單 */}
          <div>
            <div 
              className="flex items-center justify-between p-2 rounded hover:bg-slate-700 cursor-pointer"
              onClick={() => setExpandedModel(!expandedModel)}
            >
              <div className="flex items-center">
                <Bot className="w-5 h-5 mr-2" />
                <span>模型</span>
              </div>
              {expandedModel ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </div>
            
            {/* 子選單 */}
            {expandedModel && (
              <div className="ml-7 space-y-2 mt-2">
                <div className="p-2 rounded hover:bg-slate-700 cursor-pointer">
                  GPT-4
                </div>
                <div className="p-2 rounded hover:bg-slate-700 cursor-pointer">
                  Claude 3
                </div>
                <div className="p-2 rounded hover:bg-slate-700 cursor-pointer">
                  Gemini
                </div>
              </div>
            )}
          </div>

          {/* 聊天歷史 */}
          <div className="flex items-center p-2 rounded hover:bg-slate-700 cursor-pointer">
            <History className="w-5 h-5 mr-2" />
            <span>聊天歷史</span>
          </div>

          {/* 代理人 */}
          <div className="flex items-center p-2 rounded hover:bg-slate-700 cursor-pointer">
            <Users className="w-5 h-5 mr-2" />
            <span>代理人</span>
          </div>
        </div>
      </nav>

      {/* 用戶資訊區域 */}
      <div className="pt-4 border-t border-slate-600">
        <div className="flex items-center p-2">
          <div className="w-8 h-8 rounded-full bg-slate-600 mr-2"></div>
          <div>
            <div className="text-sm font-medium">用戶名稱</div>
            <div className="text-xs text-slate-400">user@example.com</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const MainContent = () => (
  <div className="flex-1 h-screen bg-white p-6">
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">歡迎使用 LLM 服務平台</h2>
      <p className="text-gray-600">
        請從左側選單選擇所需的功能。這裡是主要工作區域，內容會根據您的選擇而改變。
      </p>
    </div>
  </div>
);

const App = () => (
  <div className="flex">
    <Sidebar />
    <MainContent />
  </div>
);

export default App;