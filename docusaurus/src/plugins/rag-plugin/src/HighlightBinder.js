// HighlightBinder.js - Handles highlight-to-ask functionality
export default function HighlightBinder() {
  // This function sets up the highlight-to-ask functionality
  // It's called by the Docusaurus plugin system
  if (typeof document !== 'undefined') {
    let isProcessing = false;

    document.addEventListener('mouseup', function() {
      if (isProcessing) return;

      const selection = window.getSelection();
      if (selection.toString().trim().length > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        // Create a temporary button to ask about selection
        const askButton = document.createElement('div');
        askButton.id = 'highlight-ask-button';
        askButton.style.position = 'fixed';
        askButton.style.left = (rect.right + 5) + 'px';
        askButton.style.top = rect.top + 'px';
        askButton.style.zIndex = '9999';
        askButton.style.backgroundColor = '#25c2a0';
        askButton.style.color = 'white';
        askButton.style.padding = '5px 10px';
        askButton.style.borderRadius = '4px';
        askButton.style.cursor = 'pointer';
        askButton.style.fontSize = '12px';
        askButton.textContent = 'Ask AI';

        askButton.onclick = function() {
          const selectedText = selection.toString();
          // Trigger the RAG chat with the selected text
          window.dispatchEvent(new CustomEvent('highlightAsk', {
            detail: { text: selectedText }
          }));
          document.body.removeChild(askButton);
        };

        document.body.appendChild(askButton);

        // Remove button after delay
        setTimeout(() => {
          if (document.getElementById('highlight-ask-button')) {
            document.body.removeChild(document.getElementById('highlight-ask-button'));
          }
        }, 3000);
      }
    });
  }
}