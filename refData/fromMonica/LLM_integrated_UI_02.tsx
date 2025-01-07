import React, { useState } from 'react';
import { 
  Home,
  Bot,
  History,
  Users,
  MessageSquare,
  FileText,
  Scanner
} from 'lucide-react';

const MainSidebar = ({ onSelectItem, selectedItem }) => (
  <div className="w-[20%] h-screen bg-slate-800 text-white p-4 flex flex-col">
    {/* Logo 區域 */}
    <div className="mb-8">
      <h1 className="text-xl font-bold">LLM 服務平台</h1>
    </div>

    {/* 主導航區域 */}
    <nav className="flex-1">
      <div className="space-y-2">
        {/* 首頁 */}
        <div 
          className={`flex items-center p-2 rounded cursor-pointer ${
            selectedItem === 'home' ? 'bg-slate-600' : 'hover:bg-slate-700'
          }`}
          onClick={() => onSelectItem('home')}
        >
          <Home className="w-5 h-5 mr-2" />
          <span>首頁</span>
        </div>

        {/* 模型 */}
        <div 
          className={`flex items-center p-2 rounded cursor-pointer ${
            selectedItem === 'models' ? 'bg-slate-600' : 'hover:bg-slate-700'
          }`}
          onClick={() => onSelectItem('models')}
        >
          <Bot className="w-5 h-5 mr-2" />
          <span>模型</span>
        </div>

        {/* 聊天歷史 */}
        <div 
          className={`flex items-center p-2 rounded cursor-pointer ${
            selectedItem === 'history' ? 'bg-slate-600' : 'hover:bg-slate-700'
          }`}
          onClick={() => onSelectItem('history')}
        >
          <History className="w-5 h-5 mr-2" />
          <span>聊天歷史</span>
        </div>

        {/* 代理人 */}
        <div 
          className={`flex items-center p-2 rounded cursor-pointer ${
            selectedItem === 'agents' ? 'bg-slate-600' : 'hover:bg-slate-700'
          }`}
          onClick={() => onSelectItem('agents')}
        >
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

const SecondaryAgentSidebar = () => (
  <div className="w-[20%] h-screen bg-slate-700 text-white p-4">
    <h2 className="text-lg font-semibold mb-4">代理人服務</h2>
    <nav className="space-y-2">
      <div className="flex items-center p-2 rounded hover:bg-slate-600 cursor-pointer">
        <MessageSquare className="w-5 h-5 mr-2" />
        <span>寫作建議</span>
      </div>
      <div className="flex items-center p-2 rounded hover:bg-slate-600 cursor-pointer">
        <FileText className="w-5 h-5 mr-2" />
        <span>正則化</span>
      </div>
      <div className="flex items-center p-2 rounded hover:bg-slate-600 cursor-pointer">
        <Scanner className="w-5 h-5 mr-2" />
        <span>OCR 服務</span>
      </div>
    </nav>
  </div>
);

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

const App = () => {
  const [selectedItem, setSelectedItem] = useState(null);

  return (
    <div className="flex">
      <MainSidebar onSelectItem={setSelectedItem} selectedItem={selectedItem} />
      {selectedItem === 'agents' && <SecondaryAgentSidebar />}
      <MainContent />
    </div>
  );
};

export default App;