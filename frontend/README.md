# Portfolio Intelligence System - Frontend

A modern, production-ready React frontend for the Portfolio Intelligence System. Built with React 18, Tailwind CSS, and a multi-agent AI backend integration.

## Features

✨ **Modern UI/UX**
- Clean, professional design inspired by Vercel, Linear, and Stripe
- Fully responsive (mobile, tablet, desktop)
- Dark/light theme support with system preference detection
- Smooth animations and transitions

🤖 **AI-Powered Query System**
- Natural language portfolio queries
- Real-time agent activity tracking
- Clarification handling
- Conversation history with session management

📊 **Portfolio Management**
- Interactive portfolio dashboard
- Real-time data visualization with charts
- Holdings overview with gain/loss tracking
- Asset allocation pie charts
- Performance analytics

🎨 **Professional Components**
- Reusable component library
- Consistent design system
- Accessibility-first (WCAG AA compliant)
- Loading states and error handling

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS 3** - Styling framework
- **React Router 6** - Client-side routing
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **React Markdown** - Markdown rendering
- **Lucide React** - Icon library
- **React Hot Toast** - Notifications
- **Framer Motion** - Animations (ready to use)
- **Headless UI** - Accessible UI components

## Prerequisites

- Node.js 16+ and npm/yarn
- Backend API running on `http://localhost:8000`

## Getting Started

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# or with yarn
yarn install
```

### Environment Configuration

The `.env` file is already configured with default values:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Portfolio Intelligence
VITE_APP_VERSION=1.0.0
```

Update these values if your backend is running on a different URL.

### Development

Start the development server:

```bash
npm run dev
```

The app will open at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── agent/       # Agent activity components
│   │   ├── common/      # Reusable UI components
│   │   ├── layout/      # Layout components
│   │   ├── portfolio/   # Portfolio-specific components
│   │   ├── query/       # Query input/response components
│   │   └── session/     # Session management components
│   ├── context/         # React context providers
│   ├── hooks/           # Custom React hooks
│   ├── pages/           # Page components
│   ├── services/        # API and storage services
│   ├── utils/           # Utility functions
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── .env                 # Environment variables
├── index.html           # HTML template
├── package.json         # Dependencies
├── tailwind.config.js   # Tailwind configuration
├── vite.config.js       # Vite configuration
└── README.md            # This file
```

## Key Features Guide

### Dashboard Page

The main interface for querying the AI system:

1. **Query Input**
   - Type natural language queries
   - Use keyboard shortcuts: `Cmd/Ctrl + K` to focus, `Cmd/Ctrl + Enter` to submit
   - Character counter with validation
   - Quick suggestion chips

2. **Response Display**
   - Markdown-formatted responses
   - Agent activity badges
   - Execution time tracking
   - Copy to clipboard
   - Expand/collapse for long responses

3. **Agent Activity Panel**
   - Visual workflow diagram
   - Real-time agent status
   - Hover for agent descriptions
   - Execution metrics

4. **Conversation History**
   - Collapsible message history
   - User/assistant message bubbles
   - Timestamps
   - Copy individual messages
   - Export session

### Portfolio Page

Comprehensive portfolio overview:

- **Summary Cards**: Total holdings, value, gain/loss
- **Asset Allocation**: Interactive pie chart
- **Performance Chart**: Gain/loss by holding
- **Holdings List**: Sortable cards with detailed info
- **Auto-refresh**: Updates every 5 minutes

### Analytics Page

Detailed performance analytics:

- **Key Metrics**: Total return, average return %, top gainer/loser
- **Performance Charts**: Visual representations
- **Holdings Table**: Sortable, detailed breakdown

## Available Clients

The system comes with 5 pre-configured clients:

- CLT-001 (7 holdings)
- CLT-002 (8 holdings)
- CLT-003 (5 holdings)
- CLT-004 (12 holdings)
- CLT-005 (6 holdings)

## API Integration

### Endpoints Used

```javascript
// Health check
GET /health

// Main query
POST /api/v1/query
Body: { query, client_id, session_id, conversation_history }

// Clarification
POST /api/v1/query/clarify
Body: { session_id, clarification, original_query }

// Session management
GET /api/v1/session/{session_id}
DELETE /api/v1/session/{session_id}

// Portfolio data
GET /api/v1/clients/{client_id}/portfolio
```

### Custom Hooks

- `useQuery()` - Query execution and clarification
- `useSession()` - Session management and conversation history
- `usePortfolio()` - Portfolio data fetching with auto-refresh
- `useApi()` - Generic API call wrapper

## Keyboard Shortcuts

- `Cmd/Ctrl + K` - Focus query input
- `Cmd/Ctrl + Enter` - Submit query
- `Esc` - Close modals
- `Enter` - Submit in modals
- `Shift + Enter` - New line in textarea

## Theme Support

The app supports both light and dark themes:

- Auto-detects system preference on first load
- Toggle with the theme button in header
- Preference saved to localStorage
- Smooth transitions between themes

## Error Handling

- Global error boundary for React errors
- API error interception and user-friendly messages
- Loading states throughout the app
- Toast notifications for success/error feedback
- Retry mechanisms for failed requests

## Performance Optimizations

- Code splitting with React.lazy (ready to implement)
- Memoization with React.memo for expensive components
- Auto-resize textareas
- Debounced inputs (where applicable)
- Optimized re-renders with useCallback and useMemo

## Accessibility

- ARIA labels on all interactive elements
- Keyboard navigation support
- Focus indicators
- Screen reader friendly
- Semantic HTML
- Color contrast ratios (WCAG AA)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Backend Connection Issues

If you see "Cannot connect to server" errors:

1. Ensure the backend is running: `cd backend && uvicorn main:app --reload`
2. Check the backend URL in `.env` matches your setup
3. Verify CORS is configured on the backend

### Build Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

### Styling Issues

```bash
# Rebuild Tailwind
npm run dev
```

## Contributing

1. Follow the existing code structure
2. Use TypeScript (optional, but recommended for type safety)
3. Write meaningful commit messages
4. Test on multiple screen sizes
5. Ensure accessibility standards

## Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## Future Enhancements

- [ ] User authentication
- [ ] Real-time WebSocket updates
- [ ] Advanced filtering and search
- [ ] Export reports to PDF
- [ ] Email notifications
- [ ] Customizable dashboards
- [ ] Multi-language support
- [ ] Mobile app (React Native)

## License

MIT

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@portfoliointelligence.com

---

Built with ❤️ by the Portfolio Intelligence Team
