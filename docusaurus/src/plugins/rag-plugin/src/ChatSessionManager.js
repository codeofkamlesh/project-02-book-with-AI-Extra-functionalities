// ChatSessionManager.js - Manages chat sessions across pages
export default function ChatSessionManager() {
  // This function manages chat session persistence across page navigations
  // It's called by the Docusaurus plugin system
  if (typeof window !== 'undefined') {
    // Restore chat session from localStorage when page loads
    window.addEventListener('load', () => {
      const savedSession = localStorage.getItem('rag-chat-session');
      if (savedSession) {
        window.ragChatSession = JSON.parse(savedSession);
      } else {
        window.ragChatSession = {
          sessionId: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          messages: [],
          createdAt: new Date().toISOString()
        };
      }
    });

    // Save chat session to localStorage when page unloads
    window.addEventListener('beforeunload', () => {
      if (window.ragChatSession) {
        localStorage.setItem('rag-chat-session', JSON.stringify(window.ragChatSession));
      }
    });

    // Listen for highlight-ask events
    window.addEventListener('highlightAsk', (event) => {
      const selectedText = event.detail.text;

      // Trigger the RAG chat with the selected text
      if (window.ragChatWidget) {
        window.ragChatWidget.askAboutSelection(selectedText);
      } else {
        // If chat widget isn't initialized yet, queue the request
        window.pendingHighlightAsk = selectedText;
      }
    });
  }
}