const path = require('path');

// Docusaurus plugin for RAG chat, personalization, and translation features
module.exports = function (context, options) {
  return {
    name: 'docusaurus-physical-ai-features-plugin',

    getPathsToWatch() {
      return [];
    },

    getClientModules() {
      return [
        path.resolve(__dirname, './src/HighlightBinder.js'),
        path.resolve(__dirname, './src/ChatSessionManager.js'),
      ];
    },

    async contentLoaded({ actions }) {
      const { addRoute, createData } = actions;

      // Add routes for features if needed
    },

    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@site/src/components/rag': path.resolve(__dirname, '../../src/components/rag'),
            '@site/src/components/auth': path.resolve(__dirname, '../../src/components/auth'),
            '@site/src/components/personalize': path.resolve(__dirname, '../../src/components/personalize'),
            '@site/src/components/translate': path.resolve(__dirname, '../../src/components/translate'),
          },
        },
      };
    },

    injectHtmlTags() {
      return {
        postBodyTags: [
          `<script>
            // Highlight-to-ask functionality
            (function() {
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
            })();
          </script>`
        ],
      };
    },
  };
};