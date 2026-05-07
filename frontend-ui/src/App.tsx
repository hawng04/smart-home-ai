import 'regenerator-runtime/runtime'
import { useState, useEffect } from 'react'
import axios from 'axios'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'

function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');
  
  const [devices, setDevices] = useState([]);
  const [newName, setNewName] = useState('');
  const [newType, setNewType] = useState('light');

  const [personas, setPersonas] = useState([]);
  const [newPersonaName, setNewPersonaName] = useState('');
  const [newPersonaPrompt, setNewPersonaPrompt] = useState('');
  const [selectedPersonaId, setSelectedPersonaId] = useState('');

  const [message, setMessage] = useState('');
  const [currentSong, setCurrentSong] = useState(''); 
  const [chatHistory, setChatHistory] = useState([
    { sender: 'bot', text: 'Chào anh nờ. Bữa ni anh muốn O mần chi?' }
  ]);

  const { transcript, listening, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition();

  useEffect(() => {
    if (transcript) setMessage(transcript);
  }, [transcript]);

  useEffect(() => {
    fetchDevices();
    fetchPersonas();
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/devices/');
      setDevices(response.data);
    } catch (error) {}
  }

  const fetchPersonas = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/ai/personas');
      setPersonas(response.data);
      if (response.data.length > 0 && !selectedPersonaId) setSelectedPersonaId(response.data[0].id);
    } catch (error) {}
  }

  const toggleDevice = async (deviceId, currentStatus) => {
    const action = currentStatus === 'ON' ? 'OFF' : 'ON';
    try {
      await axios.post('http://localhost:8000/api/devices/control', { device_id: deviceId, action: action });
      fetchDevices();
    } catch (error) {}
  }

  const handleAddDevice = async (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    try {
      await axios.post('http://localhost:8000/api/devices/', { name: newName, device_type: newType });
      setNewName(''); fetchDevices();
    } catch (error) {}
  }

  const handleDeleteDevice = async (id) => {
    if (!window.confirm("Xác nhận xóa thiết bị?")) return;
    try {
      await axios.delete(`http://localhost:8000/api/devices/${id}`);
      fetchDevices();
    } catch (error) {}
  }

  const handleAddPersona = async (e) => {
    e.preventDefault();
    if (!newPersonaName.trim() || !newPersonaPrompt.trim()) return;
    try {
      await axios.post('http://localhost:8000/api/ai/personas', { name: newPersonaName, prompt: newPersonaPrompt });
      setNewPersonaName(''); setNewPersonaPrompt(''); fetchPersonas(); alert('Đã tạo nhân vật!');
    } catch (error) {}
  }

  const handleDeletePersona = async (id) => {
    if (!window.confirm("Xác nhận xóa?")) return;
    try {
      await axios.delete(`http://localhost:8000/api/ai/personas/${id}`);
      fetchPersonas();
    } catch (error) {}
  }

  const handleSendMessage = async () => {
    if (!message.trim()) return;
    if (SpeechRecognition && typeof SpeechRecognition.stopListening === 'function') SpeechRecognition.stopListening();
    resetTranscript();

    const userText = message;
    const newHistory = [...chatHistory, { sender: 'user', text: userText }];
    setChatHistory(newHistory);
    setMessage('');

    try {
      const response = await axios.post('http://localhost:8000/api/ai/chat', { 
        text: userText,
        persona_id: parseInt(selectedPersonaId) || 1
      });
      
      setChatHistory([...newHistory, { sender: 'bot', text: response.data.reply }]);
      
      if (response.data.audio_url) {
        new Audio(response.data.audio_url).play().catch(e => console.log(e));
      }

      if (response.data.youtube_id) {
        setCurrentSong(response.data.youtube_id); 
      } else if (response.data.song_name) {
        alert("Không tìm thấy bài hát này trên YouTube!");
      }

      fetchDevices();
    } catch (error) {
      setChatHistory([...newHistory, { sender: 'bot', text: 'Lỗi mạng rồi anh nờ!' }]);
    }
  }

  const toggleListening = () => {
    if (listening) {
      if (SpeechRecognition && typeof SpeechRecognition.stopListening === 'function') SpeechRecognition.stopListening();
    } else {
      resetTranscript();
      SpeechRecognition.startListening({ continuous: true, language: 'vi-VN' });
    }
  }

  if (!browserSupportsSpeechRecognition) return <span className="text-white p-5 block">Trình duyệt không hỗ trợ Mic.</span>;

  return (
    <div className="p-5 font-sans bg-[#1e1e1e] text-white min-h-screen">
      
      {/* MENU HEADER */}
      <div className="flex justify-between items-center border-b-2 border-[#444] pb-5">
        <h1 className="m-0 text-2xl font-bold">🏠 Smart Home AI</h1>
        <div className="flex gap-4">
          <button 
            onClick={() => setCurrentTab('dashboard')} 
            className={`px-5 py-2.5 cursor-pointer text-white border-none rounded-lg font-bold transition-colors ${currentTab === 'dashboard' ? 'bg-blue-600' : 'bg-[#444] hover:bg-[#555]'}`}
          >
            Bảng điều khiển
          </button>
          <button 
            onClick={() => setCurrentTab('admin')} 
            className={`px-5 py-2.5 cursor-pointer text-white border-none rounded-lg font-bold transition-colors ${currentTab === 'admin' ? 'bg-red-600' : 'bg-[#444] hover:bg-[#555]'}`}
          >
            Quản trị
          </button>
        </div>
      </div>

      {/* TAB: DASHBOARD */}
      {currentTab === 'dashboard' && (
        <div className="flex flex-col lg:flex-row gap-10 mt-8">
          
          {/* CỘT TRÁI: THIẾT BỊ & YOUTUBE */}
          <div className="flex-[2]">
            <h2 className="text-xl font-semibold mb-4">Thiết bị trong nhà</h2>
            <div className="flex gap-5 flex-wrap">
              {devices.map((device) => (
                <div 
                  key={device.id} 
                  className={`border border-[#444] p-5 rounded-2xl w-[220px] transition-all duration-300 ${device.status === 'ON' ? 'bg-green-700 shadow-[0_0_15px_#4caf50]' : 'bg-[#333]'}`}
                >
                  <h3 className="m-0 mb-2.5 text-lg font-medium">{device.name}</h3>
                  <div className="flex justify-between items-center mt-5">
                    <span className={`font-bold ${device.status === 'ON' ? 'text-green-200' : 'text-orange-300'}`}>
                      {device.status}
                    </span>
                    <button 
                      onClick={() => toggleDevice(device.id, device.status)} 
                      className="px-4 py-2 cursor-pointer bg-blue-600 hover:bg-blue-500 text-white border-none rounded-lg transition-colors"
                    >
                      Công tắc
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* YOUTUBE PLAYER */}
            {currentSong && (
              <div className="mt-10 rounded-2xl overflow-hidden border border-[#444] bg-[#2d2d2d]">
                <div className="bg-[#1a1a1a] p-4 flex justify-between items-center">
                  <h3 className="m-0 text-base text-red-400 font-semibold">🎵 Đang phát: {currentSong}</h3>
                  <button 
                    onClick={() => setCurrentSong('')} 
                    className="bg-transparent border-none text-gray-400 hover:text-white cursor-pointer font-bold text-lg"
                  >
                    ✖ Tắt nhạc
                  </button>
                </div>
                <iframe
                  className="w-full h-[250px]"
                  src={`https://www.youtube.com/embed/${currentSong}?autoplay=1`} 
                  frameBorder="0"
                  allow="autoplay; encrypted-media"
                  allowFullScreen
                ></iframe>
              </div>
            )}
          </div>

          {/* CỘT PHẢI: CHATBOT */}
          <div className="flex-1 bg-[#2d2d2d] rounded-2xl flex flex-col h-[600px] border border-[#444]">
            <div className="p-4 border-b border-[#444] bg-[#1a1a1a] rounded-t-2xl flex justify-between items-center">
              <div className="flex items-center gap-4">
                <h2 className="m-0 text-lg font-semibold">🤖 Trợ lý AI</h2>
                <select 
                  value={selectedPersonaId} 
                  onChange={(e) => setSelectedPersonaId(e.target.value)} 
                  className="px-2.5 py-1.5 rounded-lg bg-[#333] text-white border border-[#555] cursor-pointer outline-none focus:border-blue-500"
                >
                  {personas.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>
              {listening && <span className="text-red-500 font-bold animate-pulse">Đang nghe... 🔴</span>}
            </div>
            
            <div className="flex-1 p-5 overflow-y-auto flex flex-col gap-4">
              {chatHistory.map((msg, index) => (
                <div 
                  key={index} 
                  className={`px-4 py-2.5 rounded-2xl max-w-[80%] leading-relaxed ${msg.sender === 'user' ? 'self-end bg-blue-600 text-white' : 'self-start bg-[#444] text-gray-100'}`}
                >
                  {msg.text}
                </div>
              ))}
            </div>

            <div className="p-4 border-t border-[#444] flex gap-2.5 bg-[#1a1a1a] rounded-b-2xl">
              <button 
                onClick={toggleListening} 
                className={`text-white border-none rounded-full w-11 h-11 flex items-center justify-center cursor-pointer text-lg transition-colors ${listening ? 'bg-red-600' : 'bg-[#444] hover:bg-[#555]'}`}
              >
                🎤
              </button>
              <input 
                type="text" 
                value={message} 
                onChange={(e) => setMessage(e.target.value)} 
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()} 
                placeholder="Nhập lệnh..." 
                className="flex-1 p-2.5 rounded-lg border border-[#555] focus:border-blue-500 outline-none bg-[#333] text-white transition-colors" 
              />
              <button 
                onClick={handleSendMessage} 
                className="bg-green-600 hover:bg-green-500 text-white border-none rounded-lg px-4 cursor-pointer font-medium transition-colors"
              >
                Gửi
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB: ADMIN */}
      {currentTab === 'admin' && (
        <div className="mt-8 flex flex-col lg:flex-row gap-10">
          
          {/* CỘT TRÁI: THIẾT BỊ */}
          <div className="flex-1">
            <h2 className="text-xl font-semibold mb-4">⚙️ Quản lý thiết bị IoT</h2>
            <form onSubmit={handleAddDevice} className="bg-[#2d2d2d] p-5 rounded-2xl mb-5 border border-[#444]">
              <div className="flex gap-2.5">
                <input 
                  type="text" 
                  placeholder="Tên thiết bị..." 
                  value={newName} 
                  onChange={e => setNewName(e.target.value)} 
                  className="flex-1 p-2.5 rounded-lg border border-[#555] focus:border-blue-500 bg-[#333] text-white outline-none transition-colors" 
                />
                <button 
                  type="submit" 
                  className="px-4 py-2.5 bg-green-600 hover:bg-green-500 text-white border-none rounded-lg cursor-pointer font-medium transition-colors"
                >
                  + Thêm
                </button>
              </div>
            </form>
            <div className="bg-[#2d2d2d] p-5 rounded-2xl border border-[#444]">
              {devices.map(device => (
                <div key={device.id} className="flex justify-between items-center py-2.5 border-b border-[#444] last:border-0">
                  <span className="text-gray-200">{device.name}</span>
                  <button 
                    onClick={() => handleDeleteDevice(device.id)} 
                    className="bg-red-600 hover:bg-red-500 text-white border-none rounded-md px-3 py-1.5 cursor-pointer transition-colors"
                  >
                    Xóa
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* CỘT PHẢI: KỊCH BẢN AI */}
          <div className="flex-1">
            <h2 className="text-xl font-semibold mb-4">🎭 Quản lý Kịch bản AI</h2>
            <form onSubmit={handleAddPersona} className="bg-[#2d2d2d] p-5 rounded-2xl mb-5 border border-[#444]">
              <input 
                type="text" 
                placeholder="Tên nhân vật..." 
                value={newPersonaName} 
                onChange={e => setNewPersonaName(e.target.value)} 
                className="w-full p-2.5 rounded-lg border border-[#555] focus:border-blue-500 bg-[#333] text-white mb-2.5 outline-none box-border transition-colors" 
              />
              <textarea 
                placeholder="Viết kịch bản tính cách (Prompt) vào đây..." 
                value={newPersonaPrompt} 
                onChange={e => setNewPersonaPrompt(e.target.value)} 
                className="w-full p-2.5 rounded-lg border border-[#555] focus:border-blue-500 bg-[#333] text-white min-h-[100px] mb-2.5 outline-none box-border resize-y transition-colors font-sans" 
              />
              <button 
                type="submit" 
                className="w-full p-2.5 bg-blue-600 hover:bg-blue-500 text-white border-none rounded-lg cursor-pointer font-bold transition-colors"
              >
                + Tạo Nhân Vật
              </button>
            </form>
            <div className="bg-[#2d2d2d] p-5 rounded-2xl border border-[#444]">
              {personas.map(p => (
                <div key={p.id} className="flex justify-between items-center py-2.5 border-b border-[#444] last:border-0">
                  <span className="font-bold text-gray-200">{p.name}</span>
                  <button 
                    onClick={() => handleDeletePersona(p.id)} 
                    className="bg-red-600 hover:bg-red-500 text-white border-none rounded-md px-3 py-1.5 cursor-pointer transition-colors"
                  >
                    Xóa
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
export default App