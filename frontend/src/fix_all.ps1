Write-Host "🔧 Fixing all frontend issues..." -ForegroundColor Cyan

# Install missing packages
Write-Host "📦 Installing missing packages..." -ForegroundColor Yellow
npm install react-markdown@8.0.0 --legacy-peer-deps
npm install @mediapipe/tasks-vision --legacy-peer-deps

# Check if any other packages are missing
Write-Host "🔍 Checking for other missing packages..." -ForegroundColor Yellow
npm list react-markdown @mediapipe/tasks-vision --depth=0

Write-Host "✅ Fix complete! Try running npm start again." -ForegroundColor Green