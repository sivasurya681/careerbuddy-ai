Write-Host "🔧 Fixing frontend errors..." -ForegroundColor Cyan

# Install missing packages
Write-Host "📦 Installing missing packages..." -ForegroundColor Yellow
npm install react-router-dom framer-motion styled-components axios react-dropzone react-icons @react-three/fiber @react-three/drei three

# Fix case-sensitive filename
Write-Host "📝 Fixing filename case..." -ForegroundColor Yellow
if (Test-Path "src\pages\chatbot.js") {
    Move-Item -Path "src\pages\chatbot.js" -Destination "src\pages\Chatbot.js" -Force
    Write-Host "✅ Renamed chatbot.js to Chatbot.js"
}

Write-Host "✅ Fix complete! Try running 'npm start' again." -ForegroundColor Green