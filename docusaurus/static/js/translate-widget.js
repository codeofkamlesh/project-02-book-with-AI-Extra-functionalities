/**
 * Translation widget for Urdu translation functionality
 * This script handles Docusaurus route changes to ensure translation function remains available
 */

// Function to attach event listener to the translation button
function attachTranslationButton() {
  // Wait for the button to be in the DOM
  const button = document.getElementById('translate-urdu-btn');
  if (button) {
    // Remove any existing event listeners to avoid duplicates
    button.replaceWith(button.cloneNode(true)); // This removes event listeners
    const newButton = document.getElementById('translate-urdu-btn');

    // Attach the click handler to call the global translation function
    newButton.addEventListener('click', function() {
      if (window.translateToUrdu) {
        window.translateToUrdu();
      } else {
        console.error('translateToUrdu function not found. UrduTranslator component may not be loaded.');
      }
    });
  } else {
    console.warn('Urdu translation button not found in the DOM');
  }
}

// Initial setup when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  attachTranslationButton();
});

// Ensure translation function is available after route changes in Docusaurus
if (window.docusaurus) {
  window.docusaurus.eventManager.on('routeDidUpdate', function() {
    // Re-attach the button event listener after route changes
    setTimeout(attachTranslationButton, 100); // Small delay to ensure DOM is updated
    console.log('Route updated, translation functionality remains available');
  });
}

// Also try to attach the button on window load in case DOMContentLoaded fires too early
window.addEventListener('load', function() {
  setTimeout(attachTranslationButton, 50);
});