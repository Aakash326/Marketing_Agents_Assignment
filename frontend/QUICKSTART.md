# Quick Start Guide

Get the Portfolio Intelligence frontend up and running in 5 minutes.

## Prerequisites

- Node.js 16+ installed
- Backend API running on `http://localhost:8000`

## Steps

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment (Optional)

The `.env` file is pre-configured. Only modify if your backend runs on a different URL:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The app will open at **http://localhost:3000**

### 4. Test the Application

#### First Time Setup
1. The app will load with **CLT-001** selected by default
2. You'll see the Dashboard page with a query input

#### Try These Queries
- "What stocks do I own?"
- "Show my portfolio allocation"
- "Which holdings have the best return?"
- "What's the current price of AAPL?"

#### Navigate the App
- **Dashboard**: Main query interface
- **Portfolio**: Detailed portfolio view with charts
- **Analytics**: Performance metrics and analytics

#### Switch Clients
- Use the dropdown in the header to switch between clients (CLT-001 through CLT-005)

#### Toggle Theme
- Click the sun/moon icon in the header to switch between light/dark themes

## Troubleshooting

### "Cannot connect to server"

**Solution**: Ensure the backend is running:

```bash
cd backend
uvicorn main:app --reload
```

### Port Already in Use

**Solution**: Kill the process or change the port in `vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 3001, // Change this
  }
})
```

### Dependencies Failed to Install

**Solution**: Clear cache and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install
```

## Production Build

```bash
# Build
npm run build

# Preview the build
npm run preview
```

The optimized production build will be in `dist/`

## Common Issues

### 1. Blank Screen

Check browser console for errors. Common causes:
- Backend not running
- Incorrect API URL in `.env`
- JavaScript errors (check console)

### 2. Styles Not Loading

```bash
# Restart dev server
npm run dev
```

### 3. API Errors

- Verify backend is running: `http://localhost:8000/health`
- Check network tab in browser DevTools
- Ensure CORS is configured on backend

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the codebase structure
- Customize components and styles
- Add new features

## Support

- Check [README.md](README.md) for detailed documentation
- Review [TEST_RESULTS.md](../backend/TEST_RESULTS.md) for backend API details
- Open an issue for bugs or questions

---

Happy coding! 🚀
